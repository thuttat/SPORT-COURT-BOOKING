import React from "react";
import "../styles/pagination.css";

export function Pagination({ currentPage, totalPages, onPageChange }) {
    if (!totalPages || totalPages <= 1) return null;

    return (
        <div className="pagination-container">
            <button
                className="btn-outline pagination-btn"
                disabled={currentPage === 1}
                onClick={() => onPageChange(currentPage - 1)}
            >
                Prev
            </button>

            <span className="pagination-info">
                Page {currentPage} / {totalPages}
            </span>

            <button
                className="btn-outline pagination-btn"
                disabled={currentPage === totalPages}
                onClick={() => onPageChange(currentPage + 1)}
            >
                Next
            </button>
        </div>
    );
}