export function getToken() {
    if (typeof (localStorage.userId) !== "undefined") {
        return localStorage.userId;
    }
    else if (typeof (sessionStorage.userId) !== "undefined") {
        return sessionStorage.userId;
    }
    return false;
}

export function deleteToken() {
    localStorage.clear();
    sessionStorage.clear();
}