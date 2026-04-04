import { BrowserRouter, Routes, Route } from "react-router-dom";
import CustomerLayout from "./layouts/CustomerLayout.jsx";
import {Home} from "./pages/customer/Home.jsx";
import {Bookings} from "./pages/customer/Bookings.jsx";
import {Login} from "./pages/auth/Login.jsx";
import {Register} from "./pages/auth/Register.jsx";
import {Profile} from "./pages/customer/Profile.jsx";
import {CourtBooking} from "./pages/customer/CourtBooking.jsx";

function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />
                <Route element={<CustomerLayout />}>
                    <Route path="/" element={<Home />} />
                    <Route path="/court/:id" element={<CourtBooking />} />
                    <Route path="/bookings" element={<Bookings />} />
                    <Route path="/profile" element={<Profile />} />
                </Route>

            </Routes>
        </BrowserRouter>
    );
}

export default App;