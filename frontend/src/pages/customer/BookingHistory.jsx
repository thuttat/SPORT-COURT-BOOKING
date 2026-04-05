import { useState } from "react";
import {Card} from "../../components/common/Card.jsx";
import "./styles/bookingHistory.css";
import {PageHeader} from "../../components/common/PageHeader.jsx";
import {BookingTabs} from "./components/BookingTabs.jsx";
import {BookingCard} from "./components/BookingCard.jsx";

export function BookingHistory() {
    const [activeTab, setActiveTab] = useState("upcoming");

    const bookings = [
        {
            id: "b1",
            courtName: "Sân bóng đá Mini A",
            sport: "football",
            date: "2026-04-10",
            timeSlots: ["08:00", "09:00"],
            status: "upcoming"
        },
        {
            id: "b2",
            courtName: "Sân cầu lông VIP",
            sport: "badminton",
            date: "2026-04-02",
            timeSlots: ["18:00"],
            status: "past"
        },
        {
            id: "b3",
            courtName: "Sân tennis trung tâm",
            sport: "tennis",
            date: "2026-04-01",
            timeSlots: ["19:00", "20:00"],
            status: "cancelled"
        }
    ];

    const displayedBookings = bookings.filter(b =>
        activeTab === "upcoming"
            ? b.status === "upcoming"
            : b.status === "past" || b.status === "cancelled"
    );

    return (
        <div className="booking-history-container">
            <div className="booking-history-wrapper">
                <PageHeader header="My Bookings" text="View and manage your court bookings" />

                <BookingTabs activeTab={activeTab} setActiveTab={setActiveTab} />

                <div className="booking-list">
                    {displayedBookings.length === 0 ? (
                        <Card className="empty-card">
                            <div className="empty">
                                <div className="icon">📅</div>
                                <h3>No bookings found</h3>
                                <p>Try booking a court first</p>
                            </div>
                        </Card>
                    ) : (
                        displayedBookings.map(booking => (
                            <BookingCard key={booking.id} booking={booking} showCancel={activeTab === "upcoming"} />
                        ))
                    )}
                </div>
            </div>
        </div>
    );
}