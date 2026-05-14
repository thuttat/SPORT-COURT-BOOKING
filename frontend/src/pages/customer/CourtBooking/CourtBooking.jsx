import {useEffect, useState} from "react";
import {useLocation, useNavigate, useParams} from "react-router-dom";
import {Card, CardContent} from "../../../components/common/Card.jsx";
import { BookingHeader } from "./components/BookingHeader.jsx";
import { DateSelector } from "../../../components/common/DateSelector.jsx";
import { TimeSlotGrid } from "./components/TimeSlotGrid.jsx";
import { BookingSummary } from "./components/BookingSummary.jsx";

import "./courtBooking.css";
import {useField} from "../../../services/field/useField.js";
import {formatTodayString} from "../../../utils/formatters.js";
import {createBookingRequest} from "../../../services/apis.js";

export function CourtBooking() {
    const navigate = useNavigate();
    const { id } = useParams();
    const location = useLocation();
    const {slots, loadingSlots, fetchFieldSlots, fieldDetail, fetchFieldDetail} = useField();
    const [selectedDate, setSelectedDate] = useState(location.state?.preselectedDate || formatTodayString());
    const [selectedSlot, setSelectedSlot] = useState(null);
    const [isSubmitted, setIsSubmitted] = useState(false);
    const {fields} = useField();
    const currentField = fields.find((field) => field.id === parseInt(id));
    const basePrice = currentField?.price_per_hour || 0;

    useEffect(() => {
        if (id && selectedDate) {
            fetchFieldSlots(id, selectedDate);
            setSelectedSlot(null);
            fetchFieldDetail(id);
        }
    }, [id, selectedDate]);

    const handleConfirmBooking = async () => {
        if (!selectedSlot) return;
        setIsSubmitted(true);
        try {
            await createBookingRequest(id, selectedSlot.id, selectedDate);
            alert("Booking successfully!");
            navigate("/bookings");
        } catch (error) {
            alert(`Error: ${error.response?.data?.message}`);
        } finally {
            setIsSubmitted(false);
        }
    };

    const isDayFull = slots.length > 0 && slots.every(slot => !slot.is_available);
    const subTotal = selectedSlot ? basePrice * selectedSlot.duration : 0;
    const totalPrice = selectedSlot ? subTotal * selectedSlot.price_multiplier : 0;

    return (
        <div className="booking-container">
            <div className="booking-grid">
                    <BookingHeader
                        onBack={() => navigate("/")}
                        fieldDetail={fieldDetail}
                        isFull={isDayFull}
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
                        subTotal={subTotal}
                        totalPrice={totalPrice}
                        onConfirm={handleConfirmBooking}
                    />
                </div>
        </div>
    );
}