import { Button } from "../../../../components/common/Button.jsx";
import { Badge } from "../../../../components/common/Badge.jsx";
import { ArrowLeft } from "lucide-react";

export function BookingHeader({ onBack, name }) {
    return (
        <div className="booking-header">
            <Button onClick={onBack} className="back-btn">
                <ArrowLeft size={16}/> Back
            </Button>

            <h1 className="title">{name}</h1>

            <div className="badges">
                <Badge variant="info">Football</Badge>
                <Badge variant="success">Available</Badge>
            </div>
        </div>
    );
}