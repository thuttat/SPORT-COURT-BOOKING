import { useState } from "react";
import { BookingContext } from "./bookingContext";
import {getBookingDetailsRequest, getMyBookingsRequest} from "../apis.js";

export function BookingProvider({ children }) {
    const [bookings, setBookings] = useState([]);
    const [pagination, setPagination] = useState({});
    const [loading, setLoading] = useState(false);
    const [bookingDetails, setBookingDetails] = useState(null);
    const [detailLoading, setDetailLoading] = useState(true);

    const fetchMyBookings = async (page = 1) => {
        setLoading(true);
        try {
            const response = await getMyBookingsRequest(page);
            setBookings(response.data.data);
            setPagination(response.data.pagination);
        } catch (error) {
            console.error("Error fetching booking history:", error);
            throw error;
        } finally {
            setLoading(false);
        }
    };

    const fetchBookingDetails = async (id) => {
        setDetailLoading(true);
        try {
            const response = await getBookingDetailsRequest(id);
            setBookingDetails(response.data.data);
        } catch (error) {
            console.error("Error fetching booking details:", error);
        } finally {
            setDetailLoading(false);
        }
    }

    return (
        <BookingContext.Provider value={{
            bookings, pagination, loading, fetchMyBookings,
            bookingDetails, detailLoading, fetchBookingDetails,
        }}>
            {children}
        </BookingContext.Provider>
    );
}