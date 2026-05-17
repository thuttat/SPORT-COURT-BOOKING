import React from "react";
import { Button } from "../../../../components/common/Button.jsx";
import { X } from "lucide-react";
import { renderStatusBadge, sportIcons } from "../../../../utils/constants.jsx";
import { formatCurrency, formatDate, capitalizeFirstLetter } from "../../../../utils/formatters.js";

export function BookingModal({ booking, onClose }) {
    if (!booking) return null;

    return (
        <div className="modal-overlay" onClick={onClose}>
            <div className="modal-content" onClick={(e) => e.stopPropagation()}>
                <div className="modal-header">
                    <h3>Booking Details #{booking.id}</h3>
                    <Button variant="ghost" size="sm" onClick={onClose} style={{ padding: '4px' }}>
                        <X size={20} color="#64748b" />
                    </Button>
                </div>

                <div className="modal-body">
                    <div className="detail-row">
                        <span className="detail-label">Customer Name</span>
                        <span className="detail-value">{booking.customer_name}</span>
                    </div>

                    <div className="detail-row">
                        <span className="detail-label">Field Name</span>
                        <span className="detail-value" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                            {sportIcons[booking.field_type?.toLowerCase()] || sportIcons[booking.field_type]} {booking.field_name}
                        </span>
                    </div>

                    <div className="detail-row">
                        <span className="detail-label">Sport Type</span>
                        <span className="detail-value">{capitalizeFirstLetter(booking.field_type)}</span>
                    </div>

                    <div className="detail-row">
                        <span className="detail-label">Booking Date</span>
                        <span className="detail-value">{formatDate(booking.booking_date)}</span>
                    </div>

                    <div className="detail-row">
                        <span className="detail-label">Time Slot</span>
                        <span className="detail-value">🕒 {booking.time_slot}</span>
                    </div>

                    <div className="detail-row">
                        <span className="detail-label">Status</span>
                        <span>{renderStatusBadge(booking.status)}</span>
                    </div>

                    <div className="detail-row">
                        <span className="detail-label">Created At</span>
                        <span className="detail-value" style={{ fontWeight: 'normal', color: '#64748b' }}>
                            {booking.created_at}
                        </span>
                    </div>

                    <div className="detail-row">
                        <span className="detail-label" style={{ fontSize: '16px', color: 'var(--foreground)', fontWeight: 600 }}>Total Amount</span>
                        <span className="detail-value total-price">
                            {formatCurrency(booking.total_price)}
                        </span>
                    </div>
                </div>
            </div>
        </div>
    );
}