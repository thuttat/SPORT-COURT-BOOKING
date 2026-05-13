import {useEffect, useState} from "react";
import { useNavigate, useParams } from "react-router-dom";
import {Card, CardContent} from "../../../components/common/Card.jsx";
import { BookingHeader } from "./components/BookingHeader.jsx";
import { DateSelector } from "../../../components/common/DateSelector.jsx";
import { TimeSlotGrid } from "./components/TimeSlotGrid.jsx";
import { BookingSummary } from "./components/BookingSummary.jsx";

import "./courtBooking.css";
import {useField} from "../../../services/field/useField.js";
import {formatTodayString} from "../../../utils/formatters.js";

export function CourtBooking() {
    const navigate = useNavigate();
    const { id } = useParams();
    const {slots, loadingSlots, fetchFieldSlots} = useField();
    const [selectedDate, setSelectedDate] = useState(formatTodayString());
    const [selectedSlot, setSelectedSlot] = useState(null);

    useEffect(() => {
        if (id && selectedDate) {
            fetchFieldSlots(id, selectedDate);
            setSelectedSlot(null);
        }
    }, [id, selectedDate, fetchFieldSlots]);

    const handleConfirmBooking = () => {
        console.log("Booking:", id, "Date:", selectedDate, "Time slots:", selectedSlot.id);
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
                            <input
                                type="date"
                                className="input"
                                value={selectedDate}
                                min={formatTodayString()}
                                onChange={(e) => setSelectedDate(e.target.value)}
                                style={{ padding: "12px", borderRadius: "8px", border: "1px solid #e2e8f0", width: "96%", fontSize: "16px" }}
                            />
                        </CardContent>
                    </Card>

                    <Card className="time-card">
                        <CardContent className="content">
                            <h3>Select Time</h3>
                            {loadingSlots ? (
                                <p className="loading">Loading...</p>
                            ) : (
                                <TimeSlotGrid
                                    slots={slots}
                                    selectedSlot={selectedSlot}
                                    onToggle={(slot) => setSelectedSlot(slot)}
                                />
                            )}
                        </CardContent>
                    </Card>

                    <BookingSummary
                        className="summary-card-wrapper"
                        date={selectedDate}
                        selectedSlot={selectedSlot}
                        onConfirm={handleConfirmBooking}
                    />
                </div>
        </div>
    );
}