import axios from "axios";

const API_URL = "http://localhost:5000/api";

const api = axios.create({
    baseURL: API_URL,
    withCredentials: true
});

export const endpoints = {
    login: "/login",
    register: "/register",
    logout: "/logout",
    myBookings: "/my-bookings",
    bookingDetails: (id) => `/my-bookings/${id}`,
    cancelBooking: (id) => `/bookings/${id}/cancel`,
    fields: "/fields",
    fieldSlots: (id) => `/fields/${id}/slots`,
};

export const loginRequest = (username, password) => {
    const formData = new FormData();
    formData.append("username", username);
    formData.append("password", password);
    return api.post(endpoints.login, formData);
};

export const registerRequest = (fullname, username, email, password, confirm, avatarFile) => {
    const formData = new FormData();
    formData.append("fullname", fullname);
    formData.append("email", email);
    formData.append("username", username);
    formData.append("password", password);
    formData.append("confirm", confirm);
    formData.append("avatar", avatarFile);
    return api.post(endpoints.register, formData);
};

export const logoutRequest = () => {
    return api.post(endpoints.logout);
};

export const getMyBookingsRequest = (page = 1) => {
    return api.get(endpoints.myBookings, {
        params: { page },
        withCredentials: true
    });
};

export const getBookingDetailsRequest = (id) => {
    return api.get(endpoints.bookingDetails(id), {
        withCredentials: true
    });
};

export const cancelBookingRequest = (id) => {
    return api.patch(endpoints.cancelBooking(id), {
        withCredentials: true
    });
};

export const getAllFieldsRequest = (page = 1, date) => {
    return api.get(endpoints.fields, { params: { page, date } });
};

export const getFieldSlotsRequest = (fieldId, date) => {
    return api.get(endpoints.fieldSlots(fieldId), { params: { date } });
};

export default api;