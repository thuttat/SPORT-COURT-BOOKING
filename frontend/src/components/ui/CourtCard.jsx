import "./CourtCard.css";
import {Button} from "./Button.jsx";

export function CourtCard({ court }) {
    const sportIcons = {
        football: "⚽",
        badminton: "🏸",
        tennis: "🎾"
    };

    return (
        <div className="court-card">

            {/* IMAGE / ICON */}
            <div className={`court-image ${court.sport}`}>
                {sportIcons[court.sport]}
            </div>

            {/* BODY */}
            <div className="court-body">

                {/* HEADER */}
                <div className="court-header">
                    <h3 className="court-name">{court.name}</h3>

                    {court.available ? (
                        <span className="badge badge-available">Available</span>
                    ) : (
                        <span className="badge badge-booked">Full</span>
                    )}
                </div>

                {/* INFO */}
                <div className="court-info">
                    <div className="info-row">
                        <span>🏟️</span>
                        <span>{court.sport}</span>
                    </div>

                    <div className="info-row">
                        <span>📍</span>
                        <span>{court.location}</span>
                    </div>
                </div>

                {/* PRICE + RATING */}
                <div className="court-meta">
                    <div>
                        <div className="text-muted small">Price</div>
                        <div className="price">
                            {court.price.toLocaleString()}₫
                            <span className="text-muted small"> /h</span>
                        </div>
                    </div>

                    <div className="rating">
                        <div className="text-muted small">Rating</div>
                        <div>⭐ {court.rating}</div>
                    </div>
                </div>

                {/* BUTTON */}
                {court.available ? (
                    <Button className="btn-primary btn-full">
                        Book Now
                    </Button>
                ) : (
                    <button className="btn btn-disabled" disabled>
                        Unavailable
                    </button>
                )}

            </div>
        </div>
    );
}