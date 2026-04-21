import "../styles/emptyState.css";

export function EmptyState({ text }) {
    return (
        <div className="empty-state">
            <div className="empty-icon">🔍</div>
            <h4>No {text} found</h4>
            <p className="text-muted">Try adjusting your filters</p>
        </div>
    );
}