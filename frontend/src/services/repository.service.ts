import { api } from "./api";
import { API_ENDPOINTS } from "@/constants/api-endpoints";
import { Repository, RepositoryOverview } from "@/types/repository";

export const repositoryService = {
  async getRepositories(): Promise<Repository[]> {
    const response = await api.get(API_ENDPOINTS.REPOSITORIES);
    return response.data;
  },

  async analyzeRepository(repoUrl: string): Promise<RepositoryOverview> {
    const response = await api.post(API_ENDPOINTS.REPOSITORIES_ANALYZE, { repo_url: repoUrl });
    return response.data;
  }
};
