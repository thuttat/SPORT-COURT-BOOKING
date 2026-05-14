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
    const [currentPage, setCurrentPage] = useState(1);
    const ITEMS_PER_PAGE = 5;
    const { bookings, loading, fetchMyBookings } = useBooking();

    useEffect(() => {
        fetchMyBookings();
    }, []);

    useEffect(() => {
        setCurrentPage(1);
    }, [activeTab]);

    const filteredBookings = bookings.filter(b => {
        if (activeTab === "upcoming") {
            return b.status === "PENDING" || b.status === "DEPOSITED" || b.status === "CONFIRMED";
        } else {
            return b.status === "COMPLETED" || b.status === "CANCELLED";
        }
    });

    const totalPages = Math.ceil(filteredBookings.length / ITEMS_PER_PAGE);

    const displayedBookings = filteredBookings.slice(
        (currentPage - 1) * ITEMS_PER_PAGE,
        currentPage * ITEMS_PER_PAGE
    );

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
                            currentPage={currentPage}
                            totalPages={totalPages}
                            onPageChange={(newPage) => setCurrentPage(newPage)}
                        />
                    </>
                )}
            </div>
        </div>
    );
}