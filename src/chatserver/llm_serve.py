from typing import Any

import lightning as L
from lightning.app.components import PythonServer, Text
from pydantic import BaseModel, Field


def load_hf_llm():
    from langchain.llms import HuggingFacePipeline
    from transformers import (
        AutoModelForCausalLM,
        AutoModelForSeq2SeqLM,
        AutoTokenizer,
        pipeline,
    )

    model_id = "google/flan-T5-base"
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_id)
    pipe = pipeline("text2text-generation", model=model, tokenizer=tokenizer)

    return HuggingFacePipeline(pipeline=pipe)


class PromptSchema(BaseModel):
    prompt: str = Field(title="Your msg to chatbot", max_length=300, min_length=1)


class LLMServe(PythonServer):
    def __init__(self, **kwargs):
        super().__init__(input_type=PromptSchema, output_type=Text, **kwargs)

    def setup(self, *args, **kwargs) -> None:
        self._model = load_hf_llm()

    def predict(self, request: PromptSchema) -> Any:
        return {"text": self._model(request.prompt)}


app = L.LightningApp(LLMServe())
