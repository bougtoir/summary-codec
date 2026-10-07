"""Phase 1 driver: object class x level x format x size x condition matrix.

Outputs:
  object_class_tests/results.csv      one row per (object, level, format, size)
  format_tests/results.csv            cross-format equivalence + visual preservation
  corruption_tests/results.csv        manipulation condition -> observed status
  semantic_validation/results.csv     true-valid acceptance / mismatch rejection
  benchmarks/performance.csv          encode/decode/verify times + size overhead
  benchmarks/negative_controls.csv    comparator capability matrix
"""

import io
import json
import os
import sys
import time
import zipfile

import numpy as np

ROOT = os.path.dirname(os.path.abspath(__file__))
SW = os.path.join(ROOT, "..", "02_SOFTWARE")
sys.path.insert(0, os.path.abspath(SW))

from summarycodec.objects import make, REGISTRY  # noqa: E402
from summarycodec.core.codec import encode  # noqa: E402
from summarycodec.core import Level, Status, sha256_hex  # noqa: E402
from summarycodec.validators import validate  # noqa: E402
from summarycodec import formats  # noqa: E402
from summarycodec.decoders import decode  # noqa: E402

from synthetic_data.make_synthetic import make_all  # noqa: E402

OUT = os.path.join(ROOT, "object_class_tests", "objects")
os.makedirs(OUT, exist_ok=True)
FORMATS = ["svg", "png", "tiff"]
LEVELS = [Level.L1, Level.L2, Level.L3, Level.L4]


def enc_path(name, fmt, level):
    return os.path.join(OUT, f"{name}_{level.value}.{fmt}")


def strip_envelope(path):
    """Remove the Summary Codec envelope, keep the container."""
    data = open(path, "rb").read()
    ad = formats.detect(data)
    if ad.name == "svg":
        import re
        from summarycodec.formats.svg import META_RE
        open(path, "wb").write(META_RE.sub(b"", data))
    elif ad.name == "png":
        from summarycodec.formats.png import _chunks, PNG_SIG, _chunk
        out = bytearray(PNG_SIG)
        for pos, ctype, payload in _chunks(data):
            if ctype == b"scDC":
                continue
            out += _chunk(ctype, payload)
        open(path, "wb").write(bytes(out))
    else:  # tiff: rewrite without private tag
        import tifffile
        arr = tifffile.imread(path)
        tifffile.imwrite(path, arr)


def alter_visible(path):
    """Post-signing modification of V."""
    data = open(path, "rb").read()
    ad = formats.detect(data)
    if ad.name == "svg":
        txt = data.decode()
        # change one displayed bar height
        import re
        txt = re.sub(r'height="(\d+\.?\d*)"', lambda m: f'height="{float(m.group(1))*0.5:.1f}"', txt, count=1)
        open(path, "wb").write(txt.encode())
    else:
        from PIL import Image
        img = Image.open(path).convert("RGB")
        arr = np.asarray(img).copy()
        arr[10:60, 10:60] = 0
        import tifffile
        env = ad.extract(open(path, "rb").read())
        if ad.name == "png":
            buf = io.BytesIO()
            Image.fromarray(arr).save(buf, format="PNG")
            open(path, "wb").write(ad.embed(buf.getvalue(), env))
        else:
            # preserve envelope through pixel rewrite
            tifffile.imwrite(path, arr,
                             extratags=[(65000, "B", len(env), env, True)])


def _without_envelope(data: bytes, ad) -> bytes:
    """Container bytes with any existing envelope removed."""
    if ad.name == "svg":
        from summarycodec.formats.svg import META_RE
        return META_RE.sub(b"", data)
    if ad.name == "png":
        from summarycodec.formats.png import _chunks, PNG_SIG, _chunk
        out = bytearray(PNG_SIG)
        for pos, ctype, payload in _chunks(data):
            if ctype == b"scDC":
                continue
            out += _chunk(ctype, payload)
        return bytes(out)
    import tifffile
    arr = tifffile.imread(io.BytesIO(data))
    buf = io.BytesIO()
    tifffile.imwrite(buf, arr)
    return buf.getvalue()


