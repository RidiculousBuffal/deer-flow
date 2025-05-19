# Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
# SPDX-License-Identifier: MIT
import os
from typing import Any, Dict

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, AzureChatOpenAI

from src.config.agents import LLMType

load_dotenv()
# Cache for LLM instances
_llm_cache: dict[LLMType, ChatOpenAI] = {}


def _create_llm_use_conf(llm_type: LLMType, conf: Dict[str, Any]) -> ChatOpenAI | AzureChatOpenAI:
    llm_type_map = {
        "reasoning": conf.get("REASONING_MODEL"),
        "basic": conf.get("BASIC_MODEL"),
        "vision": conf.get("VISION_MODEL"),
    }
    llm_conf = llm_type_map.get(llm_type)
    if not llm_conf:
        raise ValueError(f"Unknown LLM type: {llm_type}")
    if not isinstance(llm_conf, dict):
        raise ValueError(f"Invalid LLM Conf: {llm_type}")
    if os.getenv('LLM_TYPE') == 'azure':
        return AzureChatOpenAI(**llm_conf)
    else:
        return ChatOpenAI(**llm_conf)


def get_llm_by_type(
        llm_type: LLMType,
) -> ChatOpenAI | AzureChatOpenAI:
    AZURE_DEPLOYMENT = os.getenv('AZURE_DEPLOYMENT')
    AZURE_ENDPOINT = os.getenv('AZURE_ENDPOINT')
    API_VERSION = os.getenv('API_VERSION')
    API_KEY = os.getenv('API_KEY')
    return AzureChatOpenAI(api_key=API_KEY, api_version=API_VERSION, azure_endpoint=AZURE_ENDPOINT,
                           azure_deployment=AZURE_DEPLOYMENT)


# Initialize LLMs for different purposes - now these will be cached
basic_llm = get_llm_by_type("basic")

# In the future, we will use reasoning_llm and vl_llm for different purposes
# reasoning_llm = get_llm_by_type("reasoning")
# vl_llm = get_llm_by_type("vision")


if __name__ == "__main__":
    print(basic_llm.invoke("Hello"))
