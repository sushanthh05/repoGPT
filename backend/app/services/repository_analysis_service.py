import os
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.llm.llm_service import LLMService
from app.analysis.stack_detector import StackDetector
from app.analysis.entrypoint_detector import EntrypointDetector
from app.analysis.architecture_detector import ArchitectureDetector
from app.analysis.summary_generator import SummaryGenerator
from app.analysis.analysis_models import RepositoryInsights, RepositoryMetrics
from app.database.models.models import DocumentDB, ChunkDB
from app.config.settings import settings

class RepositoryAnalysisService:
    def __init__(self, db: Session):
        self.db = db
        self.llm_service = LLMService()
        self.stack_detector = StackDetector(self.llm_service)
        self.entrypoint_detector = EntrypointDetector()
        self.architecture_detector = ArchitectureDetector(self.llm_service)
        self.summary_generator = SummaryGenerator(self.llm_service)
        self.base_repo_dir = os.path.join(os.getcwd(), "repositories")

    def generate_insights(self, repository_id: str) -> RepositoryInsights:
        """
        Orchestrates the entire repository analysis process.
        """
        repo_path = os.path.join(self.base_repo_dir, repository_id)
        if not os.path.exists(repo_path):
            raise FileNotFoundError(f"Repository {repository_id} not found locally.")

        # 1. Gather Metrics from Database
        total_documents = self.db.query(DocumentDB).filter(DocumentDB.repository_id == repository_id).count()
        total_chunks = self.db.query(ChunkDB).filter(ChunkDB.repository_id == repository_id).count()
        
        # Calculate file count from DB or FileSystem
        # Let's count files explicitly in the repo_path
        total_files = 0
        for root, _, files in os.walk(repo_path):
            total_files += len(files)

        # Calculate language distribution
        lang_counts = self.db.query(DocumentDB.language, func.count(DocumentDB.id)).filter(
            DocumentDB.repository_id == repository_id
        ).group_by(DocumentDB.language).all()
        
        languages_used = {lang or "Unknown": count for lang, count in lang_counts}

        metrics = RepositoryMetrics(
            total_files=total_files,
            total_documents=total_documents,
            total_chunks=total_chunks,
            languages_used=languages_used
        )

        # 2. Detect Tech Stack
        tech_stack = self.stack_detector.detect_stack(repository_id, repo_path)

        # 3. Detect Entry Points & Important Files
        entrypoints, important_files = self.entrypoint_detector.detect(repo_path)

        # 4. Infer Architecture
        architecture = self.architecture_detector.detect_architecture(repo_path)

        # 5. Generate Narrative Summary
        summary = self.summary_generator.generate_summary(repo_path, tech_stack, architecture)

        return RepositoryInsights(
            repository_id=repository_id,
            summary=summary,
            tech_stack=tech_stack,
            entrypoints=entrypoints,
            important_files=important_files,
            architecture_overview=architecture,
            metrics=metrics
        )
