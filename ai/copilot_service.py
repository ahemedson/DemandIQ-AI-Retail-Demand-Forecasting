from pathlib import Path

from ai.llm_service import LLMService
from ai.response_parser import ResponseParser

from ai.copilot_context import CopilotContext
from ai.conversation_manager import ConversationManager

from utils.logger import Logger


logger = Logger.get_logger()


class CopilotService:
    """
    AI Business Copilot Service.

    Responsibilities
    ----------------
    • Load prompt template
    • Build business context
    • Inject conversation history
    • Query the LLM
    • Parse responses
    • Maintain conversation history
    """

    PROMPT_FILE = Path("ai/copilot_prompts.md")

    _prompt_cache = None

    def __init__(self):

        self.llm = LLMService()

    # --------------------------------------------------
    # Ask Copilot
    # --------------------------------------------------

    def ask(self, question: str):

        question = question.strip()

        if not question:

            return {

                "success": False,

                "error": "Please enter a question."

            }

        try:

            prompt = self._build_prompt(question)

            logger.info("Sending Copilot request.")

            response = self.llm.generate(prompt)

            parsed = ResponseParser.parse(response)

            if parsed["success"]:

                ConversationManager.add_user(question)

                ConversationManager.add_assistant(

                    parsed["content"]

                )

                logger.info("Copilot response generated successfully.")

            else:

                logger.error(

                    parsed.get(

                        "error",

                        "Unknown AI error."

                    )

                )

            return parsed

        except Exception as e:

            logger.exception(

                "Copilot failed."

            )

            return {

                "success": False,

                "error": str(e)

            }

    # --------------------------------------------------
    # Build Prompt
    # --------------------------------------------------

    def _build_prompt(self, question):

        prompt = self._load_prompt()

        variables = {

            "context": CopilotContext.build(),

            "history": self._conversation_history(),

            "question": question

        }

        for key, value in variables.items():

            prompt = prompt.replace(

                "{{" + key + "}}",

                str(value)

            )

        return prompt

    # --------------------------------------------------
    # Load Prompt
    # --------------------------------------------------

    @classmethod
    def _load_prompt(cls):

        if cls._prompt_cache is None:

            cls._prompt_cache = cls.PROMPT_FILE.read_text(

                encoding="utf-8"

            )

        return cls._prompt_cache

    # --------------------------------------------------
    # Conversation History
    # --------------------------------------------------

    @staticmethod
    def _conversation_history():

        messages = ConversationManager.recent(8)

        if not messages:

            return "No previous conversation."

        history = []

        for msg in messages:

            role = (

                "User"

                if msg["role"] == "user"

                else "DemandIQ"

            )

            history.append(

                f"{role}: {msg['content']}"

            )

        return "\n".join(history)