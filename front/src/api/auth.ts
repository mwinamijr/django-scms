// src/api/auth.ts
import axios from "axios";

interface LoginResponse {
  access: string;
  refresh: string;
  isAdmin: boolean;
  isParent: boolean;
  isAccountant: boolean;
}

export async function login(username: string, password: string): Promise<LoginResponse> {
  const response = await axios.post<LoginResponse>("http://localhost:8000/api/users/login/", {
    username,
    password,
  });
  return response.data;
}
