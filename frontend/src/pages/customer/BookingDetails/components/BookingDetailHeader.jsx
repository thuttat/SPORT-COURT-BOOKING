import { renderStatusBadge, sportIcons } from "../../../../utils/constants.jsx";

export function BookingDetailHeader({ sport, fieldName, status }) {
    return (
        <div className="details-header">
            <div className="details-title-wrapper">
                <div className="details-sport-icon">
                    {sportIcons[sport]}
                </div>
                <h2 className="details-field-name">
                    {fieldName}
                </h2>
            </div>
            {renderStatusBadge(status)}
        </div>
    );
}