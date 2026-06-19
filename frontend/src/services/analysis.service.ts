import { api } from "./api";
import { API_ENDPOINTS } from "@/constants/api-endpoints";
import { AnalysisResult } from "@/types/analysis";

export const analysisService = {
  async getAnalysis(repositoryId: string): Promise<AnalysisResult> {
    const response = await api.post(API_ENDPOINTS.ANALYSIS(repositoryId));
    return response.data;
  }
};
