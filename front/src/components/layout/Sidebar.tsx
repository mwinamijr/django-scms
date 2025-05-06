import { Link } from "react-router-dom";

export default function Sidebar() {
  return (
    <aside className="w-64 bg-white shadow-md dark:bg-gray-800">
      <nav className="p-4">
        <ul className="space-y-2">
          <li><Link to="/dashboard" className="text-gray-800 dark:text-white">Tableau de bord</Link></li>
          <li><Link to="/signin2" className="text-gray-800 dark:text-white">Profil</Link></li>
        </ul>
      </nav>
    </aside>
  );
}
