export interface AnalysisResult {
  metrics: {
    total_files: number;
    total_documents: number;
    total_chunks: number;
    languages_used: Record<string, number>;
  };
  tech_stack: {
    frontend: string[];
    backend: string[];
    database: string[];
    other: string[];
  };
  entry_points: string[];
  important_files: string[];
  architecture_overview: string;
  repository_summary: string;
}
