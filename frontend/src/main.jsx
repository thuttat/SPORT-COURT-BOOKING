import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./styles/variables.css";
import "./styles/index.css";
import {BookingProvider} from "./services/booking/BookingProvider.jsx";
import {AuthProvider} from "./services/auth/AuthContext.jsx";

ReactDOM.createRoot(document.getElementById('root')).render(
    <React.StrictMode>
        <AuthProvider>
            <BookingProvider>
                <App />
            </BookingProvider>
        </AuthProvider>
    </React.StrictMode>
);