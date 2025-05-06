import PageMeta from "../../components/common/PageMeta";
import AuthLayout from "../../layout/AuthLayout"; // Corrige le chemin si besoin
import SignInForm from "../../components/auth/SignInForm";

export default function SignIn() {
  return (
    <>
      <PageMeta
        title="Connexion | Tableau de bord"
        description="Page de connexion utilisateur pour le système de gestion scolaire"
      />
      <AuthLayout>
        <SignInForm />
      </AuthLayout>
    </>
  );
}
