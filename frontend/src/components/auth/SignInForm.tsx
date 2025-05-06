/* eslint-disable @typescript-eslint/no-unused-vars */
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

export default function SignInForm() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  interface LoginResponse {
    access: string;
    refresh: string;
    isAdmin: boolean;
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    try {
      const response = await axios.post<LoginResponse>("http://localhost:8000/api/users/login/", {
        username,
        password,
      });

      const { access, refresh, isAdmin } = response.data;

      localStorage.setItem("access", access);
      axios.defaults.headers.common["Authorization"] = `Bearer ${access}`;

      navigate("/dashboard");
    } catch {
      setError("Identifiants incorrects !");
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      {/* Input login + password */}
    </form>
  );
}
