import {useCallback, useState} from "react";
import {
    createFieldRequest, deleteFieldRequest,
    getAllFieldsRequest,
    getFieldDetailRequest,
    getFieldSlotsRequest,
    getMyFieldsRequest, updateFieldRequest
} from "../apis.js";
import {FieldContext} from "./fieldContext.js";

export function FieldProvider({ children }) {
    const [fields, setFields] = useState([]);
    const [loadingFields, setLoadingFields] = useState(false);
    const [slots, setSlots] = useState([]);
    const [loadingSlots, setLoadingSlots] = useState(false);
    const [fieldPagination, setFieldPagination] = useState({});
    const [fieldDetail, setFieldDetail] = useState(null);
    const [loadingDetail, setLoadingDetail] = useState(false);
    const [myFields, setMyFields] = useState([]);
    const [myFieldPagination, setMyFieldPagination] = useState({});
    const [loadingMyFields, setLoadingMyFields] = useState(false);

    const fetchFields = async (page = 1, date) => {
        setLoadingFields(true);
        try {
            const response = await getAllFieldsRequest(page, date);
            setFields(response.data.data);
            setFieldPagination(response.data.pagination);
        } catch (error) {
            console.error("Error fetching fields", error);
        } finally {
            setLoadingFields(false);
        }
    };

    const fetchFieldDetail = async (id) => {
        setLoadingDetail(true);
        try {
            const response = await getFieldDetailRequest(id);
            setFieldDetail(response.data.data);
        } catch (error) {
            console.error("Error fetching field detail", error);
        } finally {
            setLoadingDetail(false);
        }
    };

    const fetchFieldSlots = useCallback(async (fieldId, date) => {
        setLoadingSlots(true);
        try {
            const response = await getFieldSlotsRequest(fieldId, date);
            setSlots(response.data.data);
        } catch (error) {
            console.error("Error fetching field slots", error);
        } finally {
            setLoadingSlots(false);
        }
    }, []);

    const fetchMyFields = async (page = 1) => {
        setLoadingMyFields(true);
        try {
            const response = await getMyFieldsRequest(page);
            setMyFields(response.data.data);
            setMyFieldPagination(response.data.pagination);
        } catch (error) {
            console.error("Error fetching fields:", error);
        } finally {
            setLoadingMyFields(false);
        }
    };

    const addField = async (formData) => {
        const res = await createFieldRequest(formData);
        return res.data;
    };

    const editField = async (id, formData) => {
        const res = await updateFieldRequest(id, formData);
        return res.data;
    };

    const removeField = async (id) => {
        const res = await deleteFieldRequest(id);
        return res.data;
    };

    return (
        <FieldContext.Provider value={{
            fields, loadingFields, fetchFields, fieldPagination,
            fieldDetail, loadingDetail, fetchFieldDetail,
            slots, loadingSlots, fetchFieldSlots,
            myFields, myFieldPagination, loadingMyFields, fetchMyFields,
            addField, editField, removeField
        }}>
            {children}
        </FieldContext.Provider>
    )
}