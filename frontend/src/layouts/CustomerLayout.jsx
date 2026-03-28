import { Outlet } from "react-router-dom";
import {Header} from "../components/Header.jsx";
import {Footer} from "../components/Footer.jsx";

export default function CustomerLayout() {
    return (
        <div className="min-vh-100 d-flex flex-column" style={{ background: "var(--background)" }}>
            <Header />

            <main className="flex-grow-1">
                <Outlet />
            </main>

            <Footer />
        </div>
    );
}