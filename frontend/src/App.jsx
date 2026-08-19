import { useEffect, useState } from "react";

import {
  Navigate,
  NavLink,
  Route,
  Routes,
  useNavigate,
  useParams,
} from "react-router-dom";

import {
  deleteFile,
  deleteUser,
  getCurrentUser,
  getDownloadUrl,
  getFiles,
  getPublicFileUrl,
  getUsers,
  initializeCsrf,
  loginUser,
  logoutUser,
  registerUser,
  toggleUserAdmin,
  updateFile,
  uploadFile,
} from "./services/api";


function getErrorMessage(error) {
  const data = error?.response?.data;

  if (!data) {
    return "Не удалось подключиться к серверу.";
  }

  if (typeof data.detail === "string") {
    return data.detail;
  }

  if (typeof data === "string") {
    return data;
  }

  return Object.entries(data)
    .map(([field, messages]) => {
      const text = Array.isArray(messages)
        ? messages.join(", ")
        : String(messages);

      return `${field}: ${text}`;
    })
    .join("\n");
}


function formatFileSize(size) {
  if (size < 1024) {
    return `${size} Б`;
  }

  if (size < 1024 * 1024) {
    return `${(
      size / 1024
    ).toFixed(1)} КБ`;
  }

  if (size < 1024 * 1024 * 1024) {
    return `${(
      size / 1024 / 1024
    ).toFixed(1)} МБ`;
  }

  return `${(
    size / 1024 / 1024 / 1024
  ).toFixed(1)} ГБ`;
}


function formatDate(value) {
  if (!value) {
    return "—";
  }

  return new Date(value).toLocaleString(
    "ru-RU",
  );
}


