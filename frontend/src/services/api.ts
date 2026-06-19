import axios from "axios";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Interceptors can be added here in the future
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Global error handling could go here
    return Promise.reject(error);
  }
);
