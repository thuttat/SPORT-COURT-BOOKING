export function PageHeader({header, text}) {
    return (
        <div className="page-header">
            <h2>{header}</h2>
            <p className="text-muted">
                {text}
            </p>
        </div>
    )
}