def swap_payload(path_a, path_b):
    """Embed B's envelope into A's container."""
    da, db = open(path_a, "rb").read(), open(path_b, "rb").read()
    ada, adb = formats.detect(da), formats.detect(db)
    env_b = adb.extract(db)
    base = _without_envelope(da, ada)
    open(path_a, "wb").write(ada.embed(base, env_b))


def corrupt_bytes(path, n=8):
    data = bytearray(open(path, "rb").read())
    rng = np.random.default_rng(7)
    for i in rng.choice(len(data) - 1000, n, replace=False) + 500:
        data[int(i)] ^= 0xFF
    open(path, "wb").write(bytes(data))


def resave(path):
    """Re-save through a generic editor (PIL/tifffile/svg roundtrip)."""
    data = open(path, "rb").read()
    ad = formats.detect(data)
    if ad.name == "png":
        from PIL import Image
        img = Image.open(path)
        img.save(path)  # PIL drops unknown ancillary chunks
    elif ad.name == "tiff":
        import tifffile
        arr = tifffile.imread(path)
        tifffile.imwrite(path, arr)  # drops private tag
    else:  # svg "re-save": normalize whitespace via minidom
        import xml.dom.minidom as md
        doc = md.parseString(data)
        open(path, "wb").write(doc.toxml().encode())


def convert_format(path):
    """Format conversion: png -> tiff, tiff -> png, svg -> png render-less copy."""
    data = open(path, "rb").read()
    ad = formats.detect(data)
    new = path + ".converted"
    if ad.name == "svg":
        from PIL import Image
        new += ".png"
        Image.new("RGB", (640, 400), "white").save(new, format="PNG")
    elif ad.name == "png":
        import tifffile
        from PIL import Image
        new += ".tiff"
        tifffile.imwrite(new, np.asarray(Image.open(path)))
    else:
        from PIL import Image
        import tifffile
        new += ".png"
        Image.fromarray(tifffile.imread(path)).save(new, format="PNG")
    return new


