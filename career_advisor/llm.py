"""LLM access and structured response parsing."""

from __future__ import annotations

import json
import re
from typing import TypeVar

from pydantic import BaseModel

from career_advisor.config import (
    GEMINI_MODEL_NAME,
    HF_MAX_NEW_TOKENS,
    HF_MODEL_ID,
    HF_TEMPERATURE,
    HF_TOP_P,
    HF_USE_4BIT,
    LLM_PROVIDER,
    get_gemini_api_key,
)


T = TypeVar("T", bound=BaseModel)
_gemini_model = None
_hf_model = None
_hf_tokenizer = None


def get_gemini_model():
    global _gemini_model
    if _gemini_model is None:
        import google.generativeai as genai

        api_key = get_gemini_api_key()
        if not api_key:
            raise RuntimeError(
                "Missing Gemini API key. Set GEMINI_API_KEY locally or Gemini_Key in Colab secrets."
            )
        genai.configure(api_key=api_key)
        _gemini_model = genai.GenerativeModel(GEMINI_MODEL_NAME)
    return _gemini_model


def get_hf_model():
    """Load the open-source Hugging Face chat model lazily."""
    global _hf_model, _hf_tokenizer
    if _hf_model is not None and _hf_tokenizer is not None:
        return _hf_model, _hf_tokenizer

    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    _hf_tokenizer = AutoTokenizer.from_pretrained(HF_MODEL_ID)
    model_kwargs = {"trust_remote_code": True}

    if torch.cuda.is_available():
        model_kwargs["device_map"] = "auto"
        if HF_USE_4BIT:
            from transformers import BitsAndBytesConfig

            model_kwargs["quantization_config"] = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.float16,
            )
        else:
            model_kwargs["torch_dtype"] = torch.float16
    else:
        model_kwargs["torch_dtype"] = torch.float32

    _hf_model = AutoModelForCausalLM.from_pretrained(HF_MODEL_ID, **model_kwargs)
    if not torch.cuda.is_available():
        _hf_model.to("cpu")

    return _hf_model, _hf_tokenizer


def llm_run(prompt: str, safety_fallback: str = "(Δεν υπάρχει απάντηση)") -> str:
    try:
        if LLM_PROVIDER == "gemini":
            response = get_gemini_model().generate_content(prompt)
            return getattr(response, "text", None) or safety_fallback
        return hf_generate(prompt)
    except Exception as exc:
        return f"{safety_fallback}\n\n(Σφάλμα: {exc})"


def hf_generate(prompt: str) -> str:
    import torch

    model, tokenizer = get_hf_model()
    system_prompt = (
        "Είσαι ένας βοηθός επαγγελματικού προσανατολισμού. "
        "Απάντα στα ελληνικά, με σαφήνεια, ακρίβεια και πρακτικές συμβουλές."
    )
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt},
    ]

    if hasattr(tokenizer, "apply_chat_template") and tokenizer.chat_template:
        formatted_prompt = tokenizer.apply_chat_template(
            messages,
            add_generation_prompt=True,
            tokenize=False,
        )
    else:
        formatted_prompt = f"{system_prompt}\n\nUser:\n{prompt}\n\nAssistant:\n"

    inputs = tokenizer(formatted_prompt, return_tensors="pt")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    inputs = {key: value.to(device) for key, value in inputs.items()}

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=HF_MAX_NEW_TOKENS,
            do_sample=HF_TEMPERATURE > 0,
            temperature=HF_TEMPERATURE,
            top_p=HF_TOP_P,
            pad_token_id=tokenizer.eos_token_id,
        )

    generated = outputs[0][inputs["input_ids"].shape[-1] :]
    return tokenizer.decode(generated, skip_special_tokens=True).strip()


def llm_run_json(prompt: str, schema: type[T]) -> T:
    """Run an LLM prompt and validate the JSON response with a Pydantic schema."""
    response_text = llm_run(prompt)
    data = _extract_json(response_text)
    return _validate_schema(schema, data)


def schema_instructions(schema: type[BaseModel]) -> str:
    """Return compact JSON schema instructions for prompts."""
    if hasattr(schema, "model_json_schema"):
        schema_dict = schema.model_json_schema()
    else:
        schema_dict = schema.schema()
    return json.dumps(schema_dict, ensure_ascii=False)


def _extract_json(raw_text: str) -> dict:
    cleaned = re.sub(r"```(?:json)?|```", "", raw_text).strip()
    decoder = json.JSONDecoder()

    for index, char in enumerate(cleaned):
        if char != "{":
            continue
        try:
            data, _ = decoder.raw_decode(cleaned[index:])
        except json.JSONDecodeError:
            continue
        if isinstance(data, dict):
            return data

    raise ValueError(f"LLM response did not contain a JSON object: {raw_text[:300]}")


def _validate_schema(schema: type[T], data: dict) -> T:
    if hasattr(schema, "model_validate"):
        return schema.model_validate(data)
    return schema.parse_obj(data)
