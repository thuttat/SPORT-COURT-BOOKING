import {Card, CardContent} from "../../../../components/common/Card.jsx";
import { Badge } from "../../../../components/common/Badge.jsx";
import { Button } from "../../../../components/common/Button.jsx";
import {formatDate} from "../../../../utils/formatters.js";

export function BookingSummary({ date, selectedSlot, className = "", onConfirm }) {
    return (
        <div className={`summary ${className}`}>
            <Card className="summary-card">
                <CardContent className="content">
                    <h3>Summary</h3>

                    <div className="summary-row">
                        <span>Date</span>
                        <span>{formatDate(date)}</span>
                    </div>

                    {selectedSlot && (
                        <div className="summary-row">
                            <span>Time</span>
                            <Badge variant="info">{selectedSlot.display}</Badge>
                        </div>
                    )}

                    <Button
                        className="btn-primary btn-full"
                        disabled={!selectedSlot}
                        onClick={onConfirm}
                    >
                        Confirm Booking
                    </Button>
                </CardContent>
            </Card>
        </div>
    );
}