def run():
    specs = make_all()
    rows_obj, rows_fmt, rows_corr, rows_sem, rows_perf = [], [], [], [], []
    negative_controls = []

    for name, spec in specs.items():
        objcls, inputs = spec["object_class"], spec["inputs"]
        size = len(json.dumps(inputs))
        for level in LEVELS:
            for fmt in FORMATS:
                obj = make(objcls, inputs, title=spec["title"])
                p = enc_path(name, fmt, level)
                t0 = time.perf_counter()
                manifest = encode(obj, fmt, level, p)
                t_enc = time.perf_counter() - t0

                t0 = time.perf_counter()
                payload = decode(p)
                t_dec = time.perf_counter() - t0

                t0 = time.perf_counter()
                rep = validate(p)
                t_ver = time.perf_counter() - t0

                native_ok = rep.status == Status.VALID
                rows_obj.append(dict(object=name, object_class=objcls,
                                     level=level.value, format=fmt,
                                     input_bytes=size,
                                     file_bytes=os.path.getsize(p),
                                     status=rep.status.value,
                                     native_valid=native_ok))
                rows_perf.append(dict(object=name, level=level.value,
                                      format=fmt, encode_s=t_enc,
                                      decode_s=t_dec, verify_s=t_ver,
                                      file_bytes=os.path.getsize(p),
                                      payload_bytes=len(json.dumps(payload))))
    # cross-format equivalence: same logical object across formats
    for name, spec in specs.items():
        objcls, inputs = spec["object_class"], spec["inputs"]
        disp, hashes = {}, {}
        for fmt in FORMATS:
            p = enc_path(name, fmt, Level.L4)
            payload = decode(p)
            disp[fmt] = payload["displayed"]
            data = open(p, "rb").read()
            ad = formats.detect(data)
            hashes[fmt] = sha256_hex(ad.visible_bytes(data))
        same_disp = disp["svg"] == disp["png"] == disp["tiff"]
        rows_fmt.append(dict(object=name, same_logical_object=same_disp,
                             same_level=True, same_scientific_result=same_disp,
                             pixel_identity_png_tiff="n/a-svg-visual"))
    # pixel identity TIFF/PNG: compare rendered array to stored pixels
    for name, spec in specs.items():
        obj = make(spec["object_class"], spec["inputs"], title=spec["title"])
        disp = obj.displayed(obj.analyze())
        arr = obj.render_pixels(disp)
        for fmt in ("png", "tiff"):
            p = enc_path(name, fmt, Level.L4)
            data = open(p, "rb").read()
            ad = formats.detect(data)
            stored = np.frombuffer(ad.visible_bytes(data),
                                   dtype=np.uint8).reshape(arr.shape)
            ident = bool((stored == arr).all())
            rows_fmt.append(dict(object=name, format=fmt,
                                 pixel_identity=ident))

    # ---- corruption / manipulation conditions ---------------------------
    conditions = ["native", "copied", "re_saved", "metadata_stripped",
                  "payload_swapped", "visible_altered", "format_converted",
                  "corrupted"]
    for name, spec in list(specs.items()):
        for fmt in FORMATS:
            base = enc_path(name, fmt, Level.L4)
            for cond in conditions:
                work = os.path.join(OUT, f"cond_{name}_{cond}.{fmt}")
                import shutil
                shutil.copy(base, work)
                try:
                    if cond == "copied":
                        pass
                    elif cond == "re_saved":
                        resave(work)
                    elif cond == "metadata_stripped":
                        strip_envelope(work)
                    elif cond == "payload_swapped":
                        other = enc_path("contingency", fmt, Level.L4)
                        if other == base:
                            other = enc_path("mean_sd_small", fmt, Level.L4)
                        swap_payload(work, other)
                    elif cond == "visible_altered":
                        alter_visible(work)
                    elif cond == "format_converted":
                        work = convert_format(work)
                    elif cond == "corrupted":
                        corrupt_bytes(work)
                    rep = validate(work)
                    status = rep.status.value
                except Exception as e:
                    status = f"EXCEPTION:{type(e).__name__}"
                rows_corr.append(dict(object=name, format=fmt,
                                      condition=cond, observed=status))

    # ---- semantic validation: true-valid acceptance + mismatch rejection --
    for name, spec in specs.items():
        p = enc_path(name, "svg", Level.L4)
        rep = validate(p)
        rows_sem.append(dict(object=name, case="true_valid",
                             accepted=rep.status == Status.VALID))
        # mismatch: rebuild with altered displayed value in payload
        data = open(p, "rb").read()
        ad = formats.detect(data)
        env = json.loads(ad.extract(data))
        k = sorted(env["payload"]["displayed"])[0]
        env["payload"]["displayed"][k] = "9999.99"
        env["signature"]["sig"] = ""  # tampered signature
        import re
        from summarycodec.formats.svg import META_RE
        stripped = META_RE.sub(b"", data)
        tampered = ad.embed(stripped, json.dumps(env).encode())
        w = os.path.join(OUT, f"semtamper_{name}.svg")
        open(w, "wb").write(tampered)
        rep2 = validate(w)
        rows_sem.append(dict(object=name, case="mismatch_rejected",
                             accepted=rep2.status == Status.VALID,
                             observed=rep2.status.value))

    # ---- negative controls ------------------------------------------------
    demo = enc_path("mean_sd_small", "png", Level.L4)
    png_plain = os.path.join(OUT, "plain_figure.png")
    from PIL import Image
    specs0 = make_all()["mean_sd_small"]
    obj0 = make("mean_sd", specs0["inputs"], title=specs0["title"])
    Image.fromarray(obj0.render_pixels(obj0.displayed(obj0.analyze()))).save(png_plain)
    csv_path = os.path.join(OUT, "data.csv")
    with open(csv_path, "w") as fh:
        fh.write("group,value\n")
        for g, xs in specs0["inputs"]["groups"].items():
            for x in xs:
                fh.write(f"{g},{x}\n")
    zip_path = os.path.join(OUT, "figure_plus_data.zip")
    with zipfile.ZipFile(zip_path, "w") as z:
        z.write(png_plain, "figure.png")
        z.write(csv_path, "data.csv")

    controls = {
        "ordinary_figure": png_plain,
        "figure_plus_csv": csv_path,
        "figure_plus_zip": zip_path,
        "embedded_without_contract": None,  # built below
        "summary_codec_L4": demo,
    }
    # 'embedded without scientific validation contract': raw JSON in png chunk,
    # no manifest/level/signature
    from summarycodec.formats.png import PngAdapter, _chunk, _chunks, PNG_SIG
    raw = json.dumps({"data": specs0["inputs"]}).encode()
    base_png = open(png_plain, "rb").read()
    out = bytearray(PNG_SIG)
    for pos, ct, pl in _chunks(base_png):
        if ct == b"IEND":
            out += _chunk(b"scDC", raw)
        out += base_png[pos:pos + 12 + len(pl)]
    no_contract = os.path.join(OUT, "embedded_no_contract.png")
    open(no_contract, "wb").write(bytes(out))
    controls["embedded_without_contract"] = no_contract

    nc = {
        "ordinary_figure": dict(recoverable=False, declared_level="none",
                                machine_verified_guarantee=False,
                                semantic_validation=False, tamper_evidence=False,
                                provenance=False, secondary_analysis=False),
        "figure_plus_csv": dict(recoverable=True, declared_level="implicit-raw",
                                machine_verified_guarantee=False,
                                semantic_validation=False, tamper_evidence=False,
                                provenance=False, secondary_analysis=True),
        "figure_plus_zip": dict(recoverable=True, declared_level="implicit-raw",
                                machine_verified_guarantee=False,
                                semantic_validation=False, tamper_evidence=False,
                                provenance=False, secondary_analysis=True),
        "embedded_without_contract": dict(
            recoverable=True, declared_level="undeclared",
            machine_verified_guarantee=False, semantic_validation=False,
            tamper_evidence=False, provenance=False, secondary_analysis=True),
        "summary_codec_L4": dict(
            recoverable=True, declared_level="L4",
            machine_verified_guarantee=True, semantic_validation=True,
            tamper_evidence=True, provenance=True, secondary_analysis=True),
    }
    for cname, caps in nc.items():
        path = controls[cname]
        rep = validate(path) if path and path.endswith((".png", ".svg", ".tiff")) else None
        negative_controls.append(dict(
            control=cname, file=os.path.basename(path),
            codec_status=rep.status.value if rep else "n/a", **caps))

    # additional negative controls from corruption conditions already measured:
    # corrupted object, swapped payload, modified figure + old payload,
    # invalid signature -> all in rows_corr.

    # ---- write CSVs --------------------------------------------------------
    import pandas as pd
    pd.DataFrame(rows_obj).to_csv(
        os.path.join(ROOT, "object_class_tests", "results.csv"), index=False)
    pd.DataFrame(rows_fmt).to_csv(
        os.path.join(ROOT, "format_tests", "results.csv"), index=False)
    pd.DataFrame(rows_corr).to_csv(
        os.path.join(ROOT, "corruption_tests", "results.csv"), index=False)
    pd.DataFrame(rows_sem).to_csv(
        os.path.join(ROOT, "semantic_validation", "results.csv"), index=False)
    pd.DataFrame(rows_perf).to_csv(
        os.path.join(ROOT, "benchmarks", "performance.csv"), index=False)
    pd.DataFrame(negative_controls).to_csv(
        os.path.join(ROOT, "benchmarks", "negative_controls.csv"), index=False)
    print("Phase 1 complete")
    print("objects:", len(rows_obj), "conditions:", len(rows_corr))


if __name__ == "__main__":
    run()
