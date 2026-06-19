export interface Repository {
  repository_id: string;
  repository_name: string;
}

export interface RepositoryOverview {
  status: string;
  repository_id: string;
  repository_name: string;
  message: string;
}
