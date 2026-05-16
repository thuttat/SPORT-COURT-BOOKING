import { Badge } from "../../../../components/common/Badge.jsx";
import { capitalizeFirstLetter, formatCurrency, formatDate } from "../../../../utils/formatters.js";

export function BookingDetailInfo({ sport, bookingDate, timeSlot, createdAt, totalPrice }) {
    return (
        <div className="details-list">
            <div className="details-row">
                <span className="details-label">Type</span>
                <Badge variant="info">{capitalizeFirstLetter(sport)}</Badge>
            </div>

            <div className="details-row">
                <span className="details-label">Booking date</span>
                <span className="details-value">
                    {formatDate(bookingDate)}
                </span>
            </div>

            <div className="details-row align-center">
                <span className="details-label">Time slot</span>
                <Badge>{timeSlot}</Badge>
            </div>

            <div className="details-row">
                <span className="details-label">Created at</span>
                <span className="details-value-muted">
                    {createdAt}
                </span>
            </div>

            <div className="details-total-row">
                <span className="details-total-label">Total payment</span>
                <span className="details-total-value">
                    {formatCurrency(totalPrice)}
                </span>
            </div>
        </div>
    );
}