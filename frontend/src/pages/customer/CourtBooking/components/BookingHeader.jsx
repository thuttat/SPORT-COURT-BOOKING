import { Button } from "../../../../components/common/Button.jsx";
import { Badge } from "../../../../components/common/Badge.jsx";
import { ArrowLeft } from "lucide-react";
import {capitalizeFirstLetter, formatCurrency} from "../../../../utils/formatters.js";

export function BookingHeader({ onBack, fieldDetail, isFull }) {
    return (
        <div className="booking-header header-container">
            <div className="header-top-bar">
                <Button onClick={onBack} className="back-btn btn-outline">
                    <ArrowLeft size={16}/> Back
                </Button>
            </div>

            {fieldDetail ? (
                <>
                    <div className="field-cover-wrapper">
                        <img src={fieldDetail.image} alt={fieldDetail.name} className="field-cover-img" />
                    </div>

                    <div className="field-detail-info">
                        <h1 className="title">{fieldDetail.name}</h1>

                        <div className="badges">
                            <Badge variant="info">{capitalizeFirstLetter(fieldDetail.field_type)}</Badge>
                            {isFull ? (
                                <Badge variant="danger">Full</Badge>
                            ) : (
                                <Badge variant="success">Available</Badge>
                            )}
                        </div>

                        <p className="field-desc">✏️ {fieldDetail.description}</p>
                        <div className="field-price-meta">
                            💰 {formatCurrency(fieldDetail.price_per_hour)} <span style={{fontSize: '14px', color: '#94a3b8'}}>/h</span>
                        </div>
                    </div>
                </>
            ) : (
                <div style={{ padding: '20px' }}>Loading...</div>
            )}
        </div>
    );
}