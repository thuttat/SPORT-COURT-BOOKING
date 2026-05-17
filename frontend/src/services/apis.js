import axios from "axios";

const API_URL = "http://localhost:5000/api";

const api = axios.create({
    baseURL: API_URL,
    withCredentials: true
});

api.interceptors.response.use(
    (response) => {
        return response;
    },
    (error) => {
        if (error.response && error.response.status === 401) {
            localStorage.removeItem("accessToken");
            localStorage.removeItem("role");
            alert("Your login session has expired. Please log in again!");
            window.location.href = '/login';
        }
        return Promise.reject(error);
    }
);

export const endpoints = {
    login: "/login",
    register: "/register",
    logout: "/logout",
    myBookings: "/my-bookings",
    createBooking: "/bookings",
    bookingDetails: (id) => `/my-bookings/${id}`,
    cancelBooking: (id) => `/bookings/${id}`,
    fields: "/fields",
    fieldDetail: (id) => `/fields/${id}`,
    fieldSlots: (id) => `/fields/${id}/slots`,
    adminFields: "/admin/fields",
    adminFieldAction: (id) => `/admin/fields/${id}`,
    adminBookings:  "/admin/bookings",
    updateBookingStatus: (id) => `/admin/bookings/${id}/status`,
    dashboardSummary: "/admin/dashboard/summary",
    dashboardChartSport: "/admin/dashboard/chart-sport",
    dashboardRecentBookings: "/admin/dashboard/recent-bookings",
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

export const createBookingRequest = (fieldId, timeSlotsId, bookingDate) => {
    const formData = new FormData();
    formData.append("field_id", fieldId);
    formData.append("time_slots_id", timeSlotsId);
    formData.append("booking_date", bookingDate);
    return api.post(endpoints.createBooking, formData, {
        withCredentials: true
    });
};

export const getBookingDetailsRequest = (id) => {
    return api.get(endpoints.bookingDetails(id), {
        withCredentials: true
    });
};

export const cancelBookingRequest = (id) => {
    return api.delete(endpoints.cancelBooking(id), {
        withCredentials: true
    });
};

export const getAllFieldsRequest = (page = 1, date) => {
    return api.get(endpoints.fields, { params: { page, date } });
};

export const getFieldDetailRequest = (id) => {
    return api.get(endpoints.fieldDetail(id));
}

export const getFieldSlotsRequest = (fieldId, date) => {
    return api.get(endpoints.fieldSlots(fieldId), { params: { date } });
};

export const getAdminFieldsRequest = (page = 1) => {
    return api.get(endpoints.adminFields, {
        params: {page, page_size: 100},
        withCredentials: true
    });
};

export const createFieldRequest = (formData) => {
    return api.post(endpoints.adminFields, formData, {
        withCredentials: true
    });
};

export const updateFieldRequest = (id, formData) => {
    return api.patch(endpoints.adminFieldAction(id), formData, {
        withCredentials: true
    });
};

export const deleteFieldRequest = (id) => {
    return api.delete(endpoints.adminFieldAction(id), {
        withCredentials: true
    });
};

export const getAdminBookingsRequest = (page = 1, status = "") => {
    return api.get(endpoints.adminBookings, { params: { page, status } });
};

export const updateBookingStatusRequest = (id, status) => {
    return api.patch(endpoints.updateBookingStatus(id), { status });
};

export const getDashboardSummaryRequest = () => {
    return api.get(endpoints.dashboardSummary);
};

export const getChartSportRequest = () => {
    return api.get(endpoints.dashboardChartSport);
};

export const getRecentBookingsRequest = () => {
    return api.get(endpoints.dashboardRecentBookings);
};

export default api;