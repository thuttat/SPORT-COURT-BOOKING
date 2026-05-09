import { Card, CardContent } from "../../../../components/common/Card.jsx";
import { Button } from "../../../../components/common/Button.jsx";
import { Badge } from "../../../../components/common/Badge.jsx";
import {useNavigate} from "react-router-dom";
import {renderStatusBadge, sportIcons} from "../../../../utils/constants.jsx";
import {capitalizeFirstLetter, formatCurrency, formatDate} from "../../../../utils/formatters.js";

export function BookingCard({ booking, showCancel }) {
    const navigate = useNavigate();
    const sport = booking.field_type ? booking.field_type.toLowerCase() : 'default';

    return (
        <Card className="booking-card">
            <CardContent className="content">
                <div className="booking-row">
                    <div className={`sport-icon ${sport}`}>
                        {sportIcons[sport]}
                    </div>

                    <div className="booking-info">
                        <div className="top">
                            <div className="title-row">
                                <h3 className="field-name">
                                    {booking.field_name}
                                </h3>
                                {renderStatusBadge(booking.status)}
                            </div>

                            <Badge variant="info">
                                {capitalizeFirstLetter(sport)}
                            </Badge>
                        </div>

                        <div className="meta">
                            <span>
                                🗓️ {formatDate(booking.booking_date)}
                            </span>

                            <span>
                                💰 {formatCurrency(booking.total_price)}
                            </span>
                        </div>

                        <div className="slots">
                            <Badge>{booking.time_slot}</Badge>
                        </div>
                    </div>

                    <div className="actions">
                        <Button onClick={() => navigate(`/booking/${booking.id}`)} className="btn-outline">
                            View
                        </Button>
                        {showCancel && booking.status === "PENDING" && (
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