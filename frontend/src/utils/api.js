export const API_HOST = "http://127.0.0.1:5000";

export function getProductData(id) {
    return fetch(`${API_HOST}/store/id=${id}`);
}

export function getProductsCount() {
    return fetch(`${API_HOST}/store/count`);
}

export function getImage(path) {
    return API_HOST + path;
}