import time
from transformers import AutoModelForCausalLM, AutoTokenizer

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
    device = "cuda:0"

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
