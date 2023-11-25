from transformers import AutoModelForSeq2SeqLM, T5TokenizerFast
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer
import torch
from enum import Enum


class ModelType(Enum):
    T5_MODEL = 1
    M2M100_MODEL = 2


class SpellCorrector():
    def __init__(self, model_name, device="cpu", max_time=3600):
        self.device = device
        self.max_time = max_time
        if 'm2m100' in model_name.lower():
            self.model_type = ModelType.M2M100_MODEL
            self.model = M2M100ForConditionalGeneration.from_pretrained(
                model_name,
                device_map=device
            )
            self.tokenizer = M2M100Tokenizer.from_pretrained(
                model_name,
                src_lang="ru",
                tgt_lang="ru",
                device_map=device
            )
        elif 't5' in model_name.lower():
            self.model_type = ModelType.T5_MODEL
            self.tokenizer = T5TokenizerFast.from_pretrained(
                model_name,
                device_map=device
            )
            self.model = AutoModelForSeq2SeqLM.from_pretrained(
                model_name,
                device_map=device
            )
        else:
            raise RuntimeError('Unknown model')

    def __predict_m2m100__(self, input_seq):
        encodings = self.tokenizer(input_seq, return_tensors="pt")
        generated_tokens = self.model.generate(
                **encodings.to(torch.device(self.device)),
                forced_bos_token_id=self.tokenizer.get_lang_id("ru"))
        answer = self.tokenizer.batch_decode(generated_tokens,
                                             skip_special_tokens=True)
        return answer[0]

    def __predict_t5__(self, input_seq):
        task_prefix = "Spell correct: "
        encoded = self.tokenizer(
            [task_prefix + input_seq],
            padding="longest",
            max_length=1024,
            truncation=True,
            return_tensors="pt"
        )
        result = self.tokenizer.batch_decode(
                    self.model.generate(
                        **encoded.to(torch.device(self.device)),
                        max_new_tokens=2048,
                    ),
                    skip_special_tokens=True
                )
        return result[0]

    def predict(self, input_seq):
        if self.model_type == ModelType.T5_MODEL:
            return self.__predict_t5__(input_seq)
        else:
            return self.__predict_m2m100__(input_seq)