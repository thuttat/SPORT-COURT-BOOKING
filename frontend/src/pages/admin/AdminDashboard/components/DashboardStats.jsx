import React from "react";
import { Card, CardContent } from "../../../../components/common/Card.jsx";
import { LayoutGrid, Calendar, TrendingUp, MapPin } from "lucide-react";
import { isToday } from "date-fns";

export function DashboardStats({ summary }) {
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

                    <div className="stat-value">{summary.total_fields}</div>

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

                    <div className="stat-value">{summary.active_fields}</div>

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

                    <div className="stat-value">{summary.bookings_today}</div>

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

                    <div className="stat-value">{summary.total_bookings}</div>

                    <div className="stat-label">Total Bookings</div>
                </CardContent>
            </Card>
        </div>
    );
}