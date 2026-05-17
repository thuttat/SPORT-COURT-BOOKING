import React, { useEffect, useState } from "react";
import { PageHeader } from "../../../components/common/PageHeader.jsx";
import { Button } from "../../../components/common/Button.jsx";
import { Plus, X } from "lucide-react";
import { useField } from "../../../services/field/useField.js";
import { FieldForm } from "./components/FieldForm.jsx";
import { FieldTable } from "./components/FieldTable.jsx";
import "./courtManagement.css";
import {capitalizeFirstLetter} from "../../../utils/formatters.js";

const SPORTS_TABS = ["all", "football", "badminton", "tennis"];

export function CourtManagement() {
    const { myFields, loadingMyFields, fetchMyFields, addField, editField, removeField } = useField();
    const [activeSport, setActiveSport] = useState("all");
    const [currentPage, setCurrentPage] = useState(1);
    const ITEMS_PER_PAGE = 5;
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
        fetchMyFields();
    }, []);

    useEffect(() => {
        setCurrentPage(1);
    }, [activeSport]);

    const filteredFields = myFields.filter(field => {
        const sport = field.field_type.toLowerCase();
        return activeSport === "all" || sport === activeSport;
    });

    const totalPages = Math.ceil(filteredFields.length / ITEMS_PER_PAGE);
    const displayedFields = filteredFields.slice(
        (currentPage - 1) * ITEMS_PER_PAGE,
        currentPage * ITEMS_PER_PAGE
    );

    const resetForm = () => {
        setFormData({ name: "", field_type: "football", price_per_hour: "", description: "", image: null });
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
            fetchMyFields();
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
        if (window.confirm("Are you sure you want to delete (deactivate) this court?")) {
            try {
                await removeField(id);
                alert("Delete (deactivate) successfully!");
                fetchMyFields();
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

                <div className="management-tabs">
                    {SPORTS_TABS.map(sport => (
                        <Button
                            key={sport}
                            className={`tab-btn ${activeSport === sport ? "active" : ""}`}
                            onClick={() => setActiveSport(sport)}
                        >
                            {sport === "all" ? "All Sports" : capitalizeFirstLetter(sport)}
                        </Button>
                    ))}
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
                    fields={displayedFields}
                    currentPage={currentPage}
                    totalPages={totalPages}
                    onPageChange={(page) => setCurrentPage(page)}
                    onEditClick={handleEditClick}
                    onDeleteClick={handleDeleteClick}
                />
            </div>
        </div>
    );
}