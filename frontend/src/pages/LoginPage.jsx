import { useState } from "react";

import { loginUser } from "../api/authApi";


function LoginPage({
                       onLogin,
                       onGoSignup,
                   }) {
    const [email, setEmail] =
        useState("");

    const [password, setPassword] =
        useState("");

    const [loading, setLoading] =
        useState(false);

    const [error, setError] =
        useState("");


    const handleSubmit = async (event) => {
        event.preventDefault();

        setError("");
        setLoading(true);

        try {
            const result = await loginUser({
                email,
                password,
            });

            onLogin(result);
        } catch (err) {
            setError(
                err.message ||
                "로그인에 실패했습니다."
            );
        } finally {
            setLoading(false);
        }
    };


    return (
        <div style={styles.page}>
            <div style={styles.card}>
                <h1 style={styles.title}>
                    Image RAG
                </h1>

                <p style={styles.subtitle}>
                    로그인
                </p>

                <form
                    onSubmit={handleSubmit}
                    style={styles.form}
                >
                    <div style={styles.field}>
                        <label style={styles.label}>
                            이메일
                        </label>

                        <input
                            type="email"
                            value={email}
                            onChange={(event) =>
                                setEmail(
                                    event.target.value
                                )
                            }
                            placeholder="test@test.com"
                            required
                            style={styles.input}
                        />
                    </div>

                    <div style={styles.field}>
                        <label style={styles.label}>
                            비밀번호
                        </label>

                        <input
                            type="password"
                            value={password}
                            onChange={(event) =>
                                setPassword(
                                    event.target.value
                                )
                            }
                            placeholder="비밀번호"
                            required
                            minLength={6}
                            style={styles.input}
                        />
                    </div>

                    {error && (
                        <div style={styles.error}>
                            {error}
                        </div>
                    )}

                    <button
                        type="submit"
                        disabled={loading}
                        style={{
                            ...styles.button,
                            opacity:
                                loading
                                    ? 0.6
                                    : 1,
                        }}
                    >
                        {loading
                            ? "로그인 중..."
                            : "로그인"}
                    </button>
                </form>

                <div style={styles.bottom}>
          <span>
            계정이 없나요?
          </span>

                    <button
                        type="button"
                        onClick={onGoSignup}
                        style={styles.linkButton}
                    >
                        회원가입
                    </button>
                </div>
            </div>
        </div>
    );
}


const styles = {
    page: {
        minHeight: "100vh",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        background:
            "linear-gradient(135deg, #f4f7fb 0%, #e8eef7 100%)",
        padding: "24px",
        boxSizing: "border-box",
    },

    card: {
        width: "100%",
        maxWidth: "420px",
        background: "#ffffff",
        borderRadius: "18px",
        padding: "40px",
        boxSizing: "border-box",
        boxShadow:
            "0 20px 60px rgba(0, 0, 0, 0.08)",
    },

    title: {
        margin: 0,
        textAlign: "center",
        fontSize: "32px",
        fontWeight: 800,
    },

    subtitle: {
        marginTop: "10px",
        marginBottom: "30px",
        textAlign: "center",
        fontSize: "18px",
    },

    form: {
        display: "flex",
        flexDirection: "column",
        gap: "18px",
    },

    field: {
        display: "flex",
        flexDirection: "column",
        gap: "8px",
    },

    label: {
        fontWeight: 700,
        fontSize: "14px",
    },

    input: {
        height: "48px",
        border:
            "1px solid #d9dee7",
        borderRadius: "10px",
        padding: "0 14px",
        fontSize: "15px",
        boxSizing: "border-box",
        outline: "none",
    },

    button: {
        height: "50px",
        border: "none",
        borderRadius: "10px",
        background: "#111827",
        color: "#ffffff",
        fontSize: "16px",
        fontWeight: 700,
        cursor: "pointer",
    },

    error: {
        padding: "12px",
        borderRadius: "8px",
        background: "#fff1f2",
        color: "#be123c",
        fontSize: "14px",
    },

    bottom: {
        marginTop: "24px",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        gap: "8px",
        fontSize: "14px",
    },

    linkButton: {
        border: "none",
        background: "transparent",
        cursor: "pointer",
        fontWeight: 700,
        textDecoration: "underline",
    },
};


export default LoginPage;