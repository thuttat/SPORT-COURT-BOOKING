import { Card, CardContent } from "../../../components/common/Card.jsx";
import { Button } from "../../../components/common/Button.jsx";
import { Badge } from "../../../components/common/Badge.jsx";
import {useNavigate} from "react-router-dom";

const sportIcons = {
    football: "⚽",
    badminton: "🏸",
    tennis: "🎾"
};

export function BookingCard({ booking, showCancel }) {
    const navigate = useNavigate();

    return (
        <Card className="booking-card">
            <CardContent className="content">
                <div className="booking-row">
                    <div className={`sport-icon ${booking.sport}`}>
                        {sportIcons[booking.sport]}
                    </div>

                    <div className="booking-info">
                        <div className="top">
                            <div className="title-row">
                                <h3 className="field-name">
                                    {booking.courtName}
                                </h3>

                                {booking.status === "cancelled" && (
                                    <Badge variant="danger">Cancelled</Badge>
                                )}
                            </div>

                            <Badge variant="info">
                                {booking.sport}
                            </Badge>
                        </div>

                        <div className="meta">
                            <span>
                                🗓️ {new Date(booking.date).toLocaleDateString("en-US", {
                                weekday: "long",
                                year: "numeric",
                                month: "short",
                                day: "numeric"
                            })}
                            </span>

                            <span>
                                ⏰ {booking.timeSlots.length}{" "}
                                {booking.timeSlots.length === 1 ? "hour" : "hours"}
                            </span>
                        </div>

                        <div className="slots">
                            {booking.timeSlots.map(slot => (
                                <Badge key={slot}>{slot}</Badge>
                            ))}
                        </div>
                    </div>

                    <div className="actions">
                        <Button onClick={() => navigate(`/booking/${booking.id}`)}>
                            View
                        </Button>
                        {showCancel && (
                            <Button className="btn-danger">
                                Cancel
                            </Button>
                        )}
                    </div>
                </div>
            </CardContent>
        </Card>
    );
}