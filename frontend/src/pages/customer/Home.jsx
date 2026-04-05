import { useState } from "react";
import {CourtCard} from "./components/CourtCard.jsx";
import {FilterBar} from "./components/FilterBar.jsx";
import {EmptyState} from "./components/EmptyState.jsx";
import {PageHeader} from "../../components/common/PageHeader.jsx";
import "./styles/home.css";

export function Home() {
    const courts = [
        {
            "id": "c1",
            "name": "Sân bóng đá Mini A",
            "sport": "football",
            "location": "Quận 1",
            "price": 200000,
            "rating": 4.5,
            "available": true
        },
        {
            "id": "c2",
            "name": "Sân cầu lông VIP 1",
            "sport": "badminton",
            "location": "Quận 3",
            "price": 80000,
            "rating": 4.8,
            "available": true
        },
        {
            "id": "c3",
            "name": "Sân cầu lông TTTM",
            "sport": "badminton",
            "location": "Quận 8",
            "price": 45000,
            "rating": 4.9,
            "available": false
        },
        {
            "id": "c4",
            "name": "Sân tennis trung tâm",
            "sport": "tennis",
            "location": "Quận 7",
            "price": 300000,
            "rating": 4.6,
            "available": true
        },
        {
            "id": "c5",
            "name": "Sân tennis Hồ Tùng Mậu",
            "sport": "tennis",
            "location": "Quận 1",
            "price": 500000,
            "rating": 4.7,
            "available": true
        }
    ];

    const [search, setSearch] = useState("");
    const [selectedSport, setSelectedSport] = useState("all");

    const filteredFields = courts.filter(court => {
        const matchSearch = court.name
            .toLowerCase()
            .includes(search.toLowerCase());

        const matchSport =
            selectedSport === "all" || court.sport === selectedSport;

        return matchSearch && matchSport;
    });

    const getToday = () => {
        const today = new Date();
        return today.toISOString().split("T")[0];
    };

    const [selectedDate, setSelectedDate] = useState(getToday());

    return (
        <div className="container">
            <PageHeader header="Find Your Field" text="Book your favorite sports court in just a few clicks" />

            <FilterBar
                search={search}
                setSearch={setSearch}
                selectedSport={selectedSport}
                setSelectedSport={setSelectedSport}
                selectedDate={selectedDate}
                setSelectedDate={setSelectedDate}
            />

            <div className="grid">
                {filteredFields.map(court => (
                    <CourtCard key={court.id} court={court} />
                ))}
            </div>

            {filteredFields.length === 0 && <EmptyState />}
        </div>
    );
}