import React from "react";
import { Button } from "../../../../components/common/Button.jsx";
import { capitalizeFirstLetter } from "../../../../utils/formatters.js";

export function BookingTabs({ tabs, activeTab, onTabChange }) {
    return (
        <div className="management-tabs">
            {tabs.map(tab => (
                <Button
                    key={tab}
                    className={`tab-btn ${activeTab === tab ? "active" : ""}`}
                    onClick={() => onTabChange(tab)}
                >
                    {capitalizeFirstLetter(tab.toLowerCase())}
                </Button>
            ))}
        </div>
    );
}