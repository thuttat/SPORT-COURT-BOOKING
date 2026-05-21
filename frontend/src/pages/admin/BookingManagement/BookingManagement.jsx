import React, {useEffect, useState} from "react";
import { PageHeader } from "../../../components/common/PageHeader.jsx";
import { Card } from "../../../components/common/Card.jsx";
import "./bookingManagement.css";
import {useBooking} from "../../../services/booking/useBooking.js";
import {BookingTabs} from "./components/BookingTabs.jsx";
import {BookingTable} from "./components/BookingTable.jsx";
import {BookingModal} from "./components/BookingModal.jsx";

const BOOKING_TABS = ["ALL", "PENDING", "CONFIRMED", "COMPLETED", "CANCELLED"];

export function BookingManagement() {
    const { adminBookings, adminLoading, adminTotalPages, fetchAdminBookings, updateBookingStatus } = useBooking();
    const [activeTab, setActiveTab] = useState("ALL");
    const [currentPage, setCurrentPage] = useState(1);
    const [selectedBooking, setSelectedBooking] = useState(null);

    useEffect(() => {
        fetchAdminBookings(currentPage, activeTab);
    }, [currentPage, activeTab]);

    const handleConfirm = async (id) => {
        if(window.confirm("Are you sure you want to confirm this court booking?")) {
            try {
                await updateBookingStatus(id, "CONFIRMED");
                alert("Booking confirmed successfully!");
                fetchAdminBookings(currentPage, activeTab);
            } catch (error) {
                alert(error.message);
            }
        }
    };

    const handleComplete = async (id) => {
        if(window.confirm("Are you sure you want to mark this booking as completed?")) {
            try {
                await updateBookingStatus(id, "COMPLETED");
                alert("Booking marked as completed successfully!");
                fetchAdminBookings(currentPage, activeTab);
            } catch (error) {
                alert(error.message);
            }
        }
    };

    const handleCancel = async (id) => {
        if(window.confirm("Are you sure you want to cancel this court booking? Customer will be notified.")) {
            try {
                await updateBookingStatus(id, "CANCELLED");
                alert("Booking cancelled successfully!");
                fetchAdminBookings(currentPage, activeTab);
            } catch (error) {
                alert(error.message);
            }
        }
    };

    const handleTabChange = (tab) => {
        setActiveTab(tab);
        setCurrentPage(1);
    };

    return (
        <div className="booking-management-container">
            <div className="booking-management-wrapper">
                <PageHeader header="Booking Management" text="View, approve, and manage customer bookings" />

                <BookingTabs
                    tabs={BOOKING_TABS}
                    activeTab={activeTab}
                    onTabChange={handleTabChange}
                />

                <Card>
                    <BookingTable
                        loading={adminLoading}
                        bookings={adminBookings}
                        currentPage={currentPage}
                        totalPages={adminTotalPages}
                        onPageChange={(page) => setCurrentPage(page)}
                        onConfirm={handleConfirm}
                        onCancel={handleCancel}
                        onComplete={handleComplete}
                        onView={(booking) => setSelectedBooking(booking)}
                    />
                </Card>
            </div>

            <BookingModal
                booking={selectedBooking}
                onClose={() => setSelectedBooking(null)}
            />
        </div>
    );
}