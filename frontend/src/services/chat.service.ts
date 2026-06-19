import { api } from "./api";
import { API_ENDPOINTS } from "@/constants/api-endpoints";
import { ChatResponse } from "@/types/chat";

export const chatService = {
  async sendMessage(repositoryId: string, question: string): Promise<ChatResponse> {
    const response = await api.post(API_ENDPOINTS.CHAT(repositoryId), { question });
    return response.data;
  }
};
