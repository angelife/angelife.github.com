# Model Evaluation Notes

## NousResearch/Nous-Hermes-2-Vision-Alpha — NOT NEEDED

**Evaluated:** 2026-05-30

**Why not needed:**
- Architecture: LLaVA (Mistral-7B base) — LLaVA architecture from 2023
- Parameters: 7B (we have 11B)
- Created: 2023-11-28
- Downloads: 845
- Pipeline: text-generation (no native vision endpoint on NVIDIA API)

**Our current solution:**
- `meta/llama-3.2-11b-vision-instruct` on NVIDIA Integrate API
- 11B parameters, native vision support, better than Mistral-7B + LLaVA
- Already working at `/opt/data/vision_client.py`

**Verdict:** Skip. We outperform it with what we already have.