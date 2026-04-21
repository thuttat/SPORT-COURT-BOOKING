import React from "react";
import "../styles/card.css";

export function ClickableCard({ children, className = "", onClick }) {
    return (
        <div
            className={`card ${onClick ? "card-clickable" : ""} ${className}`}
            onClick={onClick}
        >
            {children}
        </div>
    );
}

export function Card({ className = "", ...props }) {
    return <div className={`card-base ${className}`} {...props} />;
}

export function CardHeader({ className = "", ...props }) {
    return <div className={`card-header ${className}`} {...props} />;
}

export function CardTitle({ className = "", ...props }) {
    return <h4 className={`card-title ${className}`} {...props} />;
}

export function CardDescription({ className = "", ...props }) {
    return <p className={`card-description ${className}`} {...props} />;
}

export function CardAction({ className = "", ...props }) {
    return <div className={`card-action ${className}`} {...props} />;
}

export function CardContent({ className = "", ...props }) {
    return <div className={`card-content ${className}`} {...props} />;
}

export function CardFooter({ className = "", ...props }) {
    return <div className={`card-footer ${className}`} {...props} />;
}