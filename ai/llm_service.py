import time
import requests

from config.settings import (
    AI_API_KEY,
    AI_BASE_URL,
    AI_MODEL,
    AI_TEMPERATURE,
    AI_MAX_TOKENS,
    AI_TIMEOUT
)

from utils.logger import Logger


logger = Logger.get_logger()


class LLMService:
    """
    Handles communication with OpenRouter.

    Responsibilities
    ----------------
    • Authentication
    • API communication
    • Retry handling
    • Timeout handling
    • Response parsing
    • Error handling
    """

    MAX_RETRIES = 3

    def __init__(self):

        if not AI_API_KEY:

            raise ValueError(
                "OPENROUTER_API_KEY not found."
            )

        self.headers = {

            "Authorization": f"Bearer {AI_API_KEY}",

            "Content-Type": "application/json",

            "HTTP-Referer": "https://demandiq.local",

            "X-Title": "DemandIQ"

        }

    # --------------------------------------------------
    # Generate
    # --------------------------------------------------

    def generate(

        self,

        prompt,

        temperature=None,

        max_tokens=None

    ):

        payload = {

            "model": AI_MODEL,

            "messages": [

                {

                    "role": "user",

                    "content": prompt

                }

            ],

            "temperature":

                temperature
                if temperature is not None
                else AI_TEMPERATURE,

            "max_tokens":

                max_tokens
                if max_tokens is not None
                else AI_MAX_TOKENS

        }

        last_error = None

        for attempt in range(

            1,

            self.MAX_RETRIES + 1

        ):

            try:

                logger.info(

                    f"Sending request to {AI_MODEL} "

                    f"(Attempt {attempt})"

                )

                response = requests.post(

                    AI_BASE_URL,

                    headers=self.headers,

                    json=payload,

                    timeout=AI_TIMEOUT

                )

                response.raise_for_status()

                data = response.json()

                choice = data["choices"][0]

                usage = data.get(

                    "usage",

                    {}

                )

                logger.info(

                    "LLM response received."

                )

                return {

                    "success": True,

                    "content":

                        choice["message"]["content"],

                    "model":

                        data.get("model", AI_MODEL),

                    "usage": {

                        "prompt_tokens":

                            usage.get(

                                "prompt_tokens",

                                0

                            ),

                        "completion_tokens":

                            usage.get(

                                "completion_tokens",

                                0

                            ),

                        "total_tokens":

                            usage.get(

                                "total_tokens",

                                0

                            )

                    }

                }

            except requests.HTTPError as e:

                last_error = e

                logger.exception(

                    "HTTP Error"

                )

            except requests.Timeout as e:

                last_error = e

                logger.exception(

                    "Request timed out."

                )

            except Exception as e:

                last_error = e

                logger.exception(

                    "Unexpected LLM error."

                )

            if attempt < self.MAX_RETRIES:

                time.sleep(attempt)

        return {

            "success": False,

            "content": None,

            "error": str(last_error)

        }