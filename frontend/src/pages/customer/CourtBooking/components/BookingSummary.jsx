import {Card, CardContent} from "../../../../components/common/Card.jsx";
import { Badge } from "../../../../components/common/Badge.jsx";
import { Button } from "../../../../components/common/Button.jsx";
import {formatCurrency, formatDate} from "../../../../utils/formatters.js";

export function BookingSummary({ date, selectedSlot, subTotal, totalPrice, className = "", onConfirm, paymentMethod, setPaymentMethod, isSubmitted }) {
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
                        <>
                            <div className="summary-row">
                                <span>Time</span>
                                <Badge variant="info">{selectedSlot.display}</Badge>
                            </div>

                            <div className="summary-row">
                                <span>Duration</span>
                                <span>{selectedSlot.duration}h</span>
                            </div>

                            <div className="summary-row">
                                <span>Base Price</span>
                                <span>{formatCurrency(subTotal)}</span>
                            </div>

                            {selectedSlot.price_multiplier !== 1 && (
                                <p style={{ fontSize: '12px', color: '#94a3b8', textAlign: 'right', margin: 0 }}>
                                    (Rate: x{selectedSlot.price_multiplier})
                                </p>
                            )}

                            <div className="summary-row" style={{ marginTop: '8px', paddingTop: '8px', borderTop: '1px dashed var(--muted-foreground)' }}>
                                <span style={{ fontWeight: '600' }}>Total Payment</span>
                                <span style={{ fontWeight: '700', color: '#ef4444', fontSize: '1.1rem' }}>
                                    {formatCurrency(totalPrice)}
                                </span>
                            </div>

                            <div style={{ marginTop: '20px', marginBottom: '20px' }}>
                                <span style={{ fontWeight: '600', display: 'block', marginBottom: '10px', fontSize: '14px' }}>Payment Method</span>
                                <div style={{ display: 'flex', gap: '10px' }}>
                                    <Button
                                        className={paymentMethod === "CASH" ? "btn-primary" : "btn-outline"}
                                        style={{ flex: 1, padding: '8px' }}
                                        onClick={() => setPaymentMethod("CASH")}
                                        disabled={isSubmitted}
                                    >
                                        💵 Cash
                                    </Button>
                                    <Button
                                        className={paymentMethod === "VNPAY" ? "btn-primary" : "btn-outline"}
                                        style={{ flex: 1, padding: '8px' }}
                                        onClick={() => setPaymentMethod("VNPAY")}
                                        disabled={isSubmitted}
                                    >
                                        💳 VNPay
                                    </Button>
                                </div>
                            </div>
                        </>
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