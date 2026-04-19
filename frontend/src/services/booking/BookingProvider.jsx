import { useState } from "react";
import { BookingContext } from "./bookingContext";

export function BookingProvider({ children }) {
    const [fields] = useState([
        { id: "c1", sport: "football", available: true },
        { id: "c2", sport: "badminton", available: true }
    ]);

    const [bookings] = useState([
        {
            id: "b1",
            fieldName: "Sân A",
            sport: "football",
            date: "2026-04-19",
            timeSlots: ["08:00"]
        }
    ]);

    return (
        <BookingContext.Provider value={{ fields, bookings }}>
            {children}
        </BookingContext.Provider>
    );
}