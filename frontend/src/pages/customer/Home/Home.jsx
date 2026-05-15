import {useEffect, useState} from "react";
import {CourtCard} from "./components/CourtCard.jsx";
import {FilterBar} from "./components/FilterBar.jsx";
import {PageHeader} from "../../../components/common/PageHeader.jsx";
import "./home.css";
import {EmptyState} from "../../../components/common/EmptyState.jsx";
import {formatTodayString} from "../../../utils/formatters.js";
import {useField} from "../../../services/field/useField.js";
import {Pagination} from "../../../components/common/Pagination.jsx";

export function Home() {
    const {fields, loadingFields, fetchFields, fieldPagination} = useField();
    const [search, setSearch] = useState("");
    const [selectedSport, setSelectedSport] = useState("all");
    const [selectedDate, setSelectedDate] = useState(formatTodayString());

    const handlePageChange = (newPage) => {
        fetchFields(newPage, selectedDate);
    }

    useEffect(() => {
        fetchFields(1, selectedDate);
    }, [selectedDate]);

    const filteredFields = fields.filter(court => {
        const matchSearch = court.name
            .toLowerCase()
            .includes(search.toLowerCase());

        const sport = court.field_type ? court.field_type.toLowerCase() : "";
        const matchSport =
            selectedSport === "all" || sport === selectedSport;

        return matchSearch && matchSport;
    });

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
                        {filteredFields.map(court => (
                            <CourtCard key={court.id} court={court} selectedDate={selectedDate} />
                        ))}
                    </div>

                    {filteredFields.length === 0 && <EmptyState text="courts" /> }

                    <Pagination
                        currentPage={fieldPagination?.current_page}
                        totalPages={fieldPagination?.total_pages}
                        onPageChange={handlePageChange}
                    />
                </>
            )}
        </div>
    );
}