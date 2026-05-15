import React from "react";
import { Card } from "../../../../components/common/Card.jsx";
import { Button } from "../../../../components/common/Button.jsx";
import { Badge } from "../../../../components/common/Badge.jsx";
import { EmptyState } from "../../../../components/common/EmptyState.jsx";
import { Pagination } from "../../../../components/common/Pagination.jsx";
import { Edit2, Trash2 } from "lucide-react";
import { capitalizeFirstLetter, formatCurrency } from "../../../../utils/formatters.js";
import {sportIcons} from "../../../../utils/constants.jsx";

export function FieldTable({ loading, fields, pagination, onPageChange, onEditClick, onDeleteClick}) {
    return (
        <Card>
            {loading ? (
                <div className="loading">Loading...</div>
            ) : (
                <>
                    <div className="table-wrapper">
                        <table className="fields-table">
                            <thead>
                            <tr>
                                <th>Field Info</th>
                                <th>Sport</th>
                                <th>Price/Hour</th>
                                <th>Status</th>
                                <th className="actions-header">Actions</th>
                            </tr>
                            </thead>
                            <tbody>
                            {fields.map((field) => {
                                const sport = field.field_type.toLowerCase();
                                return (
                                    <tr key={field.id}>
                                        <td>
                                            <div className="field-info">
                                                {field.image ? (
                                                    <img
                                                        src={field.image}
                                                        alt="thumbnail"
                                                        className="field-image"
                                                    />
                                                ) : (
                                                    <div className={`field-image ${sport}`} style={{ fontSize: "30px", display: "flex", alignItems: "center", justifyContent: "center" }}>
                                                        {sportIcons[sport]}
                                                    </div>
                                                )}

                                                <div style={{ display: 'flex', flexDirection: 'column' }}>
                                                    <span className="field-name">{field.name}</span>
                                                    <span style={{ fontSize: '12px', color: '#64748b' }}>ID: {field.id}</span>
                                                </div>
                                            </div>
                                        </td>
                                        <td>
                                            <span>{capitalizeFirstLetter(sport)}</span>
                                        </td>
                                        <td>
                                            {formatCurrency(field.price_per_hour)}
                                        </td>
                                        <td>
                                            {field.is_active ? (
                                                <Badge variant="success">Active</Badge>
                                            ) : (
                                                <Badge variant="danger">Inactive</Badge>
                                            )}
                                        </td>
                                        <td>
                                            <div className="table-actions">
                                                <Button size="sm" className="btn-outline" onClick={() => onEditClick(field)}>
                                                    <Edit2 size={16} />
                                                </Button>
                                                {field.is_active && (
                                                    <Button size="sm" className="btn-outline" onClick={() => onDeleteClick(field.id)}>
                                                        <Trash2 size={16} className="delete-icon" />
                                                    </Button>
                                                )}
                                            </div>
                                        </td>
                                    </tr>
                                );
                            })}
                            </tbody>
                        </table>

                        {fields.length === 0 && (
                            <EmptyState text="fields" />
                        )}
                    </div>

                    <div className="table-pagination">
                        <Pagination
                            currentPage={pagination?.current_page}
                            totalPages={pagination?.total_pages}
                            onPageChange={onPageChange}
                        />
                    </div>
                </>
            )}
        </Card>
    );
}