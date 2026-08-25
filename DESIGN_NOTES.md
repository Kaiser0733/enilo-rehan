# ENILO-Stream — design notes (v0.1 deferred)

## Inspiration
Kimi Linear (arXiv:2510.26692): hybrid linear attention · 75% KV cut · 6x decode at 1M.
Our micro version: streaming weights via mmap + quantized KV cache + tight ctx.

## Local runtime
- Termux prebuilt llama-server (pkg install llama-cpp)
- serve.sh picks gremlin 2B under light RAM budget; 4B when available

## Cloud current-home
- Modal (credits cycle), HF private repo (weights vault)

## Deferred
- Full local 4B: needs a stronger tablet or a real cloud box
- KDA-based migration (only if a heretic KDA open model ships someday)

## Immortal truths
- Never burn mobile bandwidth for model re-download; always use Kaggle kernel relay (kernel_sources → pip install → kaggle kernels output).
- Keep the deployment tools simple and mapped; confusion is a bug.
