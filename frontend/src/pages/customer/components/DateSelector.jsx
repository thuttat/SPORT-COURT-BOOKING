import { Button } from "../../../components/common/Button.jsx";

export function DateSelector({ dates, selectedDate, onSelect }) {
    return (
        <div className="date-grid">
            {dates.map((date, i) => {
                const isActive = selectedDate === i;

                return (
                    <Button
                        key={i}
                        onClick={() => onSelect(i)}
                        className={`date-btn ${isActive ? "active" : ""}`}
                    >
                        <div>{date.getDate()}</div>
                        <small>
                            {date.toLocaleDateString("vi-VN", { weekday: "short" })}
                        </small>
                    </Button>
                );
            })}
        </div>
    );
}