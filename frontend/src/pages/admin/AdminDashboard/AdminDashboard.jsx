import React, { useEffect, useState } from "react";
import "./adminDashboard.css";
import { PageHeader } from "../../../components/common/PageHeader.jsx";
import { DashboardStats } from "./components/DashboardStats.jsx";
import { SportDistribution } from "./components/SportDistribution.jsx";
import { RecentBookings } from "./components/RecentBookings.jsx";
import {
    getChartSportRequest,
    getDashboardSummaryRequest,
    getRecentBookingsRequest
} from "../../../services/apis.js";

export function AdminDashboard() {
    const [summary, setSummary] = useState(null);
    const [chartData, setChartData] = useState([]);
    const [recentBookings, setRecentBookings] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchDashboardData = async () => {
            try {
                const [summaryRes, chartRes, recentRes] = await Promise.all([
                    getDashboardSummaryRequest(),
                    getChartSportRequest(),
                    getRecentBookingsRequest()
                ]);

                setSummary(summaryRes.data.data);
                setChartData(chartRes.data.data);
                setRecentBookings(recentRes.data.data);
            } catch (error) {
                console.error("Error fetching dashboard data: ", error);
            } finally {
                setLoading(false);
            }
        };
        fetchDashboardData();
    }, []);

    if (loading || !summary) {
        return <div className="admin-container loading">Loading...</div>;
    }

    return (
        <div className="admin-container">
            <div className="admin-wrapper">
                <PageHeader header="Admin Dashboard" text="Overview of your sports booking system"/>

                <DashboardStats summary={summary} />

                <div className="dashboard-grid">
                    <SportDistribution chartData={chartData} />

                    <RecentBookings bookings={recentBookings} />
                </div>
            </div>
        </div>
    );
}