from transformers import AutoModelForSeq2SeqLM, T5TokenizerFast


class SpellCorrector():
    def __init__(self, model_name, device="cpu"):
        self.device = device
        self.tokenizer = T5TokenizerFast.from_pretrained(
            model_name,
            device_map=device
        )
        self.model = AutoModelForSeq2SeqLM.from_pretrained(
            model_name,
            device_map=device
        )

    def predict(self, input_sequences):
        task_prefix = "Spell correct: "
        encoded = self.tokenizer(
            [task_prefix + sequence for sequence in input_sequences],
            padding="longest",
            max_length=1024,
            truncation=True,
            return_tensors="pt",
        )
        result = self.tokenizer.batch_decode(
                    self.model.generate(
                            **encoded.to(self.device),
                            max_new_tokens=2048
                    ),
                    skip_special_tokens=True
                )
        return result
