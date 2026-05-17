import {Badge} from "../components/common/Badge.jsx";

export const sportIcons = {
    football: "⚽",
    badminton: "🏸",
    tennis: "🎾",
    default: "🏟️"
};

export const renderStatusBadge = (status) => {
    switch(status) {
        case 'PENDING': return <Badge variant="warning">Pending</Badge>;
        case 'CONFIRMED': return <Badge variant="info">Confirmed</Badge>;
        case 'COMPLETED': return <Badge variant="success">Completed</Badge>;
        case 'CANCELLED': return <Badge variant="danger">Cancelled</Badge>;
        default: return <Badge>{status}</Badge>;
    }
};