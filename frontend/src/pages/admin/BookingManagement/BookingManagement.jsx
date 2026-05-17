import React, { useState } from "react";
import { PageHeader } from "../../../components/common/PageHeader.jsx";
import { Card } from "../../../components/common/Card.jsx";
import { Button } from "../../../components/common/Button.jsx";
import { EmptyState } from "../../../components/common/EmptyState.jsx";
import { Pagination } from "../../../components/common/Pagination.jsx";
import { Check, X, Eye } from "lucide-react";
import { renderStatusBadge, sportIcons } from "../../../utils/constants.jsx";
import { formatCurrency, formatDate, capitalizeFirstLetter } from "../../../utils/formatters.js";
import "./bookingManagement.css";
import {Table, TableBody, TableCell, TableHead, TableHeader, TableRow} from "../../../components/common/Table.jsx";

const MOCK_BOOKINGS = [
    {
        id: 101,
        customer_name: "Nguyễn Văn A",
        field_name: "Sân bóng đá Mini A",
        field_type: "football",
        booking_date: "2026-05-20",
        time_slot: "17:00 - 18:30",
        total_price: 300000,
        status: "PENDING",
        created_at: "2026-05-15 10:30:00"
    },
    {
        id: 102,
        customer_name: "Trần Thị B",
        field_name: "Sân cầu lông VIP 1",
        field_type: "badminton",
        booking_date: "2026-05-21",
        time_slot: "19:00 - 20:30",
        total_price: 120000,
        status: "CONFIRMED",
        created_at: "2026-05-16 08:15:00"
    },
    {
        id: 103,
        customer_name: "Lê Hoàng C",
        field_name: "Sân tennis trung tâm",
        field_type: "tennis",
        booking_date: "2026-05-10",
        time_slot: "06:00 - 08:00",
        total_price: 600000,
        status: "COMPLETED",
        created_at: "2026-05-08 14:00:00"
    },
    {
        id: 104,
        customer_name: "Phạm Văn D",
        field_name: "Sân bóng đá Mini B",
        field_type: "football",
        booking_date: "2026-05-18",
        time_slot: "20:00 - 21:30",
        total_price: 300000,
        status: "CANCELLED",
        created_at: "2026-05-14 09:20:00"
    },
    {
        id: 105,
        customer_name: "Phạm Văn E",
        field_name: "Sân bóng đá Mini B",
        field_type: "football",
        booking_date: "2026-05-19",
        time_slot: "20:00 - 21:30",
        total_price: 300000,
        status: "CANCELLED",
        created_at: "2026-05-14 09:20:00"
    },
    {
        id: 106,
        customer_name: "Phạm Văn F",
        field_name: "Sân bóng đá Mini C",
        field_type: "football",
        booking_date: "2026-05-12",
        time_slot: "20:00 - 21:30",
        total_price: 300000,
        status: "CANCELLED",
        created_at: "2026-05-14 09:20:00"
    }
];

const BOOKING_TABS = ["ALL", "PENDING", "CONFIRMED", "COMPLETED", "CANCELLED"];

