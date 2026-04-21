import {Card, CardContent} from "../../../../components/common/Card.jsx";
import { Badge } from "../../../../components/common/Badge.jsx";
import { Button } from "../../../../components/common/Button.jsx";

export function BookingSummary({ date, slots, className = "" }) {
    return (
        <div className={`summary ${className}`}>
            <Card className="summary-card">
                <CardContent className="content">
                    <h3>Summary</h3>

                    <div className="summary-row">
                        <span>Date</span>
                        <span>{date.toLocaleDateString('en-GB')}</span>
                    </div>

                    <div className="summary-row">
                        <span>Slots</span>
                        <span>{slots.length}</span>
                    </div>

                    {slots.length > 0 && (
                        <div className="selected-list">
                            {slots.map(s => (
                                <Badge key={s} variant="info">{s}</Badge>
                            ))}
                        </div>
                    )}

                    <Button
                        className="btn-primary btn-full"
                        disabled={slots.length === 0}
                    >
                        Confirm Booking
                    </Button>
                </CardContent>
            </Card>
        </div>
    );
}