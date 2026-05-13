import { Card, CardContent, CardFooter } from "../../../../components/common/Card.jsx";
import {Button} from "../../../../components/common/Button.jsx";
import {Badge} from "../../../../components/common/Badge.jsx";
import {useNavigate} from "react-router-dom";
import {sportIcons} from "../../../../utils/constants.jsx";
import {capitalizeFirstLetter, formatCurrency} from "../../../../utils/formatters.js";

export function CourtCard({ court }) {
    const navigate = useNavigate();

    return (
        <Card className="court-card">
            {court.image ? (
                <img src={court.image} alt="court-image" className="court-image"/>
            ) : (
                <div className={`court-image ${court.field_type.toLowerCase()}`}>
                    {sportIcons[court.field_type.toLowerCase()]}
                </div>
            )}

            <CardContent className="court-body">
                <div className="court-header">
                    <h3 className="court-name">{court.name}</h3>
                    {court.available ? (
                        <Badge variant="success">Available</Badge>
                    ) : (
                        <Badge variant="danger">Full</Badge>
                    )}
                </div>

                <div className="court-info">
                    <div className="info-row">
                        <span>🏟️</span>
                        <span>{capitalizeFirstLetter(court.field_type)}</span>
                    </div>

                    <div className="info-row">
                        <span>✏️</span>
                        <span>{court.description}</span>
                    </div>
                </div>

                <div className="court-meta">
                    <div>
                        <div className="text-muted small">Price</div>
                        <div className="price">
                            {formatCurrency(court.price_per_hour)}
                            <span className="text-muted small"> /h</span>
                        </div>
                    </div>

                    {/*<div className="rating">*/}
                    {/*    <div className="text-muted small">Rating</div>*/}
                    {/*    <div>⭐ {court.rating}</div>*/}
                    {/*</div>*/}
                </div>
            </CardContent>

            <CardFooter>
                {court.available ? (
                    <Button
                        className="btn-primary btn-full"
                        onClick={() => navigate(`court/${court.id}`)}
                    >
                        Book Now
                    </Button>
                ) : (
                    <Button className="btn-disabled btn-full">
                        Unavailable
                    </Button>
                )}
            </CardFooter>
        </Card>
    );
}