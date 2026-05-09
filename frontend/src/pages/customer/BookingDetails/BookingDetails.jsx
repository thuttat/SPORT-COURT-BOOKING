import { useParams, useNavigate } from "react-router-dom";
import { useEffect } from "react";
import { ArrowLeft } from "lucide-react";
import { Card, CardContent } from "../../../components/common/Card.jsx";
import { Button } from "../../../components/common/Button.jsx";
import { useBooking } from "../../../services/booking/useBooking.js";
import { BookingDetailHeader } from "./components/BookingDetailHeader.jsx";
import { BookingDetailInfo } from "./components/BookingDetailInfo.jsx";
import "./bookingDetails.css";

export function BookingDetails() {
    const { id } = useParams();
    const navigate = useNavigate();
    const { bookingDetails, detailLoading, fetchBookingDetails } = useBooking();

    useEffect(() => {
        if (id) {
            fetchBookingDetails(id);
        }
    }, [id]);

    if (detailLoading || !bookingDetails) {
        return (
            <div className="container loading">
                Loading...
            </div>
        );
    }

    const sport = bookingDetails.field_type ? bookingDetails.field_type.toLowerCase() : 'default';

    return (
        <div className="container booking-details-container">
            <Button
                onClick={() => navigate(-1)}
                className="btn-outline back-btn back-button-custom"
            >
                <ArrowLeft size={16}/> Back
            </Button>

            <Card>
                <CardContent className="details-card-content">
                    <BookingDetailHeader
                        sport={sport}
                        fieldName={bookingDetails.field_name}
                        status={bookingDetails.status}
                    />

                    <BookingDetailInfo
                        sport={sport}
                        bookingDate={bookingDetails.booking_date}
                        timeSlot={bookingDetails.time_slot}
                        createdAt={bookingDetails.created_at}
                        totalPrice={bookingDetails.total_price}
                    />
                </CardContent>

                {bookingDetails.status === "PENDING" && (
                    <Button className="btn-danger">
                        Cancel
                    </Button>
                )}
            </Card>
        </div>
    );
}