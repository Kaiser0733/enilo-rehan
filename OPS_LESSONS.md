# ENILO NIGHT-OPS BATTLE LESSONS
Every failure class from the ENILO-rehan build, with verified fixes.
Read before touching Kaggle / HF / training pipelines. Written 2026-08-23.

## KAGGLE GPU LOTTERY
- kaggle kernels push via API defaults to P100 (sm_60) regardless of past UI settings.
- Fix A: new CLI supports: kaggle kernels push --accelerator nvidiaTeslaT4
- Fix B: open kernel in browser, Edit, Notebook options, Accelerator, pick GPU T4 x2, then Save Version and Run All. UI runs respect your selection; API pushes may not.
- P100 is dead weight: modern torch dropped sm_60, so any CUDA op dies with AcceleratorError: no kernel image is available. bf16 does not exist on Pascal either.
- If trapped on P100 anyway: torch==2.1.2 cu121 + fp16 everywhere + eager attention + loss_type nll can limp through. T4 is the real answer.
- Note: Kaggle sunsets P100 on Sept 15, 2026.

## TRANSFORMERS VERSION GATES
- Before choosing any base model, fetch its config.json and check the model_type value against the CONFIG_MAPPING of YOUR installed transformers. Fresh arches (qwen3_5, qwen3_next etc.) are often missing even in latest releases because distillers used internal builds.
- Symptom: KeyError qwen3_5 at AutoConfig. That base is unusable in stock transformers. Pick another base (DreamFast/qwen3-4b-heretic worked for us: model_type qwen3).
- Upgrading transformers: always pip install -U --no-deps transformers, or pip drags a torch build that breaks your GPU.

## SILENT PIP FAILURES
- Never combine -q with check=False. Capture returncode, print stdout and stderr tails, then verify versions via pip show or a version print after import. We lost hours to upgrades that silently did not apply.

## TRL v1.10 TRAINING PATTERNS (docs-verified)
- Use SFTConfig, not TrainingArguments.
- Qwen lineage: set eos_token to the im_end marker in SFTConfig or responses never terminate.
- Pass peft_config=LoraConfig(...) directly into SFTTrainer; no manual get_peft_model needed.
- The tokenizer param is processing_class=tok now, not tokenizer=.
- On pre-Turing GPUs: loss_type nll (default chunked_nll may hit unsupported triton kernels), fp16=True, bf16=False.
- Recent peft requires torchao 0.16+; preinstalled torchao on Kaggle is older: pip install -U torchao.
- Conversational datasets: assistant messages must have string content. Normalize tool_calls into plain text like tool_call name equals fetch_page plus args, otherwise Jinja chat templates crash with: Can only get item pairs from a mapping.

## CHAT TEMPLATE TRAPS
- apply_chat_template in new transformers returns a BatchEncoding dict, not a tensor. Unpack with ** when calling the model; index input_ids for decoding offsets.
- When loading for generation: pass add_generation_prompt=True, return_tensors=pt, return_dict=True.

## MODAL 2026 API DRIFTS
- web_endpoint is renamed fastapi_endpoint.
- allow_concurrent_inputs is replaced by max_containers=N on app.cls, or the modal.concurrent decorator (correct placement matters).
- fastapi must be installed explicitly in the image: pip_install fastapi[standard].
- Class-based endpoints mount at /ClassName/method — plain functions mount at /.
- Free credits die mid-build on heavy CUDA compiles; budget before choosing a CUDA devel base image.

## HOSTING REALITY (Aug 2026)
- HF Spaces: docker and gradio tiers now need PRO (402 on free create). Static Spaces still free.
- Modal free credits: 30 dollars per month cycle; heavy CUDA image builds can burn it all in one deploy.
- Kaggle: cannot host persistent endpoints. Good for batch training/quantize/upload only.
- Working relay pattern: train on Kaggle GPU, quantize in a second kernel attaching the first as kernel_source, upload to HF via huggingface_hub inside a third kernel. Zero local bandwidth used.

## BASE MODEL VETTING CHECKLIST
1. config.json model_type exists in your transformers CONFIG_MAPPING?
2. Safetensors present (not GGUF-only)?
3. License usable (apache-2.0 ideal)?
4. Text-only vs VL (VL needs processor classes even for text tasks)?
5. Custom code files needed? Avoid if possible.
6. Already heretic/abliterated? Then skip your own ablation stage.

## LLAMA.CPP ON DEVICE NOTES
- Termux TUR repo ships prebuilt llama-cpp: pkg install llama-cpp. Reads /sdcard natively.
- proot builds fail when termux cmake leaks into PATH (android api-level.h hunt). Use container-own /usr/bin/cmake.
- Recent llama.cpp renamed CLI target: build target is llama-app or llama; binary family includes llama-server, llama-mtmd-cli.
- 2B Q4_K_M runs fine on 8GB tablet; 4B Q4_K_M does not (OOM). Match model size to device RAM honestly.


## TABLET LOCAL-SERVING LESSON (the one we earned tonight)
- mmap streaming does keep RSS small, but don't expect a 4B Q4 model on an 8GB Android tablet mid-life. Real-world: KV q8 cache + RAM overhead means budget ~3-3.5GB available minimum — and our tablet rests around 2-3GB with Android + Chrome breathing.
- Weights scale by ~1 byte/token-period at higher quality; when in doubt use the 2B sibling — Q4_K_M fits about 1.1GB and delivers immediate utility.
- Downloaded weights validate via GGUF magic bytes + tensors count, never trust filename-only size heuristics.
