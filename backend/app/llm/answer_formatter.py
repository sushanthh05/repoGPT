class AnswerFormatter:
    def format_answer(self, raw_answer: str, sources: list[dict]) -> str:
        """
        Appends a clean 'Sources:' section to the bottom of the LLM's response.
        """
        if not sources:
            return raw_answer
            
        formatted_answer = raw_answer.strip()
        
        # Extract unique file paths while preserving order
        unique_files = []
        seen = set()
        for s in sources:
            file_path = s.get('file_path', 'unknown')
            if file_path not in seen:
                seen.add(file_path)
                unique_files.append(file_path)
                
        if unique_files:
            formatted_answer += "\n\n### Sources\n"
            for file_path in unique_files:
                formatted_answer += f"- `{file_path}`\n"
                
        return formatted_answer
