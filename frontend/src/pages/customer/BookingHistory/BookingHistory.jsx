import {useEffect, useState} from "react";
import {Card} from "../../../components/common/Card.jsx";
import "./bookingHistory.css";
import {PageHeader} from "../../../components/common/PageHeader.jsx";
import {BookingTabs} from "./components/BookingTabs.jsx";
import {BookingCard} from "./components/BookingCard.jsx";
import {EmptyState} from "../../../components/common/EmptyState.jsx";
import {useBooking} from "../../../services/booking/useBooking.js";
import {Pagination} from "../../../components/common/Pagination.jsx";

export function BookingHistory() {
    const [activeTab, setActiveTab] = useState("upcoming");

    const { bookings, loading, pagination, fetchMyBookings } = useBooking();

    useEffect(() => {
        fetchMyBookings(1);
    }, []);

    const displayedBookings = bookings.filter(b => {
        if (activeTab === "upcoming") {
            return b.status === "PENDING" || b.status === "DEPOSITED";
        } else {
            return b.status === "COMPLETED" || b.status === "CANCELLED";
        }
    });

    return (
        <div className="booking-history-container">
            <div className="booking-history-wrapper">
                <PageHeader header="My Bookings" text="View and manage your court bookings" />

                <BookingTabs activeTab={activeTab} setActiveTab={setActiveTab} />

                {loading ? (
                    <div className="loading">
                        Loading...
                    </div>
                ) : (
                    <>
                        <div className="booking-list">
                            {displayedBookings.length === 0 ? (
                                <EmptyState text="bookings" />
                            ) : (
                                displayedBookings.map(booking => (
                                    <BookingCard
                                        key={booking.id}
                                        booking={booking}
                                        showCancel={activeTab === "upcoming"}
                                    />
                                ))
                            )}
                        </div>

                        <Pagination
                            currentPage={pagination?.current_page}
                            totalPages={pagination?.total_pages}
                            onPageChange={fetchMyBookings}
                        />
                    </>
                )}
            </div>
        </div>
    );
}