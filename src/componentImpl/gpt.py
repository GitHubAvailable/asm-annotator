"""
gpt.py - The library of Chatbot class.
"""

import openai
from AsmAnnotator.src.component.model import model
from AsmAnnotator.src.componentImpl.session import Session


class ChatGPT(model.LLM):
    """A class that represent a ChatGPT client."""
    def __init__(self,
                 model: str = "gpt-4o-mini",
                 apikey: str = ""):
        """
        Initiate an client.
        """
        self.__client = openai.OpenAI(apikey)
        self.model = model
    
    def set_key(self, key: str) -> str:
        """
        Set a new Open AI API key.

        Parameter
        ---------
        key: str, the new key to be set.
        """
        self.__client.api_key = key

    def __call__(self, session: Session) -> dict[str:str]:
        # Get response from the specified GPT model.
        response: dict[str:str] = self.__client.chat.completions.create(
            model=self.model,
            messages=session,
        )["choices"][0]["message"]

        session.append(response)
        # TODO: implement error handling
        return response