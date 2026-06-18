import os
import json
from app.llm.llm_service import LLMService
from app.analysis.analysis_models import TechStack

class StackDetector:
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service
        self.target_files = {
            "package.json",
            "requirements.txt",
            "pyproject.toml",
            "pom.xml",
            "Dockerfile",
            "docker-compose.yml",
            "go.mod",
            "Cargo.toml"
        }

    def detect_stack(self, repository_id: str, repo_path: str) -> TechStack:
        """
        Locates key configuration files in the repository and uses the LLM
        to extract the tech stack (frontend, backend, database).
        """
        config_contents = []
        
        # We'll just scan the top level directory for simplicity and speed
        # Many mono-repos have them deeper, but for MVP, root or 1 level deep is often enough.
        for root, dirs, files in os.walk(repo_path):
            # Limit depth to 2 levels to avoid massive scans
            depth = root[len(repo_path):].count(os.sep)
            if depth > 1:
                dirs.clear() # don't go deeper
                continue
                
            for file in files:
                if file in self.target_files:
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read()
                            # Truncate content if it's wildly massive (e.g. huge package-lock, but we didn't include lock files)
                            if len(content) > 10000:
                                content = content[:10000] + "...(truncated)"
                            config_contents.append(f"File: {file}\n{content}\n")
                    except Exception:
                        pass
                        
        if not config_contents:
            return TechStack(frontend=[], backend=[], database=[], other=[])
            
        combined_configs = "\n".join(config_contents)
        
        prompt = f"""
You are an expert technical architect. Analyze the following configuration files from a repository and determine the technology stack.
Identify frameworks, libraries, and tools used for the frontend, backend, and database.

Configuration files:
{combined_configs}

Return ONLY a valid JSON object matching this exact schema, with no markdown formatting or extra text:
{{
    "frontend": ["Next.js", "React", "TailwindCSS"],
    "backend": ["FastAPI", "Python"],
    "database": ["PostgreSQL", "Prisma"],
    "other": ["Docker", "Jest"]
}}
"""
        
        messages = [{"role": "system", "content": prompt}]
        try:
            raw_response = self.llm_service.generate_response(messages)
            # Clean up markdown code blocks if the LLM adds them despite instructions
            cleaned = raw_response.strip().removeprefix("```json").removesuffix("```").strip()
            data = json.loads(cleaned)
            return TechStack(**data)
        except Exception as e:
            print(f"Stack detection failed: {e}")
            return TechStack(frontend=[], backend=[], database=[], other=[])
