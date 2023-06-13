import time
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import os
os.environ["CUDA_VISIBLE_DEVICES"]="3"

if torch.cuda.is_available():
    print("cuda")
    avail = torch.cuda.device_count()
    print(f'available devices: {avail}')
    print(f'current device: { torch.cuda.current_device()}')
    
    device_num = 1                             # Num of Devices to Use: Randomize this between 1 and number of available devices
    if avail > 1:
        torch.cuda.set_device(device_num)
    curr = torch.cuda.current_device()
    print(f'current device: {curr}')
    t = torch.cuda.get_device_properties(curr).total_memory
    r = torch.cuda.memory_reserved(curr)
    a = torch.cuda.memory_allocated(curr)
    print(f'total: {t}; reserved: {r}; allocated: {a}')
else:
    print("cpu")

device = "cuda" if torch.cuda.is_available() else "cpu"

def guanaco(p=3, text='Hello there!'):
    print(text)
    print('------------------------------------------------------------------------------------------------')
    model_id = f'TheBloke/guanaco-{p}B-HF'
    #model_id = 'stabilityai/stablelm-tuned-alpha-7b'
    #model_id = "tiiuae/falcon-7b"
    tic = time.time()
    model = AutoModelForCausalLM.from_pretrained(model_id, load_in_4bit=True, device_map="auto", trust_remote_code=True)
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    print(model)
#     device = "cuda:0"

    inputs = tokenizer(text, return_tensors="pt").to(device)
    inputs.pop('token_type_ids')
    outputs = model.generate(**inputs, max_new_tokens=512)
    out = tokenizer.decode(outputs[0], skip_special_tokens=True)
    toc = time.time()
    print('------------------------------------------------------------------------------------------------')
    print(out)
    print(f'Runtime: {toc-tic:.2f} seconds' )

    return out

if __name__ == '__main__':
    text = "Explain the self attention mechanism"  
    out = guanaco(p=7, text=text)
    print(out)