function AuthForm({
  mode,
  onSuccess,
  onSwitch,
}) {
  const isLogin = mode === "login";

  const [form, setForm] = useState({
    username: "",
    email: "",
    fullName: "",
    password: "",
    passwordConfirm: "",
  });

  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  function handleChange(event) {
    const { name, value } = event.target;

    setForm((currentForm) => ({
      ...currentForm,
      [name]: value,
    }));
  }

  async function handleSubmit(event) {
    event.preventDefault();

    setError("");
    setLoading(true);

    try {
      if (!isLogin) {
        if (form.password !== form.passwordConfirm) {
          throw new Error(
            "Пароли не совпадают.",
          );
        }

        if (
          !/^[A-Za-z][A-Za-z0-9]{3,19}$/.test(
            form.username,
          )
        ) {
          throw new Error(
            "Логин должен содержать от 4 до 20 символов, начинаться с латинской буквы и содержать только латинские буквы и цифры.",
          );
        }

        if (form.password.length < 6) {
          throw new Error(
            "Пароль должен содержать минимум 6 символов.",
          );
        }

        if (!/[A-ZА-ЯЁ]/.test(form.password)) {
          throw new Error(
            "Пароль должен содержать хотя бы одну заглавную букву.",
          );
        }

        if (!/\d/.test(form.password)) {
          throw new Error(
            "Пароль должен содержать хотя бы одну цифру.",
          );
        }

        if (
          !/[^A-Za-zА-Яа-яЁё0-9]/.test(
            form.password,
          )
        ) {
          throw new Error(
            "Пароль должен содержать хотя бы один специальный символ.",
          );
        }
      }

      const data = isLogin
        ? {
            username: form.username,
            password: form.password,
          }
        : {
            username: form.username,
            full_name: form.fullName,
            email: form.email,
            password: form.password,
          };

      const result = isLogin
        ? await loginUser(data)
        : await registerUser(data);

      onSuccess(result.user);
    } catch (requestError) {
      if (
        requestError instanceof Error
        && !requestError.response
      ) {
        setError(requestError.message);
      } else {
        setError(
          getErrorMessage(requestError),
        );
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="auth-card">
      <h2>
        {isLogin ? "Вход" : "Регистрация"}
      </h2>

      <form onSubmit={handleSubmit}>
        <label htmlFor="username">
          Логин
        </label>

        <input
          id="username"
          name="username"
          value={form.username}
          onChange={handleChange}
          autoComplete="username"
          minLength={4}
          maxLength={20}
          pattern="[A-Za-z][A-Za-z0-9]{3,19}"
          title="От 4 до 20 символов: латинские буквы и цифры, первый символ — буква."
          required
        />

        {!isLogin && (
          <>
            <label htmlFor="email">
              Email
            </label>

            <input
              id="email"
              name="email"
              type="email"
              value={form.email}
              onChange={handleChange}
              autoComplete="email"
              required
            />

            <label htmlFor="fullName">
              Полное имя
            </label>

            <input
              id="fullName"
              name="fullName"
              value={form.fullName}
              onChange={handleChange}
              autoComplete="name"
              required
            />
          </>
        )}

        <label htmlFor="password">
          Пароль
        </label>

        <input
          id="password"
          name="password"
          type="password"
          value={form.password}
          onChange={handleChange}
          autoComplete={
            isLogin
              ? "current-password"
              : "new-password"
          }
          minLength={6}
          title="Минимум 6 символов, заглавная буква, цифра и специальный символ."
          required
        />

        {!isLogin && (
          <>
            <label htmlFor="passwordConfirm">
              Повторите пароль
            </label>

            <input
              id="passwordConfirm"
              name="passwordConfirm"
              type="password"
              value={form.passwordConfirm}
              onChange={handleChange}
              autoComplete="new-password"
              minLength={6}
              required
            />
          </>
        )}

        {error && (
          <p className="form-error">
            {error}
          </p>
        )}

        <button
          type="submit"
          disabled={loading}
        >
          {loading
            ? "Подождите..."
            : isLogin
              ? "Войти"
              : "Зарегистрироваться"}
        </button>
      </form>

      <button
        className="link-button"
        type="button"
        onClick={onSwitch}
      >
        {isLogin
          ? "Создать аккаунт"
          : "У меня уже есть аккаунт"}
      </button>
    </section>
  );
}


function FileUploader({
  ownerId = null,
  onUploaded,
}) {
  const [file, setFile] = useState(null);
  const [comment, setComment] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  function handleFileChange(event) {
    setFile(
      event.target.files[0] || null,
    );
    setError("");
  }

  async function handleSubmit(event) {
    event.preventDefault();

    if (!file) {
      setError("Выбери файл.");
      return;
    }

    setError("");
    setLoading(true);

    try {
      const createdFile = await uploadFile(
        file,
        comment,
        ownerId,
      );

      setFile(null);
      setComment("");
      event.target.reset();

      onUploaded(createdFile);
    } catch (requestError) {
      setError(
        getErrorMessage(requestError),
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="cloud-card">
      <h2>Загрузить файл</h2>

      <form onSubmit={handleSubmit}>
        <input
          type="file"
          onChange={handleFileChange}
          required
        />

        <textarea
          placeholder="Комментарий к файлу"
          value={comment}
          onChange={(event) => {
            setComment(event.target.value);
          }}
          rows="3"
        />

        {error && (
          <p className="form-error">
            {error}
          </p>
        )}

        <button
          type="submit"
          disabled={loading}
        >
          {loading
            ? "Загрузка..."
            : "Загрузить"}
        </button>
      </form>
    </section>
  );
}


function FileRow({
  file,
  onUpdated,
  onDeleted,
}) {
  const [editing, setEditing] = useState(false);
  const [fileName, setFileName] = useState(
    file.original_name || "",
  );
  const [comment, setComment] = useState(
    file.comment || "",
  );
  const [error, setError] = useState("");
  const [saving, setSaving] = useState(false);
  const [deleting, setDeleting] = useState(false);

  function startEditing() {
    setFileName(file.original_name || "");
    setComment(file.comment || "");
    setError("");
    setEditing(true);
  }

  function cancelEditing() {
    setFileName(file.original_name || "");
    setComment(file.comment || "");
    setError("");
    setEditing(false);
  }

  async function saveFile(event) {
    event.preventDefault();

    if (!fileName.trim()) {
      setError(
        "Имя файла не может быть пустым.",
      );
      return;
    }

    setError("");
    setSaving(true);

    try {
      const updatedFile = await updateFile(
        file.id,
        {
          original_name: fileName.trim(),
          comment,
        },
      );

      onUpdated(updatedFile);
      setEditing(false);
    } catch (requestError) {
      setError(
        getErrorMessage(requestError),
      );
    } finally {
      setSaving(false);
    }
  }

  async function handleDelete() {
    const confirmed = window.confirm(
      `Удалить файл «${file.original_name}»?`,
    );

    if (!confirmed) {
      return;
    }

    setError("");
    setDeleting(true);

    try {
      await deleteFile(file.id);
      onDeleted(file.id);
    } catch (requestError) {
      setError(
        getErrorMessage(requestError),
      );
    } finally {
      setDeleting(false);
    }
  }

  async function copyPublicLink() {
    const publicUrl = getPublicFileUrl(
      file.public_token,
    );

    try {
      await navigator.clipboard.writeText(
        publicUrl,
      );

      setError(
        "Публичная ссылка скопирована.",
      );
    } catch {
      setError(publicUrl);
    }
  }

  return (
    <article className="file-row">
      <div className="file-info">
        {!editing && (
          <h3>{file.original_name}</h3>
        )}

        <p>
          Размер: {formatFileSize(file.size)}
        </p>

        <p>
          Загружен:{" "}
          {formatDate(file.uploaded_at)}
        </p>

        <p>
          Последнее скачивание:{" "}
          {formatDate(file.last_downloaded_at)}
        </p>

        {!editing && (
          <p>
            Комментарий:{" "}
            {file.comment || "нет"}
          </p>
        )}

        {editing && (
          <form
            className="comment-form"
            onSubmit={saveFile}
          >
            <label htmlFor={`name-${file.id}`}>
              Имя файла
            </label>

            <input
              id={`name-${file.id}`}
              value={fileName}
              onChange={(event) => {
                setFileName(event.target.value);
              }}
              required
              autoFocus
            />

            <label htmlFor={`comment-${file.id}`}>
              Комментарий
            </label>

            <textarea
              id={`comment-${file.id}`}
              value={comment}
              onChange={(event) => {
                setComment(event.target.value);
              }}
              rows="3"
            />

            <div className="comment-actions">
              <button
                type="submit"
                disabled={
                  saving || !fileName.trim()
                }
              >
                {saving
                  ? "Сохранение..."
                  : "Сохранить"}
              </button>

              <button
                type="button"
                onClick={cancelEditing}
                disabled={saving}
              >
                Отмена
              </button>
            </div>
          </form>
        )}
      </div>

      <div className="file-actions">
        <a
          className="action-button"
          href={getDownloadUrl(file.id)}
          target="_blank"
          rel="noreferrer"
        >
          Скачать
        </a>

        {!editing && (
          <button
            type="button"
            onClick={startEditing}
          >
            Переименовать
          </button>
        )}

        <button
          type="button"
          onClick={copyPublicLink}
        >
          Публичная ссылка
        </button>

        <button
          type="button"
          onClick={handleDelete}
          disabled={deleting}
        >
          {deleting
            ? "Удаление..."
            : "Удалить"}
        </button>
      </div>

      {error && (
        <p className="form-error">
          {error}
        </p>
      )}
    </article>
  );
}


function FileManager({
  ownerId = null,
  ownerName = "",
}) {
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function loadFiles() {
    setError("");
    setLoading(true);

    try {
      const result = await getFiles(
        ownerId,
      );

      setFiles(
        Array.isArray(result)
          ? result
          : [],
      );
    } catch (requestError) {
      setError(
        getErrorMessage(requestError),
      );
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadFiles();
  }, [ownerId]);

  function handleUploaded(createdFile) {
    setFiles((currentFiles) => [
      createdFile,
      ...currentFiles,
    ]);
  }

  function handleUpdated(updatedFile) {
    setFiles((currentFiles) => (
      currentFiles.map((file) => (
        file.id === updatedFile.id
          ? updatedFile
          : file
      ))
    ));
  }

  function handleDeleted(fileId) {
    setFiles((currentFiles) => (
      currentFiles.filter(
        (file) => file.id !== fileId,
      )
    ));
  }

  return (
    <>
      <FileUploader
        ownerId={ownerId}
        onUploaded={handleUploaded}
      />

      <section className="cloud-card">
        <div className="section-header">
          <div>
            <h2>
              {ownerName
                ? `Файлы пользователя ${ownerName}`
                : "Мои файлы"}
            </h2>
          </div>

          <button
            type="button"
            onClick={loadFiles}
            disabled={loading}
          >
            Обновить
          </button>
        </div>

        {loading && (
          <p>Загрузка списка файлов...</p>
        )}

        {!loading && error && (
          <p className="form-error">
            {error}
          </p>
        )}

        {!loading
          && !error
          && files.length === 0
          && (
            <p>
              Файлов пока нет.
            </p>
          )}

        {!loading
          && !error
          && files.map((file) => (
            <FileRow
              key={file.id}
              file={file}
              onUpdated={handleUpdated}
              onDeleted={handleDeleted}
            />
          ))}
      </section>
    </>
  );
}


function AdminPanel() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [actionUserId, setActionUserId] = useState(null);

  const navigate = useNavigate();

  async function loadUsers() {
    setError("");
    setLoading(true);

    try {
      const result = await getUsers();

      setUsers(
        Array.isArray(result)
          ? result
          : [],
      );
    } catch (requestError) {
      setError(
        getErrorMessage(requestError),
      );
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadUsers();
  }, []);

  async function handleDeleteUser(user) {
    const confirmed = window.confirm(
      `Удалить пользователя «${user.username}»?`,
    );

    if (!confirmed) {
      return;
    }

    setError("");
    setActionUserId(user.id);

    try {
      await deleteUser(user.id);

      setUsers((currentUsers) => (
        currentUsers.filter(
          (currentUser) => (
            currentUser.id !== user.id
          ),
        )
      ));
    } catch (requestError) {
      setError(
        getErrorMessage(requestError),
      );
    } finally {
      setActionUserId(null);
    }
  }

  async function handleToggleAdmin(user) {
    setError("");
    setActionUserId(user.id);

    try {
      const updatedUser = await toggleUserAdmin(
        user.id,
      );

      setUsers((currentUsers) => (
        currentUsers.map((currentUser) => (
          currentUser.id === updatedUser.id
            ? updatedUser
            : currentUser
        ))
      ));
    } catch (requestError) {
      setError(
        getErrorMessage(requestError),
      );
    } finally {
      setActionUserId(null);
    }
  }

  return (
    <section className="cloud-card admin-card">
      <div className="section-header">
        <h2>Пользователи</h2>

        <button
          type="button"
          onClick={loadUsers}
          disabled={loading}
        >
          Обновить
        </button>
      </div>

      {loading && (
        <p>Загрузка пользователей...</p>
      )}

      {!loading && error && (
        <p className="form-error">
          {error}
        </p>
      )}

      {!loading
        && !error
        && users.length === 0
        && (
          <p>
            Пользователей пока нет.
          </p>
        )}

      {!loading
        && !error
        && users.map((user) => (
          <article
            className="admin-user-row"
            key={user.id}
          >
            <div className="admin-user-info">
              <h3>{user.username}</h3>

              <p>
                Имя: {user.full_name}
              </p>

              <p>
                Email: {user.email}
              </p>

              <p>
                Файлов:{" "}
                {user.files_count || 0}
              </p>

              <p>
                Размер:{" "}
                {formatFileSize(
                  user.files_size || 0,
                )}
              </p>

              <p>
                Статус:{" "}
                {user.is_app_admin
                  ? "Администратор"
                  : "Пользователь"}
              </p>

              <p>
                Состояние:{" "}
                {user.is_active
                  ? "Активен"
                  : "Отключён"}
              </p>
            </div>

            <div className="file-actions">
              <button
                type="button"
                onClick={() => {
                  navigate(
                    `/admin/storage/${user.id}`,
                  );
                }}
              >
                Открыть хранилище
              </button>

              <button
                type="button"
                onClick={() => {
                  handleToggleAdmin(user);
                }}
                disabled={
                  actionUserId === user.id
                }
              >
                {user.is_app_admin
                  ? "Снять администратора"
                  : "Сделать администратором"}
              </button>

              <button
                type="button"
                onClick={() => {
                  handleDeleteUser(user);
                }}
                disabled={
                  actionUserId === user.id
                }
              >
                {actionUserId === user.id
                  ? "Обработка..."
                  : "Удалить"}
              </button>
            </div>
          </article>
        ))}
    </section>
  );
}


function Navigation({
  user,
  onLogout,
}) {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  function getNavClass({
    isActive,
  }) {
    return isActive
      ? "nav-link active"
      : "nav-link";
  }

  async function handleLogout() {
    setError("");
    setLoading(true);

    try {
      await logoutUser();

      onLogout();

      navigate(
        "/login",
        {
          replace: true,
        },
      );
    } catch (requestError) {
      setError(
        getErrorMessage(requestError),
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      <nav className="app-nav">
        <NavLink
          to="/storage"
          className={getNavClass}
        >
          Хранилище
        </NavLink>

        {user.is_app_admin && (
          <NavLink
            to="/admin"
            className={getNavClass}
          >
            Администрирование
          </NavLink>
        )}

        <button
          type="button"
          onClick={handleLogout}
          disabled={loading}
        >
          {loading ? "Выход..." : "Выйти"}
        </button>
      </nav>

      {error && (
        <p className="form-error">
          {error}
        </p>
      )}
    </>
  );
}


function LandingPage() {
  const navigate = useNavigate();

  return (
    <section className="cloud-card landing-card">
      <h2>Облачное хранилище My Cloud</h2>

      <p>
        Загружай, храни, скачивай и отправляй
        файлы через публичные ссылки.
      </p>

      <div className="landing-actions">
        <button
          type="button"
          onClick={() => {
            navigate("/login");
          }}
        >
          Войти
        </button>

        <button
          type="button"
          onClick={() => {
            navigate("/register");
          }}
        >
          Зарегистрироваться
        </button>
      </div>
    </section>
  );
}


function AuthPage({
  mode,
  onSuccess,
  onSwitch,
}) {
  const navigate = useNavigate();

  function handleSuccess(nextUser) {
    onSuccess(nextUser);

    navigate(
      nextUser.is_app_admin
        ? "/admin"
        : "/storage",
      {
        replace: true,
      },
    );
  }

  function handleSwitch() {
    onSwitch();

    navigate(
      mode === "login"
        ? "/register"
        : "/login",
    );
  }

  return (
    <AuthForm
      mode={mode}
      onSuccess={handleSuccess}
      onSwitch={handleSwitch}
    />
  );
}


function ProtectedLayout({
  user,
  onLogout,
  children,
}) {
  if (!user) {
    return (
      <Navigate
        to="/login"
        replace
      />
    );
  }

  return (
    <>
      <Navigation
        user={user}
        onLogout={onLogout}
      />

      {children}
    </>
  );
}


function AdminStoragePage({
  user,
  onLogout,
}) {
  const { userId } = useParams();
  const navigate = useNavigate();

  const selectedUser = {
    id: Number(userId),
    username: `ID ${userId}`,
  };

  if (!user?.is_app_admin) {
    return (
      <Navigate
        to="/storage"
        replace
      />
    );
  }

  return (
    <ProtectedLayout
      user={user}
      onLogout={onLogout}
    >
      <section className="cloud-card">
        <div className="section-header">
          <h2>
            Управление хранилищем пользователя
          </h2>

          <button
            type="button"
            onClick={() => {
              navigate("/admin");
            }}
          >
            Назад к пользователям
          </button>
        </div>

        <p>
          Выбран пользователь:{" "}
          {selectedUser.username}
        </p>
      </section>

      <FileManager
        ownerId={selectedUser.id}
        ownerName={selectedUser.username}
      />
    </ProtectedLayout>
  );
}


function App() {
  const [user, setUser] = useState(null);
  const [status, setStatus] = useState(
    "Подключение к серверу...",
  );

  useEffect(() => {
    async function initializeApp() {
      try {
        await initializeCsrf();

        try {
          const currentUser = await getCurrentUser();

          setUser(currentUser);
          setStatus("");
        } catch {
          setStatus("");
        }
      } catch (error) {
        console.error(error);

        setStatus(
          "Не удалось подключиться к API.",
        );
      }
    }

    initializeApp();
  }, []);

  if (status) {
    return (
      <main className="app">
        <h1>My Cloud</h1>

        <p>{status}</p>
      </main>
    );
  }

  return (
    <main className="app">
      <h1>My Cloud</h1>

      <Routes>
        <Route
          path="/"
          element={
            user ? (
              <Navigate
                to="/storage"
                replace
              />
            ) : (
              <LandingPage />
            )
          }
        />

        <Route
          path="/login"
          element={
            user ? (
              <Navigate
                to={
                  user.is_app_admin
                    ? "/admin"
                    : "/storage"
                }
                replace
              />
            ) : (
              <AuthPage
                mode="login"
                onSuccess={(nextUser) => {
                  setUser(nextUser);
                }}
                onSwitch={() => {}}
              />
            )
          }
        />

        <Route
          path="/register"
          element={
            user ? (
              <Navigate
                to="/storage"
                replace
              />
            ) : (
              <AuthPage
                mode="register"
                onSuccess={(nextUser) => {
                  setUser(nextUser);
                }}
                onSwitch={() => {}}
              />
            )
          }
        />

        <Route
          path="/storage"
          element={
            <ProtectedLayout
              user={user}
              onLogout={() => {
                setUser(null);
              }}
            >
              <FileManager />
            </ProtectedLayout>
          }
        />

        <Route
          path="/admin"
          element={
            user?.is_app_admin ? (
              <ProtectedLayout
                user={user}
                onLogout={() => {
                  setUser(null);
                }}
              >
                <AdminPanel />
              </ProtectedLayout>
            ) : (
              <Navigate
                to={
                  user
                    ? "/storage"
                    : "/login"
                }
                replace
              />
            )
          }
        />

        <Route
          path="/admin/storage/:userId"
          element={
            <AdminStoragePage
              user={user}
              onLogout={() => {
                setUser(null);
              }}
            />
          }
        />

        <Route
          path="*"
          element={
            <Navigate
              to={
                user
                  ? "/storage"
                  : "/"
              }
              replace
            />
          }
        />
      </Routes>
    </main>
  );
}


export default App;