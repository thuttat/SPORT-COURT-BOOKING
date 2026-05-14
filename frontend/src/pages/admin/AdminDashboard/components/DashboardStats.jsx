import React from "react";
import { Card, CardContent } from "../../../../components/common/Card.jsx";
import { LayoutGrid, Calendar, TrendingUp, MapPin } from "lucide-react";
import { isToday } from "date-fns";

export function DashboardStats({ fields, bookings }) {
    const todayBookings = bookings.filter(
        (b) => isToday(new Date(b.date)) && b.status !== "cancelled"
    );

    const activeFields = fields.filter((f) => f.is_active);

    const totalBookings = bookings.filter(
        (b) => b.status !== "cancelled"
    ).length;

    return (
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
    );
}