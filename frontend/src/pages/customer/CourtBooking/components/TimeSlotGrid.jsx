import { Button } from "../../../../components/common/Button.jsx";

export function TimeSlotGrid({ slots, selectedSlot, onToggle }) {
    if (!slots || slots.length === 0) {
        return <p style={{ color: "#64748b" }}>No available slots.</p>;
    }

    return (
        <div className="slot-grid">
            {slots.map(slot => {
                const isSelected = selectedSlot?.id === slot.id;

                return (
                    <Button
                        key={slot.id}
                        onClick={() => onToggle(slot)}
                        disabled={!slot.is_available}
                        className={`slot ${isSelected ? "selected" : ""} ${!slot.is_available ? "occupied" : ""}`}
                    >
                        {slot.display}
                    </Button>
                );
            })}
        </div>
    );
}