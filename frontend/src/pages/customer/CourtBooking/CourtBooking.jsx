import { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import {Card, CardContent} from "../../../components/common/Card.jsx";
import { BookingHeader } from "./components/BookingHeader.jsx";
import { DateSelector } from "../../../components/common/DateSelector.jsx";
import { TimeSlotGrid } from "./components/TimeSlotGrid.jsx";
import { BookingSummary } from "./components/BookingSummary.jsx";

import "./courtBooking.css";

const timeSlots = [
    "08:00","09:00","10:00","11:00","12:00",
    "13:00","14:00","15:00","16:00","17:00",
    "18:00","19:00","20:00","21:00","22:00"
];

export function CourtBooking() {
    const navigate = useNavigate();
    const { id } = useParams();
    const [selectedDate, setSelectedDate] = useState(0);
    const [selectedSlots, setSelectedSlots] = useState([]);

    const dates = Array.from({ length: 7 }, (_, i) => {
        const d = new Date();
        d.setDate(d.getDate() + i);
        return d;
    });

    const toggleSlot = (slot) => {
        setSelectedSlots(prev =>
            prev.includes(slot)
                ? prev.filter(s => s !== slot)
                : [...prev, slot]
        );
    };

    return (
        <div className="booking-container">
            <div className="booking-grid">
                    <BookingHeader
                        name={`Court ${id}`}
                        onBack={() => navigate("/")}
                    />

                    <Card className="date-card">
                        <CardContent className="content">
                            <h3>Select Date</h3>
                            <DateSelector
                                dates={dates}
                                selectedDate={selectedDate}
                                onSelect={(i) => {
                                    setSelectedDate(i);
                                    setSelectedSlots([]);
                                }}
                            />
                        </CardContent>
                    </Card>

                    <Card className="time-card">
                        <CardContent className="content">
                            <h3>Select Time</h3>
                            <TimeSlotGrid
                                slots={timeSlots}
                                selectedSlots={selectedSlots}
                                onToggle={toggleSlot}
                            />
                        </CardContent>
                    </Card>

                <BookingSummary
                    className="summary-card-wrapper"
                    date={dates[selectedDate]}
                    slots={selectedSlots}
                />
                </div>
        </div>
    );
}