import React from "react";
import { Card, CardContent } from "../../../../components/common/Card.jsx";
import { EmptyState } from "../../../../components/common/EmptyState.jsx";
import {renderStatusBadge, sportIcons} from "../../../../utils/constants.jsx";
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
                        bookings.map((booking) => (
                            <div key={booking.id} className="recent-item">
                                <div className="recent-info">
                                    <p>{booking.field_name}</p>
                                    <span>{formatDate(booking.booking_date)} • 🕒 {booking.time_slot}</span>
                                </div>

                                <div>
                                    {renderStatusBadge(booking.status)}
                                </div>
                            </div>
                        ))
                    )}
                </div>
            </CardContent>
        </Card>
    );
}