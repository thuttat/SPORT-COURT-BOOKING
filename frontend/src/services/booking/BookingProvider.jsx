import { useState } from "react";
import { BookingContext } from "./bookingContext";
import {cancelBookingRequest, getBookingDetailsRequest, getMyBookingsRequest} from "../apis.js";

export function BookingProvider({ children }) {
    const [bookings, setBookings] = useState([]);
    const [loading, setLoading] = useState(false);
    const [bookingDetails, setBookingDetails] = useState(null);
    const [detailLoading, setDetailLoading] = useState(true);

    const fetchMyBookings = async () => {
        setLoading(true);
        try {
            let allData = [];
            let page = 1;
            let hasNext = true;

            while (hasNext) {
                const response = await getMyBookingsRequest(page);
                allData = [...allData, ...response.data.data];
                hasNext = response.data.pagination.has_next;
                page++;
            }

            setBookings(allData);
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

    const cancelBooking = async (id) => {
        try {
            const response = await cancelBookingRequest(id);
            return response.data;
        } catch (error) {
            const errorMsg = error.response?.data?.message;
            throw new Error(errorMsg);
        }
    }

    return (
        <BookingContext.Provider value={{
            bookings, loading, fetchMyBookings,
            bookingDetails, detailLoading, fetchBookingDetails,
            cancelBooking
        }}>
            {children}
        </BookingContext.Provider>
    );
}