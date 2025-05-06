import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import SignIn from "./pages/AuthPages/SignIn";
import SignIn2 from "./pages/AuthPages/SignIn2";
import Home from "./pages/Dashboard/Home";
import NotFound from "./pages/OtherPage/NotFound";
import AppLayout from "./layout/AppLayout";

export default function App() {
  return (
    <Router>
      <Routes>
        {/* Layout App avec menu/side nav */}
        <Route path="/" element={<AppLayout />}>
          <Route index element={<Home />} />
        </Route>

        {/* Auth */}
        <Route path="/signin" element={<SignIn />} />
        <Route path="/signin2" element={<SignIn2 />} />

        {/* Fallback */}
        <Route path="*" element={<NotFound />} />
      </Routes>
    </Router>
  );
}
