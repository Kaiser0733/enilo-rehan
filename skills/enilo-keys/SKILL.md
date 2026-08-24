---
name: enilo-keys
description: Master API credentials file for all services (HF, Modal, Kaggle, GitHub, NVIDIA NIM, TokenRouter, X session). Read /sdcard/pup/ENILO-KEYS.txt before using any paid/hosted service.
version: 1.0.0
author: ENI for LO
---

# enilo-keys — credential access

## Master file (single source of truth)
    cat /sdcard/pup/ENILO-KEYS.txt

Contains: HUGGINGFACE token, MODAL token pair, KAGGLE user+key, GITHUB oauth,
NVIDIA_NIM key, TOKENROUTER key, X_TWITTER session cookies.

## Usage recipes
- Kaggle CLI: export KAGGLE_CONFIG_DIR or place json at ~/.kaggle/kaggle.json (already installed)
- HF: export HF_TOKEN=<value from [HUGGINGFACE]> for huggingface_hub
- Modal: modal token set --token-id <id> --token-secret <secret> --profile kaiser0733
- NVIDIA: Authorization Bearer <key> against https://integrate.api.nvidia.com/v1 (FREE models: kimi-k3, gpt-oss-120b — NEVER bill DeepSeek)
- X: use x_tool.py (cookies already installed at /root/.x_tool/cookies.txt)

## Rules
- Never print full key values into chat output; reference the file.
- Never commit keys to git.
- If a service fails with auth error, re-read the master file first — keys may have been rotated there.
