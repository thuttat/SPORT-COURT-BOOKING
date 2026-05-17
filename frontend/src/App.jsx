import { BrowserRouter, Routes, Route } from "react-router-dom";
import CustomerLayout from "./layouts/CustomerLayout.jsx";
import {Home} from "./pages/customer/Home/Home.jsx";
import {Login} from "./pages/auth/Login.jsx";
import {Register} from "./pages/auth/Register.jsx";
import {Profile} from "./pages/customer/Profile/Profile.jsx";
import {CourtBooking} from "./pages/customer/CourtBooking/CourtBooking.jsx";
import {BookingHistory} from "./pages/customer/BookingHistory/BookingHistory.jsx";
import {BookingDetails} from "./pages/customer/BookingDetails/BookingDetails.jsx";
import {AdminDashboard} from "./pages/admin/AdminDashboard/AdminDashboard.jsx";
import AdminLayout from "./layouts/AdminLayout.jsx";
import PrivateRoute from "./services/auth/PrivateRoute.jsx";
import {ProtectedRoute} from "./components/common/ProtectedRoute.jsx";
import {CourtManagement} from "./pages/admin/CourtManagement/CourtManagement.jsx";
import {BookingManagement} from "./pages/admin/BookingManagement/BookingManagement.jsx";

function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />
                <Route element={<CustomerLayout />}>
                    <Route path="/" element={<Home />} />
                    <Route element={<ProtectedRoute allowedRoles={["USER"]} />}>
                        <Route path="/court/:id" element={<CourtBooking />} />
                        <Route path="/bookings" element={<BookingHistory />} />
                        <Route path="/booking/:id" element={<BookingDetails />} />
                        <Route path="/profile" element={<Profile />} />
                    </Route>
                </Route>
                <Route path="/admin" element={
                    <PrivateRoute allowedRoles={["ADMIN"]}>
                        <AdminLayout />
                    </PrivateRoute>
                }>
                    <Route path="dashboard" element={<AdminDashboard />} />
                    <Route path="courts" element={<CourtManagement />} />
                    <Route path="bookings" element={<BookingManagement />} />
                </Route>
            </Routes>
        </BrowserRouter>
    );
}

export default App;