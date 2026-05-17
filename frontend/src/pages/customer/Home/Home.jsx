import {useEffect, useState} from "react";
import {CourtCard} from "./components/CourtCard.jsx";
import {FilterBar} from "./components/FilterBar.jsx";
import {PageHeader} from "../../../components/common/PageHeader.jsx";
import "./home.css";
import {EmptyState} from "../../../components/common/EmptyState.jsx";
import {formatTodayString} from "../../../utils/formatters.js";
import {Pagination} from "../../../components/common/Pagination.jsx";
import {useField} from "../../../services/field/useField.js";

export function Home() {
    const { fields, loadingFields, fetchFields } = useField();
    const [search, setSearch] = useState("");
    const [selectedSport, setSelectedSport] = useState("all");
    const [selectedDate, setSelectedDate] = useState(formatTodayString());
    const [currentPage, setCurrentPage] = useState(1);
    const ITEMS_PER_PAGE = 5;

    useEffect(() => {
        fetchFields(selectedDate);
        setCurrentPage(1);
    }, [selectedDate]);

    useEffect(() => {
        setCurrentPage(1);
    }, [search, selectedSport]);

    const filteredFields = fields.filter(court => {
        const matchSearch = court.name.toLowerCase().includes(search.toLowerCase());
        const sport = court.field_type ? court.field_type.toLowerCase() : "";
        const matchSport = selectedSport === "all" || sport === selectedSport;
        return matchSearch && matchSport;
    });

    const totalPages = Math.ceil(filteredFields.length / ITEMS_PER_PAGE);
    const displayedFields = filteredFields.slice(
        (currentPage - 1) * ITEMS_PER_PAGE,
        currentPage * ITEMS_PER_PAGE
    );

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

            {loadingFields ? (
                <div className="loading">Loading...</div>
            ) : (
                <>
                    <div className="grid">
                        {displayedFields.map(court => (
                            <CourtCard key={court.id} court={court} selectedDate={selectedDate} />
                        ))}
                    </div>

                    {displayedFields.length === 0 && <EmptyState text="courts" /> }

                    <Pagination
                        currentPage={currentPage}
                        totalPages={totalPages}
                        onPageChange={(page) => setCurrentPage(page)}
                    />
                </>
            )}
        </div>
    );
}