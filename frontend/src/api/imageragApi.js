const API_BASE_URL =
    import.meta.env.VITE_API_BASE_URL || "";


export const searchImageRag = async (imageFile) => {
    const formData = new FormData();

    formData.append("image", imageFile);

    const response = await fetch(
        `${API_BASE_URL}/api/imagerag/search`,
        {
            method: "POST",
            body: formData,
        }
    );

    const data = await response.json();

    if (!response.ok) {
        throw new Error(
            data.detail ||
            "이미지 분석에 실패했습니다."
        );
    }

    return data;
};


export const getImageUrl = (path) => {
    if (!path) {
        return "";
    }

    if (
        path.startsWith("http://") ||
        path.startsWith("https://")
    ) {
        return path;
    }

    return `${API_BASE_URL}${path}`;
};