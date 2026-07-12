import api from "./axios";

export interface LoginData {
  email: string;
  password: string;
}

export async function login(data: LoginData) {
  const response = await api.post("/auth/login", data);
  return response.data;
}
