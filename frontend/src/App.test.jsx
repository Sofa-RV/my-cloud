import {
  fireEvent,
  render,
  screen,
  waitFor,
} from "@testing-library/react";

import {
  MemoryRouter,
} from "react-router-dom";

import App from "./App";

import {
  getCurrentUser,
  getFiles,
  initializeCsrf,
  loginUser,
  registerUser,
} from "./services/api";


jest.mock(
  "./services/api",
  () => ({
    deleteFile: jest.fn(),
    deleteUser: jest.fn(),
    getCurrentUser: jest.fn(),
    getDownloadUrl: jest.fn(
      (fileId) => `/api/files/${fileId}/download/`,
    ),
    getFiles: jest.fn(),
    getPublicFileUrl: jest.fn(
      (token) => `/api/files/public/${token}/`,
    ),
    getUsers: jest.fn(),
    initializeCsrf: jest.fn(),
    loginUser: jest.fn(),
    logoutUser: jest.fn(),
    registerUser: jest.fn(),
    toggleUserAdmin: jest.fn(),
    updateFile: jest.fn(),
    uploadFile: jest.fn(),
  }),
);


function renderApp(
  initialEntries = ["/login"],
) {
  return render(
    <MemoryRouter
      initialEntries={initialEntries}
      future={{
        v7_startTransition: true,
        v7_relativeSplatPath: true,
      }}
    >
      <App />
    </MemoryRouter>,
  );
}


describe("App", () => {
  beforeEach(() => {
    jest.clearAllMocks();

    initializeCsrf.mockResolvedValue({});

    getCurrentUser.mockRejectedValue(
      new Error("Не авторизован"),
    );

    getFiles.mockResolvedValue([]);

    loginUser.mockResolvedValue({
      user: {
        id: 1,
        username: "testuser",
        full_name: "Тестовый пользователь",
        email: "test@example.com",
        is_app_admin: false,
      },
    });

    registerUser.mockResolvedValue({
      user: {
        id: 2,
        username: "newuser",
        full_name: "Новый пользователь",
        email: "new@example.com",
        is_app_admin: false,
      },
    });
  });

  test(
    "shows login form after API initialization",
    async () => {
      renderApp();

      expect(
        await screen.findByRole(
          "heading",
          {
            name: "Вход",
          },
        ),
      ).toBeInTheDocument();

      expect(
        screen.getByLabelText("Логин"),
      ).toBeInTheDocument();

      expect(
        screen.getByLabelText("Пароль"),
      ).toBeInTheDocument();
    },
  );

  test(
    "shows landing page",
    async () => {
      renderApp(["/"]);

      expect(
        await screen.findByRole(
          "heading",
          {
            name: "Облачное хранилище My Cloud",
          },
        ),
      ).toBeInTheDocument();

      expect(
        screen.getByRole(
          "button",
          {
            name: "Войти",
          },
        ),
      ).toBeInTheDocument();

      expect(
        screen.getByRole(
          "button",
          {
            name: "Зарегистрироваться",
          },
        ),
      ).toBeInTheDocument();
    },
  );

  test(
    "switches from login to registration",
    async () => {
      renderApp();

      await screen.findByRole(
        "heading",
        {
          name: "Вход",
        },
      );

      fireEvent.click(
        screen.getByRole(
          "button",
          {
            name: "Создать аккаунт",
          },
        ),
      );

      expect(
        await screen.findByRole(
          "heading",
          {
            name: "Регистрация",
          },
        ),
      ).toBeInTheDocument();

      expect(
        screen.getByLabelText("Email"),
      ).toBeInTheDocument();

      expect(
        screen.getByLabelText("Полное имя"),
      ).toBeInTheDocument();
    },
  );

  test(
    "shows error when registration passwords differ",
    async () => {
      renderApp();

      await screen.findByRole(
        "heading",
        {
          name: "Вход",
        },
      );

      fireEvent.click(
        screen.getByRole(
          "button",
          {
            name: "Создать аккаунт",
          },
        ),
      );

      await screen.findByRole(
        "heading",
        {
          name: "Регистрация",
        },
      );

      fireEvent.change(
        screen.getByLabelText("Логин"),
        {
          target: {
            value: "newuser",
          },
        },
      );

      fireEvent.change(
        screen.getByLabelText("Email"),
        {
          target: {
            value: "new@example.com",
          },
        },
      );

      fireEvent.change(
        screen.getByLabelText("Полное имя"),
        {
          target: {
            value: "Новый пользователь",
          },
        },
      );

      const passwordInput = screen.getByLabelText(
        "Пароль",
      );

      const passwordConfirmInput = screen.getByLabelText(
        "Повторите пароль",
      );

      fireEvent.change(
        passwordInput,
        {
          target: {
            value: "Password1!",
          },
        },
      );

      fireEvent.change(
        passwordConfirmInput,
        {
          target: {
            value: "DifferentPassword1!",
          },
        },
      );

      fireEvent.click(
        screen.getByRole(
          "button",
          {
            name: "Зарегистрироваться",
          },
        ),
      );

      expect(
        await screen.findByText(
          "Пароли не совпадают.",
        ),
      ).toBeInTheDocument();

      expect(
        registerUser,
      ).not.toHaveBeenCalled();
    },
  );

  test(
    "logs in and displays user panel",
    async () => {
      renderApp();

      await screen.findByRole(
        "heading",
        {
          name: "Вход",
        },
      );

      fireEvent.change(
        screen.getByLabelText("Логин"),
        {
          target: {
            value: "testuser",
          },
        },
      );

      fireEvent.change(
        screen.getByLabelText("Пароль"),
        {
          target: {
            value: "Password1!",
          },
        },
      );

      fireEvent.click(
        screen.getByRole(
          "button",
          {
            name: "Войти",
          },
        ),
      );

      expect(
        await screen.findByRole(
          "link",
          {
            name: "Хранилище",
          },
        ),
      ).toBeInTheDocument();

      expect(
        await screen.findByText(
          "Файлов пока нет.",
        ),
      ).toBeInTheDocument();

      await waitFor(() => {
        expect(
          loginUser,
        ).toHaveBeenCalledWith(
          {
            username: "testuser",
            password: "Password1!",
          },
        );
      });
    },
  );
});