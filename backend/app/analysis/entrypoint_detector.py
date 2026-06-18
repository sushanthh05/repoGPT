import os

class EntrypointDetector:
    def __init__(self):
        self.common_entrypoints = {
            "main.py", "app.py", "manage.py", "wsgi.py",
            "server.js", "index.js", "app.js",
            "server.ts", "index.ts", "main.ts", "app.ts",
            "Program.cs", "Startup.cs",
            "main.go",
            "Cargo.toml", "src/main.rs",
            "manage.py"
        }
        
        self.important_files_set = {
            "README.md", "package.json", "requirements.txt",
            "pyproject.toml", "docker-compose.yml", "Dockerfile",
            "schema.prisma", ".env.example", "tsconfig.json"
        }

    def detect(self, repo_path: str) -> tuple[list[str], list[str]]:
        """
        Scans the repository to identify common entry points and globally important files.
        Returns a tuple of (entrypoints, important_files).
        """
        entrypoints = []
        important_files = []
        
        for root, dirs, files in os.walk(repo_path):
            # We don't want to dig into massive node_modules or venv folders
            dirs[:] = [d for d in dirs if d not in {".git", "node_modules", "venv", ".venv", "dist", "build", "__pycache__"}]
            
            for file in files:
                rel_path = os.path.relpath(os.path.join(root, file), repo_path)
                
                # Check for entry points
                # If the filename itself matches a common entry point, or if it's explicitly src/main.rs
                if file in self.common_entrypoints or rel_path.replace("\\", "/") in self.common_entrypoints:
                    entrypoints.append(rel_path.replace("\\", "/"))
                    
                # Check for important files
                if file in self.important_files_set:
                    important_files.append(rel_path.replace("\\", "/"))
                    
        return sorted(entrypoints), sorted(important_files)
