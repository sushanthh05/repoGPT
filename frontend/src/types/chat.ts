export interface SourceEvidence {
  file_path: string;
  chunk_id: string;
  similarity_score: number;
  language: string;
  snippet: string;
}

export interface ChatResponse {
  answer: string;
  sources: SourceEvidence[];
  confidence: number;
}
