import {
  useEffect,
  useState,
} from "react";

import {
  getMe,
  logoutUser,
} from "./api/authApi";

import ImageRagPage
  from "./pages/ImageRagPage";

import LoginPage
  from "./pages/LoginPage";

import SignupPage
  from "./pages/SignupPage";


const TOKEN_KEY =
    "image_rag_access_token";


function App() {
  const [user, setUser] =
      useState(null);

  const [page, setPage] =
      useState("login");

  const [loading, setLoading] =
      useState(true);


  useEffect(() => {
    const restoreLogin =
        async () => {
          const token =
              localStorage.getItem(
                  TOKEN_KEY
              );

          if (!token) {
            setLoading(false);
            return;
          }

          try {
            const currentUser =
                await getMe(token);

            setUser(
                currentUser
            );

            setPage(
                "app"
            );
          } catch {
            localStorage.removeItem(
                TOKEN_KEY
            );

            setUser(null);
            setPage("login");
          } finally {
            setLoading(false);
          }
        };

    restoreLogin();
  }, []);


  const handleLogin = (
      loginResult
  ) => {
    localStorage.setItem(
        TOKEN_KEY,
        loginResult.access_token
    );

    setUser(
        loginResult.user
    );

    setPage(
        "app"
    );
  };


  const handleLogout = async () => {
    const token =
        localStorage.getItem(
            TOKEN_KEY
        );

    try {
      if (token) {
        await logoutUser(
            token
        );
      }
    } catch (error) {
      console.error(
          "Logout error:",
          error
      );
    } finally {
      localStorage.removeItem(
          TOKEN_KEY
      );

      setUser(null);
      setPage("login");
    }
  };


  if (loading) {
    return (
        <div style={styles.loading}>
          로그인 상태 확인 중...
        </div>
    );
  }


  if (
      !user
      && page === "signup"
  ) {
    return (
        <SignupPage
            onSignupSuccess={() =>
                setPage("login")
            }
            onGoLogin={() =>
                setPage("login")
            }
        />
    );
  }


  if (!user) {
    return (
        <LoginPage
            onLogin={handleLogin}
            onGoSignup={() =>
                setPage("signup")
            }
        />
    );
  }


  return (
      <div>
        <header style={styles.header}>
          <div>
            <strong>
              {user.username}
            </strong>

            <span style={styles.email}>
            {user.email}
          </span>
          </div>

          <button
              type="button"
              onClick={handleLogout}
              style={styles.logoutButton}
          >
            로그아웃
          </button>
        </header>

        <ImageRagPage />
      </div>
  );
}


const styles = {
  loading: {
    minHeight: "100vh",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontSize: "18px",
  },

  header: {
    minHeight: "64px",
    padding: "0 24px",
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    borderBottom:
        "1px solid #e5e7eb",
    background: "#ffffff",
    boxSizing: "border-box",
  },

  email: {
    marginLeft: "12px",
    color: "#6b7280",
    fontSize: "14px",
  },

  logoutButton: {
    border: "none",
    borderRadius: "8px",
    background: "#111827",
    color: "#ffffff",
    padding: "10px 16px",
    cursor: "pointer",
    fontWeight: 700,
  },
};


export default App;