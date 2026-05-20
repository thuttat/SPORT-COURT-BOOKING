import React, { useEffect, useState } from "react";
import { useLocation, useNavigate, Link } from "react-router-dom";
import { PageHeader } from "../../../../components/common/PageHeader.jsx";
import { Card } from "../../../../components/common/Card.jsx";
import { Button } from "../../../../components/common/Button.jsx";
import { CheckCircle, XCircle } from "lucide-react";
import {verifyVnPayRequest} from "../../../../services/apis.js";

export function PaymentResult() {
    const location = useLocation();
    const navigate = useNavigate();
    const [status, setStatus] = useState("processing");
    const [message, setMessage] = useState("Processing payment results...");

    useEffect(() => {
        const verifyPayment = async () => {
            const searchParams = location.search;
            if (!searchParams) {
                setStatus("error");
                setMessage("Payment information not found.");
                return;
            }

            try {
                const res = await verifyVnPayRequest(searchParams);
                setStatus("success");
                setMessage("Payment successful! Your court has been reserved.");
            } catch (error) {
                setStatus("error");
                setMessage(error.response?.data?.message || "Payment failed or was canceled.");
            }
        };
        verifyPayment();
    }, [location]);

    return (
        <div className="container" style={{ textAlign: 'center', padding: '60px 20px' }}>
            <Card style={{ maxWidth: '500px', margin: '0 auto', padding: '40px 20px' }}>
                {status === "processing" && (
                    <div>
                        <h2>Checking the transaction...</h2>
                        <p className="text-muted">Please do not close your browser at this time.</p>
                    </div>
                )}

                {status === "success" && (
                    <div>
                        <CheckCircle size={64} color="var(--primary)" style={{ marginBottom: '20px' }} />
                        <h2 style={{ color: 'var(--primary)', marginBottom: '10px' }}>Payment Successful</h2>
                        <p style={{ marginBottom: '30px' }}>{message}</p>
                        <Button onClick={() => navigate("/bookings")} className="btn-primary">
                            View your booking history
                        </Button>
                    </div>
                )}

                {status === "error" && (
                    <div>
                        <XCircle size={64} color="var(--destructive)" style={{ marginBottom: '20px' }} />
                        <h2 style={{ color: 'var(--destructive)', marginBottom: '10px' }}>Payment Failed</h2>
                        <p style={{ marginBottom: '30px' }}>{message}</p>
                        <div style={{ display: 'flex', gap: '10px', justifyContent: 'center' }}>
                            <Button variant="outline" onClick={() => navigate("/")}>
                                Back to home page
                            </Button>
                            <Button onClick={() => navigate("/bookings")} className="btn-primary">
                                Reset the sport court
                            </Button>
                        </div>
                    </div>
                )}
            </Card>
        </div>
    );
}