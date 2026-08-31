const API_BASE_URL =
    import.meta.env.VITE_API_BASE_URL || "";


async function parseResponse(response) {
    let data = null;

    try {
        data = await response.json();
    } catch {
        data = null;
    }

    if (!response.ok) {
        throw new Error(
            data?.detail ||
            data?.message ||
            "요청 처리 중 오류가 발생했습니다."
        );
    }

    return data;
}


export async function signupUser({
                                     email,
                                     username,
                                     password,
                                 }) {
    const response = await fetch(
        `${API_BASE_URL}/api/auth/signup`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                email,
                username,
                password,
            }),
        }
    );

    return parseResponse(response);
}


export async function loginUser({
                                    email,
                                    password,
                                }) {
    const response = await fetch(
        `${API_BASE_URL}/api/auth/login`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                email,
                password,
            }),
        }
    );

    return parseResponse(response);
}


export async function getMe(token) {
    const response = await fetch(
        `${API_BASE_URL}/api/auth/me`,
        {
            method: "GET",
            headers: {
                Authorization: `Bearer ${token}`,
            },
        }
    );

    return parseResponse(response);
}


export async function logoutUser(token) {
    const response = await fetch(
        `${API_BASE_URL}/api/auth/logout`,
        {
            method: "POST",
            headers: {
                Authorization: `Bearer ${token}`,
            },
        }
    );

    return parseResponse(response);
}