# Summary Codec — reproducibility bundle

Third-party verification path (no author contact required).

## Install

```bash
cd 02_SOFTWARE
pip install -r requirements.txt   # pinned versions
pip install -e .                  # or: PYTHONPATH=. for the commands below
```

`requirements.txt` is pinned. Python >= 3.10.

## Independent verification of the published objects

```bash
# per object
summarycodec verify ../04_PHASE2/biomedical_objects/gbsg2_km_horth.svg
summarycodec inspect ../04_PHASE2/biomedical_objects/gbsg2_km_horth.svg
summarycodec decode  ../04_PHASE2/biomedical_objects/gbsg2_km_horth.svg --out payload.json
summarycodec reanalyze ../04_PHASE2/biomedical_objects/gbsg2_km_horth.svg \
    --query survival_at --args '[1000]'

# batch: verify + decode + reproduce + reanalyze everything
python3 ../04_PHASE2/independent_reproduction/reproduce.py
```

## Reproduce Phase 1

```bash
python3 ../03_PHASE1/synthetic_data/make_synthetic.py
python3 ../03_PHASE1/run_phase1.py     # regenerates all result CSVs
python3 -m pytest ../02_SOFTWARE/tests -q   # 86 tests
```

## Post-publication reanalysis demo

```bash
python3 ../04_PHASE2/reanalysis_demo/run_reanalysis.py
```

## Manipulation suite

```bash
python3 ../04_PHASE2/manipulation_tests/run_manipulation.py
```

## Data provenance

`04_PHASE2/datasets/raw/acquisition_ledger.json` — source, sha256, UTC,
license for each frozen dataset (GBSG2, WDBC, Efron diabetes).
