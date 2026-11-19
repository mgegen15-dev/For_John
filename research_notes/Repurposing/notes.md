# Repurposing screen: working notes

*Started November 19, 2026. Working notes behind `reports/Approved drugs worth testing in osteosarcoma.md`. Script: `tools/repurposing_screen.py`. Output: `data/osteosarcoma_repurposing_candidates.csv`. Raw pulls cached (git-ignored) in `data/repurposing_raw/`.*

Every candidate below is a hypothesis for laboratory testing, not a treatment recommendation, and nothing here is medical advice.

## 1. Data pulled

- **ChEMBL REST API**, November 19, 2026: 4,225 molecule records with max_phase 4 and 1,892 with max_phase 3 (salts and parents counted separately), and all 7,561 mechanism-of-action records, with the 1,518 targets they name (registry). Raw JSON: `chembl_molecules_phase4.json`, `chembl_molecules_phase3.json`, `chembl_mechanisms.json`, `chembl_targets.json`.
- Kept: mechanisms with max_phase 3 or 4 acting on a human protein target. Dropped: vaccines, replacement enzymes, collagen- or clot-digesting enzymes, fusion-protein targets (ChEMBL lists repotrectinib against "CD74-ROS1", which would credit CD74), and imaging agents.
- **Caveat found while building**: ChEMBL's `therapeutic_flag` is False for every phase 3 molecule, so it can only be used to remove diagnostics among approved drugs. ChEMBL also lags recent approvals: defactinib still reads max_phase 3 although the FDA granted accelerated approval on May 8, 2025 (registry).
- Mutant-selective drugs (a mechanism with a variant sequence, or sotorasib/adagrasib/ivosidenib/vorasidenib-type names) are not credited to the wild-type gene. Osteosarcoma rarely carries those mutations.
