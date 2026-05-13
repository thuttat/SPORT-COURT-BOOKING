import {useCallback, useState} from "react";
import {getAllFieldsRequest, getFieldSlotsRequest} from "../apis.js";
import {FieldContext} from "./fieldContext.js";

export function FieldProvider({ children }) {
    const [fields, setFields] = useState([]);
    const [loadingFields, setLoadingFields] = useState(false);
    const [slots, setSlots] = useState([]);
    const [loadingSlots, setLoadingSlots] = useState(false);
    const [fieldPagination, setFieldPagination] = useState({});

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

    return (
        <FieldContext.Provider value={{
            fields, loadingFields, fetchFields, fieldPagination,
            slots, loadingSlots, fetchFieldSlots
        }}>
            {children}
        </FieldContext.Provider>
    )
}