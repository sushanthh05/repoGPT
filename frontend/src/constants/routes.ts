export const ROUTES = {
  HOME: "/",
  REPOSITORIES: "/repositories",
  REPOSITORY_OVERVIEW: (id: string) => `/repositories/${id}`,
  REPOSITORY_CHAT: (id: string) => `/repositories/${id}/chat`,
  REPOSITORY_ANALYSIS: (id: string) => `/repositories/${id}/analysis`,
};
