import React from "react";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "../../../../components/common/Table.jsx";
import { EmptyState } from "../../../../components/common/EmptyState.jsx";
import { Pagination } from "../../../../components/common/Pagination.jsx";
import { Button } from "../../../../components/common/Button.jsx";
import {Check, X, Eye, CheckCircle} from "lucide-react";
import { renderStatusBadge, sportIcons } from "../../../../utils/constants.jsx";
import { formatCurrency, formatDate, capitalizeFirstLetter } from "../../../../utils/formatters.js";

export function BookingTable({
                                 loading, bookings, currentPage, totalPages,
                                 onPageChange, onConfirm, onCancel, onComplete, onView
                             }) {
    if (loading) {
        return <div className="loading">Loading...</div>;
    }

    return (
        <>
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
                    {bookings.length === 0 ? (
                        <TableRow>
                            <TableCell colSpan={6} style={{ padding: 0 }}>
                                <EmptyState text="bookings in this category" />
                            </TableCell>
                        </TableRow>
                    ) : (
                        bookings.map((booking) => (
                            <TableRow key={booking.id}>
                                <TableCell>
                                    <div className="customer-info">
                                        <span className="customer-name">{booking.customer_name}</span>
                                        <span className="booking-id">ID: #{booking.id}</span>
                                    </div>
                                </TableCell>

                                <TableCell>
                                    <div className="field-info">
                                        <div style={{ fontSize: '24px' }}>
                                            {sportIcons[booking.field_type?.toLowerCase()] || sportIcons[booking.field_type]}
                                        </div>
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
                                    <span className="total-price">
                                        {formatCurrency(booking.total_price)}
                                    </span>
                                </TableCell>

                                <TableCell>
                                    {renderStatusBadge(booking.status)}
                                </TableCell>

                                <TableCell>
                                    <div className="table-actions">
                                        {booking.status === "PENDING" && (
                                            <Button className="btn-icon btn-primary" onClick={() => onConfirm(booking.id)}>
                                                <Check size={16} /> Confirm
                                            </Button>
                                        )}
                                        {booking.status === "CONFIRMED" && (
                                            <Button className="btn-icon btn-complete" onClick={() => onComplete(booking.id)}>
                                                <CheckCircle size={16} /> Complete
                                            </Button>
                                        )}
                                        {(booking.status === "PENDING" || booking.status === "CONFIRMED") && (
                                            <Button className="btn-icon btn-danger" onClick={() => onCancel(booking.id)}>
                                                <X size={16} /> Cancel
                                            </Button>
                                        )}
                                        {(booking.status === "CANCELLED" || booking.status === "COMPLETED") && (
                                            <Button className="btn-icon btn-outline" onClick={() => onView(booking)}>
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

            {bookings.length > 0 && (
                <div className="table-pagination">
                    <Pagination
                        currentPage={currentPage}
                        totalPages={totalPages}
                        onPageChange={onPageChange}
                    />
                </div>
            )}
        </>
    );
}