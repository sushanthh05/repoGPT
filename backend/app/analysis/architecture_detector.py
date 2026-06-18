import os
from app.llm.llm_service import LLMService

class ArchitectureDetector:
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service

    def detect_architecture(self, repo_path: str) -> str:
        """
        Uses the LLM to infer the high-level architecture of the repository
        by analyzing the file tree and the README.
        """
        # 1. Get a basic file tree
        tree_lines = []
        for root, dirs, files in os.walk(repo_path):
            dirs[:] = [d for d in dirs if d not in {".git", "node_modules", "venv", ".venv", "dist", "build", "__pycache__"}]
            rel_path = os.path.relpath(root, repo_path)
            if rel_path == ".":
                rel_path = ""
            else:
                rel_path = rel_path.replace("\\", "/") + "/"
            
            # For brevity, don't go too deep. We just want high level folders and files.
            depth = rel_path.count("/")
            if depth > 3:
                dirs.clear()
                continue
                
            for file in files:
                tree_lines.append(f"{rel_path}{file}")
                
        file_tree = "\n".join(tree_lines[:200]) # Cap it to 200 files for context limits
        
        # 2. Get the README if it exists
        readme_content = ""
        readme_path = os.path.join(repo_path, "README.md")
        if not os.path.exists(readme_path):
            readme_path = os.path.join(repo_path, "readme.md")
            
        if os.path.exists(readme_path):
            try:
                with open(readme_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    # Grab first 3000 chars of readme
                    readme_content = content[:3000]
            except Exception:
                pass
                
        prompt = f"""
You are an expert software architect. Below is the file tree and README content for a repository.
Your task is to infer the high-level architecture of this repository.

Describe the layer architecture using plain text or ASCII arrows if helpful (e.g., Frontend -> API Layer -> Database Layer).
Keep it concise, no more than 1 or 2 paragraphs. Focus on structural organization.

README Preview:
{readme_content}

File Tree Preview:
{file_tree}
"""
        messages = [{"role": "system", "content": prompt}]
        try:
            return self.llm_service.generate_response(messages)
        except Exception as e:
            print(f"Architecture detection failed: {e}")
            return "Could not determine repository architecture."
