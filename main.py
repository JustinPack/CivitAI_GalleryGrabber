import io,re,os,json,requests,tkinter as tk
from tkinter import filedialog
from PIL import Image
from PIL.PngImagePlugin import PngInfo

r=tk.Tk();r.title("Civitai Image Downloader")
tk.Label(r,text="Enter model hash:").pack();e=tk.Entry(r);e.pack();tk.Label(r,text="Saved Images:").pack();l=tk.Listbox(r);l.pack();tk.Button(r,text="Choose where to download files",command=lambda:filedialog.askdirectory()).pack();tk.Button(r,text="Download",command=lambda:get_metadata(e.get())).pack();save_directory=""

def get_metadata(s):
    u=f"https://civitai.com/api/v1/model-versions/by-hash/{s}"
    r=requests.get(u,headers={"Content-Type":"application/json"});open("response.json","w").write(r.text)
    l.delete(0,tk.END);p=re.compile("https://imagecache.civitai.com/[^.*]+/width=450");u=re.findall(p,r.text)
    return parse_json_metadata(u,r.text)

def parse_json_metadata(u,j):
    d=json.loads(j);i=d.get("images",[]);m=d.get("model",{})
    if not m or not i:return
    global save_directory
    for n,url in enumerate(u):
        img=i[n];model=m.get("name");meta=img.get("meta",{});r=requests.get(url);img_data=io.BytesIO(r.content);img=Image.open(img_data)
        try:filename=f"{model}_{n}_{meta.get('seed','')}.png"
        except AttributeError:filename=f"{model}_{n}_no_meta_.png"
        if save_directory:img_path=os.path.join(save_directory,filename);img.save(img_path,format="PNG")
        else:model_dir=model.replace(' ','_');os.makedirs(model_dir,exist_ok=True);img_path=os.path.join(model_dir,filename);img.save(img_path,format="PNG")
        write_metadata(img_path,meta);l.insert(tk.END,img_path);l.see(tk.END);save_directory=None if n==len(u)-1 else save_directory

def write_metadata(filename,tags):
    image=Image.open(filename)
    if not image:return
    if not tags:return
    prompt,neg_prompt,steps,sampler,cfg_scale,seed,size,model_hash,denoising_strength,hires_upscale,hires_steps,hires_upscaler=[tags.pop(k,None)for k in("prompt","negativePrompt","steps","sampler","cfgScale","seed","Size","Model hash","Denoising strength","Hires upscale","Hires steps","Hires upscaler")]
    metadata_str=f"{prompt}\nNegative prompt: {neg_prompt}\nSteps: {steps}, Sampler: {sampler}, CFG scale: {cfg_scale}, Seed: {seed}, Size: {size}, Model hash: {model_hash}, Denoising strength: {denoising_strength}, Hires upscale: {hires_upscale}, Hires steps: {hires_steps}, Hires upscaler: {hires_upscaler}"
    metadata=PngInfo();metadata.add_text('parameters',metadata_str);image.save(filename,pnginfo=metadata)

r.mainloop()
