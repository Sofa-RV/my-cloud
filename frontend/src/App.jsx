import { useEffect, useState } from "react";


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
      if (
        !isLogin
        && form.password !== form.passwordConfirm
      ) {
        throw new Error(
          "Пароли не совпадают.",
        );
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
  const [comment, setComment] = useState(
    file.comment || "",
  );
  const [error, setError] = useState("");
  const [saving, setSaving] = useState(false);
  const [deleting, setDeleting] = useState(false);

  function startEditing() {
    setComment(file.comment || "");
    setError("");
    setEditing(true);
  }

  function cancelEditing() {
    setComment(file.comment || "");
    setError("");
    setEditing(false);
  }

  async function saveComment(event) {
    event.preventDefault();

    setError("");
    setSaving(true);

    try {
      const updatedFile = await updateFile(
        file.id,
        {
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
        <h3>{file.original_name}</h3>

        <p>
          Размер: {formatFileSize(file.size)}
        </p>

        <p>
          Загружен:{" "}
          {formatDate(file.uploaded_at)}
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
            onSubmit={saveComment}
          >
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
              autoFocus
            />

            <div className="comment-actions">
              <button
                type="submit"
                disabled={saving}
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
            Изменить
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


function FileManager() {
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function loadFiles() {
    setError("");
    setLoading(true);

    try {
      const result = await getFiles();

      setFiles(result);
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
  }, []);

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
        onUploaded={handleUploaded}
      />

      <section className="cloud-card">
        <div className="section-header">
          <h2>Мои файлы</h2>

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

  async function loadUsers() {
    setError("");
    setLoading(true);

    try {
      const result = await getUsers();

      setUsers(result);
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


function UserPanel({
  user,
  onLogout,
}) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleLogout() {
    setError("");
    setLoading(true);

    try {
      await logoutUser();

      onLogout();
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
      <section className="user-card">
        <div>
          <h2>
            Добро пожаловать,{" "}
            {user.full_name || user.username}
          </h2>

          <p>
            Логин: {user.username}
          </p>

          <p>
            Email: {user.email || "не указан"}
          </p>
        </div>

        <button
          type="button"
          onClick={handleLogout}
          disabled={loading}
        >
          {loading ? "Выход..." : "Выйти"}
        </button>

        {error && (
          <p className="form-error">
            {error}
          </p>
        )}
      </section>

      <FileManager />

      {user.is_app_admin && (
        <AdminPanel />
      )}
    </>
  );
}


function App() {
  const [user, setUser] = useState(null);
  const [mode, setMode] = useState("login");
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

      {user ? (
        <UserPanel
          user={user}
          onLogout={() => setUser(null)}
        />
      ) : (
        <AuthForm
          mode={mode}
          onSuccess={(nextUser) => {
            setUser(nextUser);
          }}
          onSwitch={() => {
            setMode((currentMode) => (
              currentMode === "login"
                ? "register"
                : "login"
            ));
          }}
        />
      )}
    </main>
  );
}


export default App;