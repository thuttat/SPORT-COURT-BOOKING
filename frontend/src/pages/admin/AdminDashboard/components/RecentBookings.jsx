import React from "react";
import { Card, CardContent } from "../../../../components/common/Card.jsx";
import { EmptyState } from "../../../../components/common/EmptyState.jsx";
import { sportIcons } from "../../../../utils/constants.jsx";
import { formatDate } from "../../../../utils/formatters.js";

export function RecentBookings({ bookings }) {
    return (
        <Card>
            <CardContent className="content">
                <h3>Recent Bookings</h3>

                <div className="recent-list">
                    {bookings.length === 0 ? (
                        <EmptyState text="bookings" />
                    ) : (
                        bookings.slice(0, 5).map((booking) => (
                            <div key={booking.id} className="recent-item">
                                <div className={`recent-icon ${booking.sport}`}>
                                    {sportIcons[booking.sport]}
                                </div>

                                <div className="recent-info">
                                    <p>{booking.fieldName}</p>
                                    <span>{formatDate(booking.date)}</span>
                                </div>

                                <div className="recent-time">
                                    {booking.timeSlots.length}h
                                </div>
                            </div>
                        ))
                    )}
                </div>
            </CardContent>
        </Card>
    );
}