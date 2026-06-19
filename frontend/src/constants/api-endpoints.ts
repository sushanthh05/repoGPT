export const API_ENDPOINTS = {
  REPOSITORIES: "/repositories",
  REPOSITORIES_ANALYZE: "/repositories/analyze",
  ANALYSIS: (id: string) => `/repositories/${id}/analyze`,
  CHAT: (id: string) => `/repositories/${id}/chat`,
  PARSE: (id: string) => `/repositories/${id}/parse`,
  CHUNK: (id: string) => `/repositories/${id}/chunk`,
  INDEX: (id: string) => `/repositories/${id}/index`,
};
