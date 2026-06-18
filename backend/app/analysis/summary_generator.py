import os
from app.llm.llm_service import LLMService
from app.analysis.analysis_models import TechStack

class SummaryGenerator:
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service

    def generate_summary(self, repo_path: str, tech_stack: TechStack, architecture: str) -> str:
        """
        Uses the LLM to generate a human-friendly narrative summary of the project.
        """
        # Get the README if it exists
        readme_content = ""
        readme_path = os.path.join(repo_path, "README.md")
        if not os.path.exists(readme_path):
            readme_path = os.path.join(repo_path, "readme.md")
            
        if os.path.exists(readme_path):
            try:
                with open(readme_path, "r", encoding="utf-8") as f:
                    readme_content = f.read()[:3000]
            except Exception:
                pass

        prompt = f"""
You are an expert developer. Summarize the purpose and design of this repository.

Tech Stack Detected:
Frontend: {", ".join(tech_stack.frontend) or "None detected"}
Backend: {", ".join(tech_stack.backend) or "None detected"}
Database: {", ".join(tech_stack.database) or "None detected"}
Other: {", ".join(tech_stack.other) or "None"}

Architecture Overview:
{architecture}

README Context:
{readme_content}

Generate a concise, 2-3 paragraph narrative summary of the repository. Explain what the project is, what technologies it uses, and how it is broadly structured.
Do not use bullet points. Make it read naturally.
"""
        messages = [{"role": "system", "content": prompt}]
        try:
            return self.llm_service.generate_response(messages)
        except Exception as e:
            print(f"Summary generation failed: {e}")
            return "Could not generate repository summary."
