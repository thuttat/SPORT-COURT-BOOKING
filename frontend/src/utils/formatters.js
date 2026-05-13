export const formatDate = (dateString) => {
    if (!dateString) return "";
    return new Date(dateString).toLocaleDateString("vi-VN", {
        weekday: "long",
        year: "numeric",
        month: "short",
        day: "numeric"
    });
};

export const formatTodayString = () => {
    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const day = String(today.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

export const formatCurrency = (amount) => {
    if (amount === undefined || amount === null) return "0 VNĐ";
    return amount.toLocaleString('vi-VN') + " VNĐ";
};

export const capitalizeFirstLetter = (string) => {
    if (!string) return "";
    return string.charAt(0).toUpperCase() + string.slice(1).toLowerCase();
};