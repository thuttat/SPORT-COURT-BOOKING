import { Button } from "../../../components/common/Button.jsx";

export function TimeSlotGrid({ slots, selectedSlots, onToggle }) {
    return (
        <div className="slot-grid">
            {slots.map(slot => {
                const isSelected = selectedSlots.includes(slot);

                return (
                    <Button
                        key={slot}
                        onClick={() => onToggle(slot)}
                        className={`slot ${isSelected ? "selected" : ""}`}
                    >
                        {slot}
                    </Button>
                );
            })}
        </div>
    );
}