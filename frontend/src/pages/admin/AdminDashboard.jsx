import React from "react";
import { Card, CardContent } from "../../components/common/Card.jsx";
import { LayoutGrid, Calendar, TrendingUp, MapPin } from "lucide-react";
import { format, isToday } from "date-fns";
import "./adminDashboard.css";
import {useBooking} from "../../services/booking/useBooking.js";

export function AdminDashboard() {
    const bookingData = useBooking() || {};
    const fields = bookingData.fields || [];
    const bookings = bookingData.bookings || [];

    const todayBookings = bookings.filter(
        (b) => isToday(new Date(b.date)) && b.status !== "cancelled"
    );

    const activeFields = fields.filter((f) => f.available);
    const totalBookings = bookings.filter((b) => b.status !== "cancelled").length;

    const sportCounts = fields.reduce((acc, field) => {
        acc[field.sport] = (acc[field.sport] || 0) + 1;
        return acc;
    }, {});

    return (
        <div className="admin-container">
            <div className="admin-wrapper">
                <div className="admin-header">
                    <h1>Admin Dashboard</h1>
                    <p>Overview of your sports booking system</p>
                </div>

                <div className="stats-grid">
                    <Card className="stat-card blue">
                        <CardContent className="content">
                            <div className="stat-top">
                                <div className="icon-box blue">
                                    <MapPin size={22} />
                                </div>
                                <TrendingUp size={18} />
                            </div>
                            <div className="stat-value">{fields.length}</div>
                            <div className="stat-label">Total Fields</div>
                        </CardContent>
                    </Card>

                    <Card className="stat-card green">
                        <CardContent className="content">
                            <div className="stat-top">
                                <div className="icon-box green">
                                    <LayoutGrid size={22} />
                                </div>
                                <TrendingUp size={18} />
                            </div>
                            <div className="stat-value">{activeFields.length}</div>
                            <div className="stat-label">Active Fields</div>
                        </CardContent>
                    </Card>

                    <Card className="stat-card purple">
                        <CardContent className="content">
                            <div className="stat-top">
                                <div className="icon-box purple">
                                    <Calendar size={22} />
                                </div>
                                <TrendingUp size={18} />
                            </div>
                            <div className="stat-value">{todayBookings.length}</div>
                            <div className="stat-label">Bookings Today</div>
                        </CardContent>
                    </Card>

                    <Card className="stat-card primary">
                        <CardContent className="content">
                            <div className="stat-top">
                                <div className="icon-box primary">
                                    <TrendingUp size={22} />
                                </div>
                                <TrendingUp size={18} />
                            </div>
                            <div className="stat-value">{totalBookings}</div>
                            <div className="stat-label">Total Bookings</div>
                        </CardContent>
                    </Card>
                </div>

                <div className="dashboard-grid">
                    <Card>
                        <CardContent className="content">
                            <h2>Fields by Sport</h2>

                            <div className="sport-list">
                                {Object.entries(sportCounts).map(([sport, count]) => (
                                    <div key={sport} className="sport-item">
                                        <div className="sport-row">
                                            <div className="sport-name">
                                                <span className="sport-icon">
                                                    {sport === "football" && "⚽"}
                                                    {sport === "badminton" && "🏸"}
                                                    {sport === "tennis" && "🎾"}
                                                </span>
                                                <span className="capitalize">{sport}</span>
                                            </div>
                                            <span className="sport-count">{count}</span>
                                        </div>

                                        <div className="progress">
                                            <div
                                                className={`progress-bar ${sport}`}
                                                style={{
                                                    width: `${fields.length ? (count / fields.length) * 100 : 0}%`,
                                                }}
                                            />
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </CardContent>
                    </Card>

                    <Card>
                        <CardContent className="content">
                            <h2>Recent Bookings</h2>
                            <div className="recent-list">
                                {bookings.slice(0, 5).map((booking) => (
                                    <div key={booking.id} className="recent-item">
                                        <div className={`recent-icon ${booking.sport}`}>
                                            {booking.sport === "football" && "⚽"}
                                            {booking.sport === "badminton" && "🏸"}
                                            {booking.sport === "tennis" && "🎾"}
                                        </div>

                                        <div className="recent-info">
                                            <p>{booking.fieldName}</p>
                                            <span>
                                                {format(new Date(booking.date), "MMM dd, yyyy")}
                                            </span>
                                        </div>

                                        <div className="recent-time">
                                            {booking.timeSlots.length}h
                                        </div>
                                    </div>
                                ))}

                                {bookings.length === 0 && (
                                    <div className="empty">
                                        <Calendar size={40} />
                                        <p>No bookings yet</p>
                                    </div>
                                )}
                            </div>
                        </CardContent>
                    </Card>
                </div>
            </div>
        </div>
    );
}