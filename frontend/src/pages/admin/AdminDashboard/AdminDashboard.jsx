import React, { useEffect, useState } from "react";
import "./adminDashboard.css";
import { PageHeader } from "../../../components/common/PageHeader.jsx";
import { DashboardStats } from "./components/DashboardStats.jsx";
import { SportDistribution } from "./components/SportDistribution.jsx";
import { RecentBookings } from "./components/RecentBookings.jsx";
import {getMyFieldsRequest} from "../../../services/apis.js";

export function AdminDashboard() {
    const [fields, setFields] = useState([]);
    const [loadingFields, setLoadingFields] = useState(true);
    const bookings = [];

    useEffect(() => {
        const fetchDashboardData = async () => {
            try {
                let allFields = [];
                let page = 1;
                let hasNext = true;

                while (hasNext) {
                    const fieldsResponse = await getMyFieldsRequest(page);
                    allFields = [...allFields, ...fieldsResponse.data.data];
                    hasNext = fieldsResponse.data.pagination.has_next;
                    page++;
                }

                setFields(allFields);
            } catch (error) {
                console.error("Error fetching fields: ", error);
            } finally {
                setLoadingFields(false);
            }
        };
        fetchDashboardData();
    }, []);

    if (loadingFields) {
        return <div className="admin-container loading">Loading...</div>;
    }

    return (
        <div className="admin-container">
            <div className="admin-wrapper">
                <PageHeader header="Admin Dashboard" text="Overview of your sports booking system"/>

                <DashboardStats
                    fields={fields}
                    bookings={bookings}
                />

                <div className="dashboard-grid">
                    <SportDistribution fields={fields}/>

                    <RecentBookings bookings={bookings}/>
                </div>
            </div>
        </div>
    );
}