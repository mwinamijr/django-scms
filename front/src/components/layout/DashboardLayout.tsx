import { ReactNode } from "react"
import { Link, useLocation } from "react-router-dom"

const menuItems = [
  { path: "/students", label: "👨‍🎓 Élèves" },
  { path: "/grades", label: "📊 Notes" },
  { path: "/attendance", label: "📅 Présences" },
  { path: "/finance", label: "💰 Finances" },
]

export default function DashboardLayout({ children }: { children: ReactNode }) {
  const location = useLocation()

  return (
    <div className="flex h-screen">
      {/* Sidebar fixe uniquement pour desktop */}
      <aside className="w-64 bg-zinc-900 text-white p-6">
        <h1 className="text-2xl font-bold mb-6">📚 Mon École</h1>
        <nav className="space-y-2">
          {menuItems.map(item => (
            <Link
              key={item.path}
              to={item.path}
              className={`block p-2 rounded hover:bg-zinc-800 ${
                location.pathname === item.path ? "bg-zinc-800" : ""
              }`}
            >
              {item.label}
            </Link>
          ))}
        </nav>
      </aside>

      {/* Zone de contenu */}
      <main className="flex-1 overflow-y-auto p-6 bg-gray-100">
        {children}
      </main>
    </div>
  )
}
