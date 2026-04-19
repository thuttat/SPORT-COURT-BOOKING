import { useContext } from "react";
import { BookingProvider } from "./BookingProvider.jsx";

export function useBooking() {
    return useContext(BookingProvider);
}