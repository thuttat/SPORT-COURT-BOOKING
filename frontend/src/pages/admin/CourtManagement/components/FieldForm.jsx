import React from "react";
import { Card } from "../../../../components/common/Card.jsx";
import { Button } from "../../../../components/common/Button.jsx";
import { sportIcons } from "../../../../utils/constants.jsx";

export function FieldForm({ formData, setFormData, onSubmit, onCancel, editingId, isSubmitted }) {
    return (
        <Card className="field-form-card">
            <h3>{editingId ? "Edit Field" : "Add New Field"}</h3>
            <form onSubmit={onSubmit} className="field-form">
                <div>
                    <label className="form-label">Field Name</label>
                    <input
                        className="input"
                        style={{ width: '97%' }}
                        placeholder="e.g., Main Football Pitch"
                        value={formData.name}
                        onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                        required
                    />
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
                    <div>
                        <label className="form-label">Price per Hour (VNĐ)</label>
                        <input
                            type="number"
                            className="input"
                            style={{ width: '90%' }}
                            min="0"
                            value={formData.price_per_hour}
                            onChange={(e) => setFormData({ ...formData, price_per_hour: e.target.value })}
                            required
                        />
                    </div>
                    <div>
                        <label className="form-label">Court Image {editingId && "(Leave empty to keep current)"}</label>
                        <input
                            type="file"
                            className="input"
                            style={{ width: '94%' }}
                            accept="image/png, image/jpeg, image/jpg"
                            onChange={(e) => setFormData({ ...formData, image: e.target.files[0] })}
                            required={!editingId}
                        />
                    </div>
                </div>

                <div>
                    <label className="form-label">Description</label>
                    <textarea
                        className="input"
                        style={{ width: '97%', minHeight: '80px', resize: 'vertical' }}
                        value={formData.description}
                        onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                        required
                    />
                </div>

                <div>
                    <label className="form-label">Sport Type</label>
                    <div className="sport-grid">
                        {["football", "badminton", "tennis"].map((sport) => (
                            <button
                                key={sport}
                                type="button"
                                onClick={() => setFormData({ ...formData, field_type: sport })}
                                className={`sport-option ${formData.field_type === sport ? `selected ${sport}` : ""}`}
                            >
                                <div className="sport-emoji">
                                    {sportIcons[sport]}
                                </div>
                                <div className="sport-name">{sport}</div>
                            </button>
                        ))}
                    </div>
                </div>

                <div className="form-actions">
                    <Button type="button" variant="outline" onClick={onCancel} disabled={isSubmitted}>
                        Cancel
                    </Button>
                    <Button type="submit" className="flex-1 btn-primary" disabled={isSubmitted}>
                        {isSubmitted ? "Processing..." : (editingId ? "Update Field" : "Add Field")}
                    </Button>
                </div>
            </form>
        </Card>
    );
}