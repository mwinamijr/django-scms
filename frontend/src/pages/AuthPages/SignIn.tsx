import { useState } from "react";
import { useNavigate } from "react-router-dom"; // Pour la redirection
import PageMeta from "../../components/common/PageMeta";
import AuthLayout from "./AuthPageLayout";
import SignInForm from "../../components/auth/SignInForm";
import axios from "axios";

console.log("************appel SignIn*****************");

interface LoginResponse {
  token: string;
  refresh: string;
  email: string;
  username: string;
  // Ajoutez d'autres champs si nécessaire
}

export default function SignIn() {
  console.log("Le composant SignIn est rendu !");

  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  const handleSignIn = async (email: string, password: string) => {
    try {
      // Envoyer les données de connexion à l'API
      const response = await axios.post<LoginResponse>("http://localhost:8000/api/users/login/", {
        email,
        password,
      });

      // Vérifier si la réponse contient un token
      if (response.data && response.data.token) {
        // Stocker le token dans le localStorage
        localStorage.setItem("token", response.data.token);

        // Rediriger vers le tableau de bord
        console.log("Le composant SignIn est OK !");

        navigate("/dashboard");
      } else {
        setError("Connexion échouée. Veuillez vérifier vos informations.");
      }
    } catch (err) {
      console.error("Erreur lors de la connexion :", err);
      setError("Une erreur s'est produite lors de la connexion. Veuillez réessayer.");
    }
  };

  return (
    <>
      <PageMeta
        title="Connexion React.js | TailAdmin - Modèle de tableau de bord Next.js"
        description="Ceci est la page de connexion React.js pour TailAdmin - Modèle de tableau de bord React.js Tailwind CSS"
      />
      <AuthLayout>
        <SignInForm onSignIn={handleSignIn} error={error} />
      </AuthLayout>
    </>
  );
}
