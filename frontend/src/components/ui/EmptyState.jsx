export function EmptyState() {
    return (
        <div className="empty-state">
            <div className="empty-icon">🔍</div>
            <h4>No fields found</h4>
            <p className="text-muted">Try adjusting your filters</p>
        </div>
    );
}