"""summarycodec CLI: encode / inspect / verify / decode / reproduce / reanalyze.

Usage:
  summarycodec encode --object mean_sd --format svg --level L2 \
      --inputs data.json --out fig.svg --title "Group means"
  summarycodec verify fig.svg
  summarycodec inspect fig.svg
  summarycodec decode fig.svg [--query NAME --args '[...]']
"""

from __future__ import annotations

import argparse
import json
import sys

from ..core import Level, canonical_json
from ..core.codec import encode as encode_object
from ..decoders import decode, detect_and_extract
from ..objects import REGISTRY
from ..validators import validate


def _obj(args):
    inputs = json.load(open(args.inputs))
    cls = REGISTRY[args.object]
    return cls(inputs, title=args.title or "",
               rounding=getattr(args, "rounding", "2"))


def main(argv=None):
    p = argparse.ArgumentParser(prog="summarycodec")
    sub = p.add_subparsers(dest="cmd", required=True)

    e = sub.add_parser("encode")
    e.add_argument("--object", required=True, choices=sorted(REGISTRY))
    e.add_argument("--format", required=True, choices=["svg", "png", "tiff"])
    e.add_argument("--level", required=True, choices=[l.value for l in Level])
    e.add_argument("--inputs", required=True)
    e.add_argument("--out", required=True)
    e.add_argument("--title", default="")
    e.add_argument("--rounding", default="2")
    e.add_argument("--actor", default="author")

    i = sub.add_parser("inspect")
    i.add_argument("file")

    v = sub.add_parser("verify")
    v.add_argument("file")

    d = sub.add_parser("decode")
    d.add_argument("file")
    d.add_argument("--out")

    r = sub.add_parser("reanalyze")
    r.add_argument("file")
    r.add_argument("--query", required=True)
    r.add_argument("--args", default="[]")

    args = p.parse_args(argv)

    if args.cmd == "encode":
        manifest = encode_object(_obj(args), args.format, Level(args.level),
                                 args.out, actor=args.actor)
        print(json.dumps({"object_id": manifest["object_id"],
                          "object_hash": manifest["object_hash"],
                          "level": manifest["declared_level"],
                          "format": args.format, "out": args.out}, indent=2))
        return 0

    if args.cmd == "inspect":
        adapter, env = detect_and_extract(args.file)
        if adapter is None:
            print("FORMAT_UNSUPPORTED"); return 1
        if env is None:
            print(f"format={adapter.name} envelope=ABSENT"); return 1
        m = env["manifest"]
        print(json.dumps({"format": adapter.name,
                          "object_id": m["object_id"],
                          "object_class": m["object_class"],
                          "declared_level": m["declared_level"],
                          "object_hash": m["object_hash"],
                          "provenance_events": len(m["provenance"]["chain"])},
                         indent=2))
        return 0

    if args.cmd == "verify":
        rep = validate(args.file)
        print(json.dumps(rep.to_dict(), indent=2))
        return 0 if rep.ok else 1

    if args.cmd == "decode":
        payload = decode(args.file)
        text = canonical_json(payload).decode("utf-8")
        if args.out:
            with open(args.out, "w") as fh:
                fh.write(text)
        else:
            print(text)
        return 0

    if args.cmd == "reanalyze":
        payload = decode(args.file)
        obj = REGISTRY[payload["object_class"]](
            payload["inputs"], title=payload.get("title", ""),
            rounding=payload.get("rounding_rule", "2"))
        fn = obj.secondary_queries().get(args.query)
        if fn is None:
            print(f"query not declared: {args.query}", file=sys.stderr)
            return 2
        out = fn(*json.loads(args.args))
        print(json.dumps(out, indent=2, default=str))
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
