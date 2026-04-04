import { Button } from "../../../components/common/Button.jsx";

export function FilterBar({
                              search,
                              setSearch,
                              selectedSport,
                              setSelectedSport,
                              selectedDate,
                              setSelectedDate
                          }) {
    return (
        <div className="filter-bar">
            <input
                type="text"
                placeholder="Search fields..."
                className="input"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
            />

            <div className="filter-row">
                <div className="filter-buttons">
                    <Button
                        className={selectedSport === "all" ? "btn-primary" : ""}
                        onClick={() => setSelectedSport("all")}
                    >
                        All
                    </Button>

                    <Button
                        className={selectedSport === "football" ? "btn-primary" : ""}
                        onClick={() => setSelectedSport("football")}
                    >
                        ⚽ Football
                    </Button>

                    <Button
                        className={selectedSport === "badminton" ? "btn-primary" : ""}
                        onClick={() => setSelectedSport("badminton")}
                    >
                        🏸 Badminton
                    </Button>

                    <Button
                        className={selectedSport === "tennis" ? "btn-primary" : ""}
                        onClick={() => setSelectedSport("tennis")}
                    >
                        🎾 Tennis
                    </Button>
                </div>

                <input
                    type="date"
                    className="input date-input"
                    value={selectedDate}
                    onChange={(e) => setSelectedDate(e.target.value)}
                />
            </div>
        </div>
    );
}