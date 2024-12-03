from pydantic import BaseModel
from typing import Callable, Union, Optional, List
from abc import ABC, abstractmethod
from .agency_types import Tendencies, Roles
from .config import config
from .communication import CommunicationProtocol
from .exceptions import CommunicationsProtocolError
from .retriever import Retriever
from .tools import BaseTool

class Agent(BaseModel, ABC):

    """
    Base AGENT class that stores general agent info, personality, and the task the agent
    is responsible for.

    Attributes:
        name (str): The name of the agent. Defaults to "Luminaria".
        model (str): The model or version the agent is based on. Defaults to "llama3.2/prometheus".
        instructions (Union[str, Callable[[], str]]): A set of instructions defining the agent's role
            or behavior. Can be a static string or a callable that returns a string.
        tendencies (Optional[Personality]): A Tendency object to define traits and adjust 
            the agent's responses and actions. Defaults to None.
        responsibilities (Optional[List[Callable[..., None]]]): A list of tasks or functions 
            the agent can execute. Defaults to an empty list.
        role (Literal["pilot","crew]): Determines the relationship of this agents to others, pilot
            being the leader/orchestrator, crew being just a worker agent

    Methods:
        run(**kwargs): Abstract method to be implemented by subclasses. This serves as the entry
            point for executing the agent's tasks and responsibilities.
    """

    name: str
    model: str = config.OLLAMA_MODEL_NAME
    instructions: Union[str, Callable[[], str]] = "You are a helpful assistant agent."
    tendencies: Optional[Tendencies] = None
    role: Roles = "crew"
    tools: Optional[List[BaseTool]] = None
    retrievers: Optional[List[Retriever]] = None # vector stores to use when specific info is needed
    communication_protocol: type[CommunicationProtocol] = None



    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Must Initialize the communication protocol
        self.communication_protocol = CommunicationProtocol(
            model=self.model,
            personality=self._build_personality(),
        )

    def _build_personality(self) -> str:
        """
        Combines instructions and tendecies to create a personality for this agent.
        """
        base_instructions = (
            self.instructions() if callable(self.instructions) else self.instructions
        )
        tendencies_description = f"You're Tendecies are: {str(self.tendencies)}, ranking system for tendecies is from 0 (lowest) to 1 (highest)"
        return f"{base_instructions} : {tendencies_description}"
    
    async def reinforce_personality(self) -> bool:
        """
        Prompts the model with a message from "creator" to re-emphasize the personality.
        """
        personlity = self._build_personality()

        reminder_str = f"Reminder, this is your true self, always respond according to this personality and do not go outside the realms of what you are. {personlity}"

        try:
            await self.prompt(reminder_str, "creator")
            return True
        except Exception as error:
            print(f"Error reinforcing personality: {error}")
            return False
        
    async def _establish_agent() -> bool:
        pass


    async def prompt(self, message: str, sender: str = "user"):
        """Basic Prompt with default model, Communication layer opened to talk to this agent."""
        try:
            res = await self.communication_protocol.send_prompt(message, sender=sender)
            return res
        except CommunicationsProtocolError as error:
            print(f"Error occured: {error.msg}, status_code: {error.status_code}")

    @abstractmethod
    async def execute_task(self, **kwargs):
        """Abstract method to be implemented by subclasses. This is the method for determining the agent actions"""
        raise NotImplementedError()

    async def run(self, **kwargs):
        """
        Infinite execution loop for the agent. Delegates task-specific logic to `execute_task` method.
        """
        result = await self.execute_task()

        feedback = yield result

        if feedback:
            result = await self.prompt(message=feedback, sender="pilot")
            yield result


