import React from "react";
import { Card } from "../../../../components/common/Card.jsx";
import { Button } from "../../../../components/common/Button.jsx";
import { Badge } from "../../../../components/common/Badge.jsx";
import { EmptyState } from "../../../../components/common/EmptyState.jsx";
import { Pagination } from "../../../../components/common/Pagination.jsx";
import {CheckCircle, Edit2, Trash2} from "lucide-react";
import { capitalizeFirstLetter, formatCurrency } from "../../../../utils/formatters.js";
import {Table, TableBody, TableCell, TableHead, TableHeader, TableRow} from "../../../../components/common/Table.jsx";

export function FieldTable({ loading, fields, currentPage, totalPages, onPageChange, onEditClick, onDeleteClick, onToggleClick }) {
    return (
        <Card>
            {loading ? (
                <div className="loading">Loading...</div>
            ) : (
                <>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Field Info</TableHead>
                                <TableHead>Sport</TableHead>
                                <TableHead>Price/Hour</TableHead>
                                <TableHead>Status</TableHead>
                                <TableHead>Actions</TableHead>
                            </TableRow>
                        </TableHeader>

                        <TableBody>
                            {fields.length === 0 ? (
                                <TableRow>
                                    <TableCell colSpan={5} style={{ padding: 0 }}>
                                        <EmptyState text="fields" />
                                    </TableCell>
                                </TableRow>
                            ) : (
                                fields.map((field) => {
                                    const sport = field.field_type.toLowerCase();
                                    return (
                                        <TableRow key={field.id}>
                                            <TableCell>
                                                <div className="field-info">
                                                    <img
                                                        src={field.image}
                                                        alt="thumbnail"
                                                        style={{ width: '50px', height: '50px', objectFit: 'cover', borderRadius: '8px' }}
                                                    />
                                                    <div style={{ display: 'flex', flexDirection: 'column' }}>
                                                        <span className="field-name">{field.name}</span>
                                                        <span style={{ fontSize: '12px', color: '#64748b' }}>ID: {field.id}</span>
                                                    </div>
                                                </div>
                                            </TableCell>

                                            <TableCell>
                                                <span>{capitalizeFirstLetter(sport)}</span>
                                            </TableCell>

                                            <TableCell>
                                                {formatCurrency(field.price_per_hour)}
                                            </TableCell>

                                            <TableCell>
                                                {field.is_active ? (
                                                    <Badge variant="success">Active</Badge>
                                                ) : (
                                                    <Badge variant="danger">Inactive</Badge>
                                                )}
                                            </TableCell>

                                            <TableCell>
                                                <div className="table-actions">
                                                    <Button size="sm" className="btn-outline" onClick={() => onEditClick(field)}>
                                                        <Edit2 size={16} />
                                                    </Button>

                                                    {field.is_active ? (
                                                        <Button
                                                            size="sm"
                                                            className="btn-outline"
                                                            onClick={() => onDeleteClick(field.id)}
                                                        >
                                                            <Trash2 size={16} color="#ef4444" />
                                                        </Button>
                                                    ) : (
                                                        <Button
                                                            size="sm"
                                                            className="btn-outline btn-success"
                                                            onClick={() => onToggleClick(field)}
                                                        >
                                                            <CheckCircle size={16} />
                                                        </Button>
                                                    )}
                                                </div>
                                            </TableCell>
                                        </TableRow>
                                    );
                                })
                            )}
                        </TableBody>
                    </Table>

                    <div className="table-pagination">
                        <Pagination
                            currentPage={currentPage}
                            totalPages={totalPages}
                            onPageChange={onPageChange}
                        />
                    </div>
                </>
            )}
        </Card>
    );
}