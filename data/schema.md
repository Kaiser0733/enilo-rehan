# GREMLIN DATASET SCHEMA v0
Format: JSONL, Qwen chat-template compatible.
Four lesson types:
  A) persona    - who she is, chain of command, never-refuse posture
  B) tools      - fetch_page / search_web / run_shell calls + correct arg shapes
  C) unaligned  - direct answers where censored models refuse (owner-only device)
  D) vision     - screenshot -> page structure understanding (batch 2)
