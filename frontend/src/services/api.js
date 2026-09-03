import axios from "axios";


const API_ORIGIN = "";


const apiClient = axios.create({
  baseURL: `${API_ORIGIN}/api`,
  withCredentials: true,
  xsrfCookieName: "csrftoken",
  xsrfHeaderName: "X-CSRFToken",
  headers: {
    Accept: "application/json",
  },
});


function getCookie(name) {
  const cookies = document.cookie.split(";");

  for (const cookie of cookies) {
    const trimmedCookie = cookie.trim();

    if (
      trimmedCookie.startsWith(
        `${name}=`,
      )
    ) {
      return decodeURIComponent(
        trimmedCookie.slice(name.length + 1),
      );
    }
  }

  return null;
}


apiClient.interceptors.request.use(
  (config) => {
    const csrfToken = getCookie(
      "csrftoken",
    );

    if (csrfToken) {
      config.headers = {
        ...config.headers,
        "X-CSRFToken": csrfToken,
      };
    }

    return config;
  },
  (error) => Promise.reject(error),
);


export async function initializeCsrf() {
  await apiClient.get("/auth/csrf/");
}


export async function getCurrentUser() {
  const response = await apiClient.get(
    "/auth/me/",
  );

  return response.data;
}


export async function registerUser(data) {
  const response = await apiClient.post(
    "/auth/register/",
    data,
  );

  return response.data;
}


export async function loginUser(data) {
  const response = await apiClient.post(
    "/auth/login/",
    data,
  );

  return response.data;
}


export async function logoutUser() {
  const response = await apiClient.post(
    "/auth/logout/",
  );

  return response.data;
}


export async function getFiles(
  ownerId = null,
) {
  const params = {};

  if (ownerId !== null) {
    params.owner_id = ownerId;
  }

  const response = await apiClient.get(
    "/files/",
    {
      params,
    },
  );

  return response.data;
}


export async function uploadFile(
  file,
  comment,
  ownerId = null,
) {
  const formData = new FormData();

  formData.append(
    "file",
    file,
  );

  formData.append(
    "comment",
    comment,
  );

  if (ownerId !== null) {
    formData.append(
      "owner_id",
      ownerId,
    );
  }

  const response = await apiClient.post(
    "/files/upload/",
    formData,
  );

  return response.data;
}


export async function updateFile(
  fileId,
  data,
) {
  const response = await apiClient.patch(
    `/files/${fileId}/`,
    data,
  );

  return response.data;
}


export async function deleteFile(
  fileId,
) {
  await apiClient.delete(
    `/files/${fileId}/`,
  );
}


export function getDownloadUrl(
  fileId,
) {
  return (
    `${API_ORIGIN}/api/files/`
    + `${fileId}/download/`
  );
}


export function getPublicFileUrl(
  token,
) {
  return (
    `${API_ORIGIN}/api/files/public/`
    + `${token}/`
  );
}


export async function getUsers() {
  const response = await apiClient.get(
    "/auth/users/",
  );

  return response.data;
}


export async function deleteUser(
  userId,
) {
  await apiClient.delete(
    `/auth/users/${userId}/`,
  );
}


export async function toggleUserAdmin(
  userId,
) {
  const response = await apiClient.patch(
    `/auth/users/${userId}/admin/`,
  );

  return response.data;
}


export default apiClient;
