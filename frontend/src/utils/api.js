const API_HOST = "http://127.0.0.1:5000";

export function getProductData(id) {
    return fetch(`${API_HOST}/store/id=${id}`);
}

export function getProductsCount() {
    return fetch(`${API_HOST}/store/count`);
}

export function getImage(path) {
    return API_HOST + path;
}

export function regProfile(form) {
    return fetch(`${API_HOST}/registration`, {
        method: 'POST', 
        headers: { 'Content-Type' : 'application/json' },
        body: JSON.stringify(form)
    });
}

export function authProfile(form) {
    return fetch(`${API_HOST}/auth`, {
        method: 'POST', 
        headers: { 'Content-Type' : 'application/json' },
        body: JSON.stringify(form)
    });
}

export function uploadProduct(form) {
    return fetch(`${API_HOST}/upload`, {
        method: 'POST', 
        body: form
    });
}