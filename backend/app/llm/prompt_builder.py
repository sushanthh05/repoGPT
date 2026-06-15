from app.llm.system_prompts import CORE_SYSTEM_PROMPT

class PromptBuilder:
    def build_prompt(self, question: str, context: str) -> list[dict[str, str]]:
        """
        Constructs the messages payload for the LLM API.
        We format this as a standard Chat message structure: system, and user.
        """
        system_message = {
            "role": "system",
            "content": f"{CORE_SYSTEM_PROMPT}\n\n---\n\nRepository Context:\n{context}"
        }
        
        user_message = {
            "role": "user",
            "content": f"User Question: {question}\n\nPlease provide your answer based ONLY on the repository context above."
        }
        
        return [system_message, user_message]
