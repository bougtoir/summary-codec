# Adding a new object class (developer example)

Worked example: `dose_response` — a minimal object reporting response
rates at discrete dose levels. Demonstrates architectural extensibility
without adding a production object. ~120 lines including the test.

## 1. Object schema

```python
# inputs contract (documented in the class docstring)
inputs = {
    "doses":  [0, 10, 50, 100],          # numeric dose levels
    "n":      [50, 50, 50, 50],          # subjects per level
    "events": [2, 8, 25, 41],            # responders per level
}
```

## 2. Visible representation mapping

`displayed()` defines exactly what a reader sees — stable cell labels →
post-rounding values. This is what `SEMANTIC_MISMATCH` recomputes:

```python
def displayed(self, results):
    out = {}
    for d, n, e, r in zip(self.inputs["doses"], self.inputs["n"],
                          self.inputs["events"], results["rate"]):
        out[f"dose={d:g}"] = f"{e}/{n} ({self.fmt(r)})"
    out["max_rate"] = self.fmt(results["max_rate"])
    return out
```

## 3. Recovery-level declaration

Declare only what the class can *prove*: L1 needs `displayed`; L2 needs
`analysis_results` matching `analyze()`; L3 needs every member of
`secondary_queries()` to execute; L4 needs `canonical_dataset()` to hash
identically. `encode()` refuses unprovable levels (e.g. L3 with
`secondary_queries() == {}`).

## 4. Validation-contract registration

```python
# summarycodec/objects/dose_response.py
class DoseResponse(ScientificObject):
    object_class = "dose_response"               # add to MANIFEST_SCHEMA enum
    equivalence_rule = "dose-response table identical; rates equal at declared rounding"
```

Register in `summarycodec/objects/__init__.py` (`REGISTRY`) and add
`"dose_response"` to the `object_class` enum in
`01_SPECIFICATION/MANIFEST_SCHEMA.json`.

## 5. Semantic recomputation function

```python
def analyze(self):
    d = self.inputs
    rates = [e / n for e, n in zip(d["events"], d["n"])]
    # Cochran–Armitage-style trend is optional; rates alone suffice.
    return {"rate": rates, "max_rate": max(rates),
            "pooled": sum(d["events"]) / sum(d["n"])}
```

## 6–8. Encode / decode / verify paths — free

No format or envelope code needed; the core handles all three:

```python
obj = make("dose_response", inputs, title="Dose–response")
encode(obj, "svg", Level.L4, "fig.svg")
payload = decode("fig.svg")            # inputs + displayed + results
rep = validate("fig.svg")              # VALID + 9 checks
```

## 9. Test fixture

```python
def test_dose_response_roundtrip(tmp_path):
    from summarycodec.objects import make
    from summarycodec.core.codec import encode
    from summarycodec.validators import validate
    from summarycodec.core import Level, Status
    obj = make("dose_response",
               {"doses": [0, 10, 50, 100],
                "n": [50] * 4, "events": [2, 8, 25, 41]})
    p = str(tmp_path / "dr.png")
    encode(obj, "png", Level.L4, p)
    assert validate(p).status == Status.VALID
```

## 10. Failure condition

A class that mis-implements `displayed()` (e.g. returns unrounded floats)
fails `semantic_equivalence` → `SEMANTIC_MISMATCH` on its *own* valid
output — the contract is enforced on the author, not only on adversaries.
A class promising L3 without executable queries fails
`secondary_queries_executable` → `LEVEL_NOT_SATISFIED`.

## Checklist for a production class

- [ ] `analyze()` deterministic on canonical-JSON inputs (iterate sorted
      keys — canonical JSON re-sorts)
- [ ] `displayed()` covers every visible number
- [ ] `secondary_queries()` = the *prespecified* reuse family (all must
      run on payload data alone)
- [ ] `canonical_dataset()` fully determines `analyze()`
- [ ] registered in REGISTRY + schema enum + spec docs
- [ ] round-trip + adversarial tests
