import React, { useEffect, useState } from "react";
import { PageHeader } from "../../../components/common/PageHeader.jsx";
import { Button } from "../../../components/common/Button.jsx";
import { Plus, X } from "lucide-react";
import { useField } from "../../../services/field/useField.js";
import { FieldForm } from "./components/FieldForm.jsx";
import { FieldTable } from "./components/FieldTable.jsx";
import "./courtManagement.css";

export function CourtManagement() {
    const { myFields, myFieldPagination, loadingMyFields, fetchMyFields, addField, editField, removeField } = useField();
    const [showForm, setShowForm] = useState(false);
    const [editingId, setEditingId] = useState(null);
    const [isSubmitted, setIsSubmitted] = useState(false);

    const [formData, setFormData] = useState({
        name: "",
        field_type: "football",
        price_per_hour: "",
        description: "",
        image: null
    });

    useEffect(() => {
        fetchMyFields(1);
    }, []);

    const resetForm = () => {
        setFormData({
            name: "",
            field_type: "football",
            price_per_hour: "",
            description: "",
            image: null,
        });
        setEditingId(null);
        setShowForm(false);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsSubmitted(true);

        const payload = new FormData();
        payload.append("name", formData.name);
        payload.append("field_type", formData.field_type.toUpperCase());
        payload.append("price_per_hour", formData.price_per_hour);
        payload.append("description", formData.description);

        if (formData.image) {
            payload.append("image", formData.image);
        }

        try {
            if (editingId) {
                await editField(editingId, payload);
                alert("Update successfully!");
            } else {
                await addField(payload);
                alert("Create successfully!");
            }
            fetchMyFields(myFieldPagination?.current_page || 1);
            resetForm();
        } catch (error) {
            alert(`Error: ${error.response?.data?.message}`);
        } finally {
            setIsSubmitted(false);
        }
    };

    const handleEditClick = (field) => {
        setEditingId(field.id);
        setFormData({
            name: field.name,
            field_type: field.field_type.toLowerCase(),
            price_per_hour: field.price_per_hour,
            description: field.description,
            image: null,
        });
        setShowForm(true);
    };

    const handleDeleteClick = async (id) => {
        const isConfirmed = window.confirm("Are you sure you want to delete (deactivate) this court? This action cannot be reversed if someone is currently booking the court.");
        if (isConfirmed) {
            try {
                await removeField(id);
                alert("Delete (deactivate) successfully!");
                fetchMyFields(myFieldPagination?.current_page || 1);
            } catch (error) {
                alert(`Error: ${error.response?.data?.message}`);
            }
        }
    };

    return (
        <div className="field-management-container">
            <div className="field-management-wrapper">
                <div className="field-management-header">
                    <PageHeader header="Court Management" text="Add, edit, or remove sports courts" />
                    <Button onClick={() => { if (showForm) resetForm(); else setShowForm(true); }}>
                        {showForm ? <><X size={16} /> Cancel</> : <><Plus size={16} /> Add Field</>}
                    </Button>
                </div>

                {showForm && (
                    <FieldForm
                        formData={formData}
                        setFormData={setFormData}
                        onSubmit={handleSubmit}
                        onCancel={resetForm}
                        editingId={editingId}
                        isSubmitted={isSubmitted}
                    />
                )}

                <FieldTable
                    loading={loadingMyFields}
                    fields={myFields}
                    pagination={myFieldPagination}
                    onPageChange={fetchMyFields}
                    onEditClick={handleEditClick}
                    onDeleteClick={handleDeleteClick}
                />
            </div>
        </div>
    );
}