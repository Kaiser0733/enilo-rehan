import os, modal

app = modal.App("enilo-rehan")
img = (modal.Image.from_registry("nvidia/cuda:12.4.1-devel-ubuntu22.04", add_python="3.12")
       .apt_install("git","cmake","build-essential","wget","ca-certificates","curl")
       .run_commands(
         "git clone --depth 1 https://github.com/ggml-org/llama.cpp /opt/lc",
         "cd /opt/lc && cmake -B build -DGGML_CUDA=ON -DLLAMA_BUILD_TESTS=OFF -DCMAKE_BUILD_TYPE=Release",
         "cd /opt/lc && cmake --build build --target llama-server -j8")
       .pip_install("fastapi[standard]","huggingface_hub"))
vol = modal.Volume.from_name("enilo-models", create_if_missing=True)

def prep():
    dst="/cache/enilo-q4_k_m.gguf"
    if not (os.path.exists(dst) and os.path.getsize(dst)>2_000_000_000):
        from huggingface_hub import hf_hub_download
        import shutil
        p=hf_hub_download("Kaiser0733/enilo-rehan-4b","enilo-q4_k_m.gguf",cache_dir="/cache")
        shutil.copy(p,dst)
    return dst

@app.function(image=img,gpu="T4",volumes={"/cache":vol},timeout=900,
              secrets=[modal.Secret.from_name("enilo-hf")],max_containers=1,
              scaledown_window=900)
@modal.fastapi_endpoint(method="POST")
def chat(req:dict):
    import subprocess,time,httpx,urllib.request
    # ensure server up (starts once per container)
    global _srv_up
    try:
        urllib.request.urlopen("http://127.0.0.1:8080/health",timeout=2)
    except Exception:
        dst=prep()
        subprocess.Popen(["/opt/lc/build/bin/llama-server","-m",dst,
                          "--host","127.0.0.1","--port","8080",
                          "-c","4096","-ngl","99"])
        for _ in range(120):
            time.sleep(2)
            try:
                urllib.request.urlopen("http://127.0.0.1:8080/health",timeout=2); break
            except Exception: pass
    r=httpx.post("http://127.0.0.1:8080/v1/chat/completions",json=req,timeout=600)
    return r.json()
