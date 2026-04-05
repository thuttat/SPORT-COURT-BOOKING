import { useParams, useNavigate } from "react-router-dom";
import { Card, CardContent } from "../../components/common/Card.jsx";
import { Button } from "../../components/common/Button.jsx";
import { Badge } from "../../components/common/Badge.jsx";
import {ArrowLeft} from "lucide-react";

export function BookingDetails() {
    const { id } = useParams();
    const navigate = useNavigate();

    const booking = {
        id,
        fieldName: "Sân bóng đá Mini A",
        sport: "football",
        date: "2026-04-10",
        timeSlots: ["08:00", "09:00"],
        status: "upcoming"
    };

    return (
        <div className="container">
            <Button onClick={() => navigate(-1)}
                    className="back-btn"
                    style={{marginBottom: "8px"}}
            >
                <ArrowLeft size={16}/> Back
            </Button>

            <Card>
                <CardContent>
                    <h2>{booking.fieldName}</h2>
                    <Badge>{booking.sport}</Badge>

                    <p>Date: {booking.date}</p>
                    <p>Slots:</p>

                    <div style={{ display: "flex", gap: "8px" }}>
                        {booking.timeSlots.map(slot => (
                            <Badge key={slot}>{slot}</Badge>
                        ))}
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}