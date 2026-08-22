import json
def code(s): return {"cell_type":"code","execution_count":None,"metadata":{},"outputs":[],"source":s.splitlines(True)}
c1='''import os
# find merged model produced by train kernel (attached as kernel source)
src=None
for r,d,f in os.walk("/kaggle/input"):
    if any(x.endswith(".safetensors") for x in f):
        pr=[x for x in f if x.startswith("model")][0]
        src=os.path.join(r); break
print("src:",src)'''
c2='''import subprocess
subprocess.run(["git","clone","--depth","1","https://github.com/ggml-org/llama.cpp","/tmp/lc"],check=False)
subprocess.run(["pip","install","-q","gguf","sentencepiece","protobuf"],check=False)
r=subprocess.run(["python3","/tmp/lc/convert_hf_to_gguf.py",src,"--outfile","/kaggle/working/enilo-f16.gguf","--outtype","f16"],capture_output=True,text=True)
print("rc",r.returncode);print(r.stdout[-400:]);print(r.stderr[-400:])'''
c3='''import os,subprocess
os.chdir("/tmp/lc")
subprocess.run(["cmake","-B","build","-DGGML_NATIVE=ON"],check=False)
subprocess.run(["cmake","--build","build","--target","llama-quantize","-j","4"],check=False)
q=subprocess.run(["./build/bin/llama-quantize","/kaggle/working/enilo-f16.gguf","/kaggle/working/enilo-q4_k_m.gguf","Q4_K_M"],capture_output=True,text=True)
print(q.stdout[-300:]);print(q.stderr[-200:])
for f in os.listdir("/kaggle/working"):
    pth=os.path.join("/kaggle/working",f)
    if os.path.isfile(pth): print(f, round(os.path.getsize(pth)/1e9,2),"GB")'''
cells=[code(x) for x in (c1,c2,c3)]
nb={"cells":cells,"metadata":{"kernelspec":{"display_name":"Python 3","language":"python","name":"python3"},"language_info":"python"},"nbformat":4,"nbformat_minor":4}
json.dump(nb,open("quantize-enilo.ipynb","w"),indent=1)
meta={"id":"kaiser0733/enilo-quantize-v1","title":"enilo-quantize-v1","code_file":"quantize-enilo.ipynb","language":"python","kernel_type":"notebook","is_private":True,"enable_gpu":False,"enable_internet":True,"dataset_sources":[],"competition_sources":[],"kernel_sources":["kaiser0733/gremlin-train-v2"],"model_sources":[]}
json.dump(meta,open("kernel-metadata.json","w"),indent=1)
print("quantize kernel staged — waits for train output as source")
