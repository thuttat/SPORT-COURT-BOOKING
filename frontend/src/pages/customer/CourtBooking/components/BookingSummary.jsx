import {Card, CardContent} from "../../../../components/common/Card.jsx";
import { Badge } from "../../../../components/common/Badge.jsx";
import { Button } from "../../../../components/common/Button.jsx";
import {formatCurrency, formatDate} from "../../../../utils/formatters.js";
import {useState} from "react";

export function BookingSummary({ date, selectedSlot, subTotal, totalPrice, className = "", onConfirm, paymentMethod, setPaymentMethod, isSubmitted, isRestricted }) {
    const [isAgreed, setIsAgreed] = useState(false);

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
                                        disabled={isSubmitted || isRestricted}
                                    >
                                        💵 Cash
                                    </Button>
                                    <Button
                                        className={paymentMethod === "VNPAY" ? "btn-primary" : "btn-outline"}
                                        style={{ flex: 1, padding: '8px' }}
                                        onClick={() => setPaymentMethod("VNPAY")}
                                        disabled={isSubmitted || isRestricted}
                                    >
                                        💳 VNPay
                                    </Button>
                                </div>
                            </div>

                            <div style={{ marginBottom: '20px', display: 'flex', alignItems: 'flex-start', gap: '8px' }}>
                                <input
                                    type="checkbox"
                                    id="agreeTerms"
                                    checked={isAgreed}
                                    onChange={(e) => setIsAgreed(e.target.checked)}
                                    disabled={isRestricted}
                                    style={{ marginTop: '4px', cursor: isRestricted ? 'not-allowed' : 'pointer' }}
                                />
                                <label htmlFor="agreeTerms" style={{ fontSize: '13px', color: '#64748b', cursor: isRestricted ? 'not-allowed' : 'pointer', lineHeight: '1.5' }}>
                                    I have read and agree to the Terms of Service. I understand that canceling 3 bookings within a 7-day period will result in a 24-hour booking restriction.
                                </label>
                            </div>
                        </>
                    )}

                    <Button
                        className="btn-primary btn-full"
                        disabled={!selectedSlot || isSubmitted || isRestricted || !isAgreed}
                        onClick={onConfirm}
                    >
                        {isSubmitted ? "Processing..." : "Confirm Booking"}
                    </Button>
                </CardContent>
            </Card>
        </div>
    );
}