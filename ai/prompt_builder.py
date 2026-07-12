import re
from pathlib import Path


class PromptBuilder:
    """
    Builds prompts from Markdown templates.

    Folder Structure
    ----------------
    ai/
        prompts/
            forecast/
                executive.md
                risk.md
                recommendation.md

            inventory/
                assessment.md
                risk.md
                purchase.md

            dashboard/
                executive.md
    """

    PROMPT_ROOT = Path("ai/prompts")

    _cache = {}

    # --------------------------------------------------
    # Build Prompt
    # --------------------------------------------------

    @classmethod
    def build(
        cls,
        module: str,
        template: str,
        variables: dict
    ) -> str:

        prompt = cls._load_template(
            module,
            template
        )

        placeholders = cls._find_placeholders(
            prompt
        )

        missing = [
            p for p in placeholders
            if p not in variables
        ]

        if missing:

            raise ValueError(

                "Missing prompt variables: "

                + ", ".join(missing)

            )

        for key, value in variables.items():

            prompt = prompt.replace(

                "{{" + key + "}}",

                str(value)

            )

        return prompt

    # --------------------------------------------------
    # Load Template
    # --------------------------------------------------

    @classmethod
    def _load_template(
        cls,
        module,
        template
    ):

        cache_key = f"{module}/{template}"

        if cache_key in cls._cache:

            return cls._cache[cache_key]

        path = (
            cls.PROMPT_ROOT
            / module
            / f"{template}.md"
        )

        if not path.exists():

            raise FileNotFoundError(

                f"Prompt not found: {path}"

            )

        content = path.read_text(
            encoding="utf-8"
        )

        cls._cache[cache_key] = content

        return content

    # --------------------------------------------------
    # Find Placeholders
    # --------------------------------------------------

    @staticmethod
    def _find_placeholders(
        prompt
    ):

        return re.findall(

            r"\{\{(.*?)\}\}",

            prompt

        )

    # --------------------------------------------------
    # Clear Cache
    # --------------------------------------------------

    @classmethod
    def clear_cache(cls):

        cls._cache.clear()