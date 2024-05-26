import os

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from openai import OpenAI

from agentlite.llm.LLMConfig import LLMConfig

OPENAI_CHAT_MODELS = [
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-16k-0613",
    "gpt-3.5-turbo-16k",
    "gpt-4",
    "gpt-4-0613",
    "gpt-4-turbo",
    "gpt-4-32k",
    "gpt-4-32k-0613",
    "gpt-4-1106-preview",
]
OPENAI_LLM_MODELS = ["text-davinci-003", "text-ada-001"]


class BaseLLM:
    def __init__(self, llm_config: LLMConfig) -> None:
        self.llm_name = llm_config.llm_name
        self.context_len: int = llm_config.context_len
        self.stop: list = llm_config.stop
        self.max_tokens: int = llm_config.max_tokens
        self.temperature: float = llm_config.temperature
        self.end_of_prompt: str = llm_config.end_of_prompt

    def __call__(self, prompt: str) -> str:
        return self.run(prompt)

    def run(self, prompt: str):
        # return str
        raise NotImplementedError


class OpenAIChatLLM(BaseLLM):
    def __init__(self, llm_config: LLMConfig):
        super().__init__(llm_config=llm_config)
        self.client = OpenAI(api_key=llm_config.api_key)

    def run(self, prompt: str):
        response = self.client.chat.completions.create(
            model=self.llm_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
        )
        return response.choices[0].message.content


class MSChatLLM(BaseLLM):
    def __init__(self, llm_config: LLMConfig):
        super().__init__(llm_config=llm_config)
        self.api_key = llm_config.api_key
        self.base_url = llm_config.base_url
        self.en_prompt = llm_config.en_prompt
        self.client = OpenAI(api_key=self.api_key,
                             base_url=self.base_url)

    def run(self, prompt: str, system_prompt: str = ""):
        if len(system_prompt) == 0:
            if self.en_prompt:
                system_prompt = "You are a helpful assistant."
            else:
                system_prompt = "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"
        
        response = self.client.chat.completions.create(
            model=self.llm_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            temperature=self.temperature,
        )
        return response.choices[0].message.content


class LangchainLLM(BaseLLM):
    def __init__(self, llm_config: LLMConfig):
        from langchain_openai import OpenAI

        super().__init__(llm_config)
        llm = OpenAI(
            model_name=self.llm_name,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            base_url=llm_config.base_url,
            api_key=llm_config.api_key,
        )
        human_template = "{prompt}"
        prompt = PromptTemplate(template=human_template, input_variables=["prompt"])
        self.llm_chain = LLMChain(prompt=prompt, llm=llm)

    def run(self, prompt: str):
        return self.llm_chain.run(prompt)


class LangchainChatModel(BaseLLM):
    def __init__(self, llm_config: LLMConfig):
        from langchain_openai import ChatOpenAI

        super().__init__(llm_config)
        llm = ChatOpenAI(
            model_name=self.llm_name,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            base_url=llm_config.base_url,
            api_key=llm_config.api_key,
        )
        human_template = "{prompt}"
        prompt = PromptTemplate(template=human_template, input_variables=["prompt"])
        self.llm_chain = LLMChain(prompt=prompt, llm=llm)

    def run(self, prompt: str):
        return self.llm_chain.run(prompt)


def get_llm_backend(llm_config: LLMConfig):
    llm_name = llm_config.llm_name

    if llm_name in OPENAI_CHAT_MODELS:
        return LangchainChatModel(llm_config)
    elif llm_name in OPENAI_LLM_MODELS:
        return LangchainLLM(llm_config)
    else:
        return LangchainLLM(llm_config)
