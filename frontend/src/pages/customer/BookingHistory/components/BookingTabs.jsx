import { Button } from "../../../../components/common/Button.jsx";

export function BookingTabs({ activeTab, setActiveTab }) {
    return (
        <div className="tabs">
            <Button
                className={`tab-btn ${activeTab === "upcoming" ? "active" : ""}`}
                onClick={() => setActiveTab("upcoming")}
            >
                Upcoming
            </Button>

            <Button
                className={`tab-btn ${activeTab === "past" ? "active" : ""}`}
                onClick={() => setActiveTab("past")}
            >
                Past
            </Button>
        </div>
    );
}