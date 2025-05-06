import { useState } from "react"
import axios from "axios"
import { useNavigate } from "react-router-dom"

export default function SignInForm() {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState("")
  const navigate = useNavigate()

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setError("")

    try {
      interface LoginResponse {
        access: string;
        refresh: string;
        isAdmin: boolean;
        isAccountant: boolean;
        isTeacher: boolean;
        isParent: boolean;
      }
    
      const response = await axios.post<LoginResponse>("http://localhost:8000/api/users/login/", {
        email,
        password,
      });
    
      const { access, refresh, isAdmin, isAccountant, isTeacher, isParent } = response.data;
    
      // stockage local + autorisation
      localStorage.setItem("access_token", access);
      localStorage.setItem("refresh_token", refresh);
      localStorage.setItem("user_role", JSON.stringify({ isAdmin, isAccountant, isTeacher, isParent }));
      axios.defaults.headers.common["Authorization"] = `Bearer ${access}`;
    
      navigate("/");
    } catch (err) {
      console.error(err);
      setError("Identifiants incorrects !");
    }
    
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4 w-full max-w-sm mx-auto mt-10">
      <h2 className="text-xl font-semibold">Connexion</h2>
      {error && <p className="text-red-500">{error}</p>}
      <input
        type="email"
        placeholder="Adresse e-mail"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        className="w-full px-4 py-2 border rounded"
        required
      />
      <input
        type="password"
        placeholder="Mot de passe"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        className="w-full px-4 py-2 border rounded"
        required
      />
      <button
        type="submit"
        className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
      >
        Se connecter
      </button>
    </form>
  )
}
