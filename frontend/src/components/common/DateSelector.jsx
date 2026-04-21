import { Button } from "./Button.jsx";
import "../styles/dateSelector.css";

export function DateSelector({ dates, selectedDate, onSelect, allowPastDates = false }) {
    const today = new Date();
    today.setHours(0, 0, 0, 0);

    return (
        <div className="date-grid">
            {dates.map((date, i) => {
                const isActive = selectedDate === i;
                const checkDate = new Date(date);
                checkDate.setHours(0,0,0,0);
                const isDisabled = !allowPastDates && checkDate < today;

                return (
                    <Button
                        key={i}
                        onClick={() => !isDisabled && onSelect(i)}
                        className={`date-btn ${isActive ? "active" : ""} ${isDisabled ? "btn-disabled" : ""}`}
                        disabled={isDisabled}
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