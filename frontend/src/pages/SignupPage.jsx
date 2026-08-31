import { useState } from "react";

import { signupUser } from "../api/authApi";


function SignupPage({
                        onSignupSuccess,
                        onGoLogin,
                    }) {
    const [email, setEmail] =
        useState("");

    const [username, setUsername] =
        useState("");

    const [password, setPassword] =
        useState("");

    const [passwordConfirm, setPasswordConfirm] =
        useState("");

    const [loading, setLoading] =
        useState(false);

    const [error, setError] =
        useState("");

    const [success, setSuccess] =
        useState("");


    const handleSubmit = async (event) => {
        event.preventDefault();

        setError("");
        setSuccess("");

        if (
            password
            !== passwordConfirm
        ) {
            setError(
                "비밀번호가 서로 일치하지 않습니다."
            );

            return;
        }

        setLoading(true);

        try {
            await signupUser({
                email,
                username,
                password,
            });

            setSuccess(
                "회원가입이 완료되었습니다."
            );

            setTimeout(() => {
                onSignupSuccess();
            }, 700);
        } catch (err) {
            setError(
                err.message ||
                "회원가입에 실패했습니다."
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
                    회원가입
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
                            사용자명
                        </label>

                        <input
                            type="text"
                            value={username}
                            onChange={(event) =>
                                setUsername(
                                    event.target.value
                                )
                            }
                            placeholder="사용자명"
                            required
                            minLength={2}
                            maxLength={100}
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
                            placeholder="6자 이상"
                            required
                            minLength={6}
                            maxLength={100}
                            style={styles.input}
                        />
                    </div>

                    <div style={styles.field}>
                        <label style={styles.label}>
                            비밀번호 확인
                        </label>

                        <input
                            type="password"
                            value={passwordConfirm}
                            onChange={(event) =>
                                setPasswordConfirm(
                                    event.target.value
                                )
                            }
                            placeholder="비밀번호 다시 입력"
                            required
                            style={styles.input}
                        />
                    </div>

                    {error && (
                        <div style={styles.error}>
                            {error}
                        </div>
                    )}

                    {success && (
                        <div style={styles.success}>
                            {success}
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
                            ? "가입 중..."
                            : "회원가입"}
                    </button>
                </form>

                <div style={styles.bottom}>
          <span>
            이미 계정이 있나요?
          </span>

                    <button
                        type="button"
                        onClick={onGoLogin}
                        style={styles.linkButton}
                    >
                        로그인
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
        gap: "16px",
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

    success: {
        padding: "12px",
        borderRadius: "8px",
        background: "#ecfdf5",
        color: "#047857",
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


export default SignupPage;