export function BookingManagement() {
    const [bookings, setBookings] = useState(MOCK_BOOKINGS);
    const [activeTab, setActiveTab] = useState("ALL");
    const [currentPage, setCurrentPage] = useState(1);
    const [selectedBooking, setSelectedBooking] = useState(null);
    const ITEMS_PER_PAGE = 5;

    const filteredBookings = bookings.filter(b =>
        activeTab === "ALL" ? true : b.status === activeTab
    );

    const totalPages = Math.ceil(filteredBookings.length / ITEMS_PER_PAGE);
    const displayedBookings = filteredBookings.slice(
        (currentPage - 1) * ITEMS_PER_PAGE,
        currentPage * ITEMS_PER_PAGE
    );

    const handleConfirm = (id) => {
        if(window.confirm("Are you sure you want to confirm this court booking?")) {
            setBookings(prev => prev.map(b => b.id === id ? { ...b, status: "CONFIRMED" } : b));
        }
    };

    const handleCancel = (id) => {
        if(window.confirm("Are you sure you want to cancel this court booking? Customer will be notified.")) {
            setBookings(prev => prev.map(b => b.id === id ? { ...b, status: "CANCELLED" } : b));
        }
    };

    return (
        <div className="booking-management-container">
            <div className="booking-management-wrapper">
                <PageHeader header="Booking Management" text="View, approve, and manage customer bookings" />

                <div className="management-tabs">
                    {BOOKING_TABS.map(tab => (
                        <Button
                            className={`tab-btn ${activeTab === tab ? "active" : ""}`}
                            onClick={() => {
                                setActiveTab(tab);
                                setCurrentPage(1);
                            }}
                        >
                            {capitalizeFirstLetter(tab.toLowerCase())}
                        </Button>
                    ))}
                </div>

                <Card>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Customer</TableHead>
                                <TableHead>Field Info</TableHead>
                                <TableHead>Schedule</TableHead>
                                <TableHead>Amount</TableHead>
                                <TableHead>Status</TableHead>
                                <TableHead>Actions</TableHead>
                            </TableRow>
                        </TableHeader>

                        <TableBody>
                            {displayedBookings.length === 0 ? (
                                <TableRow>
                                    <TableCell colSpan={6} style={{ padding: 0 }}>
                                        <EmptyState text="bookings in this category" />
                                    </TableCell>
                                </TableRow>
                            ) : (
                                displayedBookings.map((booking) => (
                                    <TableRow key={booking.id}>
                                        <TableCell>
                                            <div className="customer-info">
                                                <span className="customer-name">{booking.customer_name}</span>
                                                <span className="booking-id">ID: #{booking.id}</span>
                                            </div>
                                        </TableCell>

                                        <TableCell>
                                            <div className="field-info">
                                                <div style={{ fontSize: '24px' }}>{sportIcons[booking.field_type]}</div>
                                                <div className="customer-info">
                                                    <span style={{ fontWeight: 500 }}>{booking.field_name}</span>
                                                    <span className="booking-id">{capitalizeFirstLetter(booking.field_type)}</span>
                                                </div>
                                            </div>
                                        </TableCell>

                                        <TableCell>
                                            <div className="schedule-info">
                                                <span style={{ fontWeight: 500 }}>{formatDate(booking.booking_date)}</span>
                                                <span style={{ color: '#64748b' }}>🕒 {booking.time_slot}</span>
                                            </div>
                                        </TableCell>

                                        <TableCell>
                                            <span style={{ fontWeight: 600, color: 'var(--primary)' }}>
                                                {formatCurrency(booking.total_price)}
                                            </span>
                                        </TableCell>

                                        <TableCell>
                                            {renderStatusBadge(booking.status)}
                                        </TableCell>

                                        <TableCell>
                                            <div className="table-actions">
                                                {booking.status === "PENDING" && (
                                                    <Button size="sm" className="btn-icon btn-success" onClick={() => handleConfirm(booking.id)}>
                                                        <Check size={16} /> Confirm
                                                    </Button>
                                                )}
                                                {(booking.status === "PENDING" || booking.status === "CONFIRMED") && (
                                                    <Button size="sm" variant="outline" className="btn-icon btn-danger" onClick={() => handleCancel(booking.id)}>
                                                        <X size={16} /> Cancel
                                                    </Button>
                                                )}
                                                {(booking.status === "CANCELLED" || booking.status === "COMPLETED") && (
                                                    <Button size="sm" variant="ghost" className="btn-icon" onClick={() => setSelectedBooking(booking)}>
                                                        <Eye size={16} /> View
                                                    </Button>
                                                )}
                                            </div>
                                        </TableCell>
                                    </TableRow>
                                ))
                            )}
                        </TableBody>
                    </Table>

                    <div className="table-pagination">
                        <Pagination
                            currentPage={currentPage}
                            totalPages={totalPages}
                            onPageChange={(page) => setCurrentPage(page)}
                        />
                    </div>
                </Card>
            </div>

            {selectedBooking && (
                <div className="modal-overlay" onClick={() => setSelectedBooking(null)}>
                    <div className="modal-content" onClick={(e) => e.stopPropagation()}>
                        <div className="modal-header">
                            <h3>Booking Details #{selectedBooking.id}</h3>
                            <Button variant="ghost" size="sm" onClick={() => setSelectedBooking(null)} style={{ padding: '4px' }}>
                                <X size={20} color="#64748b" />
                            </Button>
                        </div>

                        <div className="modal-body">
                            <div className="detail-row">
                                <span className="detail-label">Customer Name</span>
                                <span className="detail-value">{selectedBooking.customer_name}</span>
                            </div>

                            <div className="detail-row">
                                <span className="detail-label">Field Name</span>
                                <span className="detail-value" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                                    {sportIcons[selectedBooking.field_type]} {selectedBooking.field_name}
                                </span>
                            </div>

                            <div className="detail-row">
                                <span className="detail-label">Sport Type</span>
                                <span className="detail-value">{capitalizeFirstLetter(selectedBooking.field_type)}</span>
                            </div>

                            <div className="detail-row">
                                <span className="detail-label">Booking Date</span>
                                <span className="detail-value">{formatDate(selectedBooking.booking_date)}</span>
                            </div>

                            <div className="detail-row">
                                <span className="detail-label">Time Slot</span>
                                <span className="detail-value">🕒 {selectedBooking.time_slot}</span>
                            </div>

                            <div className="detail-row">
                                <span className="detail-label">Status</span>
                                <span>{renderStatusBadge(selectedBooking.status)}</span>
                            </div>

                            <div className="detail-row">
                                <span className="detail-label">Created At</span>
                                <span className="detail-value" style={{ fontWeight: 'normal', color: '#64748b' }}>
                                    {selectedBooking.created_at}
                                </span>
                            </div>

                            <div className="detail-row" style={{ marginTop: '8px', paddingTop: '16px', borderTop: '1px solid #e2e8f0', borderBottom: 'none' }}>
                                <span className="detail-label" style={{ fontSize: '16px', color: 'var(--foreground)', fontWeight: 600 }}>Total Amount</span>
                                <span className="detail-value" style={{ fontSize: '20px', color: 'var(--primary)' }}>
                                    {formatCurrency(selectedBooking.total_price)}
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}