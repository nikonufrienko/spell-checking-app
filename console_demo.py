from transformers import AutoModelForSeq2SeqLM, T5TokenizerFast
import torch
response = int(input(
'''
    1 -- UrukHan/t5-russian-spell
    2 -- summervent/russian-spellchecking
    3 -- summervent/speller-t5-909_both_
'''
))
if response == 1:
    model_name = 'UrukHan/t5-russian-spell'
elif response == 2:
    model_name = 'summervent/russian-spellchecking'
elif response == 3:
    model_name = 'summervent/speller-t5-909_both_'
else:
    raise RuntimeError('Expected 1, 2 or 3')

tokenizer = T5TokenizerFast.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(torch.device('cuda'))
device = torch.device('cuda')
print('Модель загружена')
def predict(input_sequences):
    task_prefix = "Spell correct: "
    if type(input_sequences) != list: input_sequences = [input_sequences]
    encoded = tokenizer(
    [task_prefix + sequence for sequence in input_sequences],
    padding="longest",
    max_length=1024,
    truncation=True,
    return_tensors="pt",
    )
    return tokenizer.batch_decode(model.generate(**encoded.to(device), max_new_tokens=2048), skip_special_tokens=True)

while True:
    print("Spell correct: %s" % predict(input('Input:'))[0])
