import os


class LLMConfig:
    """constructing the llm configuration for running multi-agent system"""

    def __init__(self, config_dict: dict) -> None:
        self.config_dict = config_dict
        self.context_len = config_dict.get("context_len", None)
        self.llm_name = config_dict.get("llm_name", "gpt-3.5-turbo")
        self.temperature = config_dict.get("temperature", 0.9)
        self.stop = config_dict.get("stop", ["\n"])
        self.max_tokens = config_dict.get("max_tokens", 256)
        self.end_of_prompt = config_dict.get("end_of_prompt", "")
        self.api_key: str = config_dict.get("api_key", "EMPTY")
        self.base_url = config_dict.get("base_url", None)
        self.en_prompt = config_dict.get("en_prompt", True)
        self.__dict__.update(config_dict)
