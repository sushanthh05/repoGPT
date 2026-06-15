from app.services.retrieval_service import RetrievalService
from app.llm.prompt_builder import PromptBuilder
from app.llm.llm_service import LLMService
from app.llm.answer_formatter import AnswerFormatter

class ChatService:
    def __init__(self):
        self.retrieval_service = RetrievalService()
        self.prompt_builder = PromptBuilder()
        self.llm_service = LLMService()
        self.answer_formatter = AnswerFormatter()

    def chat(self, repository_id: str, question: str) -> tuple[str, list[dict]]:
        """
        Orchestrates the end-to-end question answering flow:
        1. Retrieve context
        2. Build prompt
        3. Invoke LLM
        4. Format and return answer with sources
        """
        # 1. Retrieve Context
        context_string, sources = self.retrieval_service.build_context(repository_id, question)
        
        # 2. Check for empty context
        if not context_string or not context_string.strip():
            fallback_answer = "I could not find sufficient repository context to answer this question."
            return fallback_answer, []
            
        # 3. Build Prompt
        messages = self.prompt_builder.build_prompt(question=question, context=context_string)
        
        # 4. Invoke LLM
        raw_answer = self.llm_service.generate_response(messages)
        
        # 5. Format Answer
        final_answer = self.answer_formatter.format_answer(raw_answer, sources)
        
        return final_answer, sources
