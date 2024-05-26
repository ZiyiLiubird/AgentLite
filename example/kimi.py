import os
from agentlite.llm.agent_llms import MSChatLLM
from agentlite.llm.LLMConfig import LLMConfig

config_dict = {
    "api_key": os.environ.get('MOONSHOT_API_KEY'),
    "base_url": "https://api.moonshot.cn/v1",
    "llm_name": "moonshot-v1-8k",
    "en_prompt": False
}

llm_config = LLMConfig(config_dict=config_dict)

chat = MSChatLLM(llm_config=llm_config)

print(chat.run("介绍一下中国"))