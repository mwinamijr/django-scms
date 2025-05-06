import PageMeta from "../../components/common/PageMeta";
import AuthLayout from "./AuthPageLayout";
import SignUpForm from "../../components/auth/SignUpForm";

export default function SignUp() {
  return (
    <>
      <PageMeta
        title="Inscription React.js | TailAdmin - Modèle de tableau de bord Next.js"
        description="Ceci est la page d'inscription React.js pour TailAdmin - Modèle de tableau de bord React.js Tailwind CSS"
      />
      <AuthLayout>
        <SignUpForm />
      </AuthLayout>
    </>
  );
}
