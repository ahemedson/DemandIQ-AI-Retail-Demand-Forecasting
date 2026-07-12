from datetime import datetime


class ResponseParser:
    """
    Parses, validates and standardizes LLM responses.
    """

    # --------------------------------------------------
    # Parse Response
    # --------------------------------------------------

    @classmethod
    def parse(cls, response):

        if not response["success"]:

            return {

                "success": False,

                "engine": "AI",

                "content": None,

                "error": response.get(
                    "error",
                    "Unknown AI error."
                ),

                "metadata": {}
            }

        content = cls._clean_markdown(
            response["content"]
        )

        metadata = {

            "model":
                response.get(
                    "model",
                    "Unknown"
                ),

            "generated_at":
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),

            "usage":
                response.get(
                    "usage",
                    {}
                )
        }

        return {

            "success": True,

            "engine": "AI",

            "content": content,

            "metadata": metadata
        }

    # --------------------------------------------------
    # Markdown Cleanup
    # --------------------------------------------------

    @staticmethod
    def _clean_markdown(text):

        if text is None:

            return ""

        text = text.strip()

        if text.startswith("```markdown"):

            text = text.replace(
                "```markdown",
                "",
                1
            )

        if text.startswith("```"):

            text = text.replace(
                "```",
                "",
                1
            )

        if text.endswith("```"):

            text = text[:-3]

        return text.strip()