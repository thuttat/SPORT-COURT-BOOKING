import {useCallback, useState} from "react";
import {
    createFieldRequest, deleteFieldRequest,
    getAllFieldsRequest,
    getFieldDetailRequest,
    getFieldSlotsRequest,
    getAdminFieldsRequest, updateFieldRequest
} from "../apis.js";
import {FieldContext} from "./fieldContext.js";

export function FieldProvider({ children }) {
    const [fields, setFields] = useState([]);
    const [loadingFields, setLoadingFields] = useState(false);
    const [slots, setSlots] = useState([]);
    const [loadingSlots, setLoadingSlots] = useState(false);
    const [fieldDetail, setFieldDetail] = useState(null);
    const [loadingDetail, setLoadingDetail] = useState(false);
    const [myFields, setMyFields] = useState([]);
    const [loadingMyFields, setLoadingMyFields] = useState(false);

    const fetchFields = async (date) => {
        setLoadingFields(true);
        try {
            let allData = [];
            let page = 1;
            let hasNext = true;
            while (hasNext) {
                const response = await getAllFieldsRequest(page, date);
                allData = [...allData, ...response.data.data];
                hasNext = response.data.pagination.has_next;
                page++;
            }
            setFields(allData);
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

    const fetchMyFields = async () => {
        setLoadingMyFields(true);
        try {
            let allData = [];
            let page = 1;
            let hasNext = true;
            while (hasNext) {
                const response = await getAdminFieldsRequest(page);
                allData = [...allData, ...response.data.data];
                hasNext = response.data.pagination.has_next;
                page++;
            }
            setMyFields(allData);
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
            fields, loadingFields, fetchFields,
            fieldDetail, loadingDetail, fetchFieldDetail,
            slots, loadingSlots, fetchFieldSlots,
            myFields, loadingMyFields, fetchMyFields,
            addField, editField, removeField
        }}>
            {children}
        </FieldContext.Provider>
    )
}