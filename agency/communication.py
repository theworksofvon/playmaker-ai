import os
from typing import Union, Dict, List
import asyncio
import httpx
from .config import config
from .exceptions import CommunicationsProtocolError

class CommunicationProtocol:
    """
    This protocol determines the communication layer between agents. 
    The protocol is model-agnostic and handles both local (e.g., Ollama) 
    and remote models (e.g., OpenAI API), incorporating agent-specific personality 
    and context.
    """

    def __init__(self, model: str,  personality: str = "") -> None:
        """
        Initialize the communication protocol with the specified model.

        Args:
            model (str): The model type (e.g., "ollama", "openai").
            config (Dict): Configuration parameters for the model (e.g., API key, endpoint).
            personality (str): The personality or context of the agent.
        """
        self.model = model.lower()
        self.personality = personality  # Personality of the agent
        self.history: List[Dict[str, str]] = []  # To track the context of the conversation

    async def send_prompt(self, prompt: str, sender: str) -> str:
        """
        Send a prompt to the model, including personality and history, and return the response.
        Mainly for agent -> agent communication.

        Args:
            prompt (str): The input prompt for the model.

        Returns:
            str: The model's response.
        """
        full_prompt = self._build_prompt(prompt, sender)
        print(f"Prompt: {prompt}")
        if self.model == "openai":
            response = await self._send_to_openai(full_prompt)
        else:
            response = await self._send_to_ollama(full_prompt)
        try:
            self._update_history("user", prompt)
            self._update_history("assistant", response)
        except Exception as error:
            error_message = f"Failed to update agent's context history, error: {error}"
            raise CommunicationsProtocolError(error_message, status_code=400)
        return response

    def _build_prompt(self, prompt: str, sender: str) -> str:
        """
        Combine personality, context, and the new prompt into a full query.

        Args:
            prompt (str): The input prompt for the model.

        Returns:
            str: The full prompt including personality and history.
        """
        context = "\n".join([f"{item['role']}: {item['content']}" for item in self.history[-5:]])  # Last 5 interactions
        return f"{self.personality}\n\n{context}\n\nUser - {sender}: {prompt}"

    async def _send_to_ollama(self, prompt: str) -> str:
        """
        Handle communication with a local Ollama model.

        Args:
            prompt (str): The input prompt for the model.

        Returns:
            str: The model's response.
        """
        url = f"{config.OLLAMA_API_URL}/generate"
        async with httpx.AsyncClient() as client:

            try:
                print(prompt)
                res = await client.post(url, json={"prompt": prompt, "stream": False, "model": self.model})
                res.raise_for_status()
                return res.json()["response"]
            except httpx.RequestError as error:
                error_message = (f"Error communicating with Ollama model: {self.model}, error: {error}")
                print(error_message)
                raise CommunicationsProtocolError(error_message, status_code=400)

    async def _send_to_openai(self, prompt: str) -> str:
        """
        Handle communication with the OpenAI API.

        Args:
            prompt (str): The input prompt for the model.

        Returns:
            str: The model's response.
        """
        api_key = self.config.get("openai_api_key", os.getenv("OPENAI_API_KEY"))
        if not api_key:
            raise ValueError("OpenAI API key is missing.")
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {api_key}"},
                json={
                    "model": self.config.get("openai_model", "gpt-4"),
                    "messages": [{"role": "user", "content": prompt}],
                },
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]


    def _update_history(self, role: str, content: str) -> None:
        """
        Update the conversation history.

        Args:
            role (str): The role of the speaker (e.g., "user", "assistant").
            content (str): The content of the message.
        """
        self.history.append({"role": role, "content": content})
        print(self.history)

    def clear_history(self) -> None:
        """
        Clear the conversation history.
        """
        self.history = []

    def test_connection(self) -> bool:
        """
        Test the connection to the configured model endpoint.

        Returns:
            bool: True if the connection is successful, False otherwise.
        """
        try:
            if self.model == "ollama":
                response = httpx.get(self.config.get("ollama_endpoint", "http://localhost:8000/api/version"))
                return response.status_code == 200
            elif self.model == "openai":
                return bool(os.getenv("OPENAI_API_KEY") or self.config.get("openai_api_key"))
            else:
                return False
        except Exception:
            return False