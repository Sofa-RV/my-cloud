import { createSlice } from "@reduxjs/toolkit";


const initialState = {
  user: null,
  isAuthenticated: false,
  isLoading: false,
  error: null,
};


const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    setUser(state, action) {
      state.user = action.payload;
      state.isAuthenticated = Boolean(action.payload);
      state.error = null;
    },

    clearUser(state) {
      state.user = null;
      state.isAuthenticated = false;
      state.error = null;
    },

    setAuthLoading(state, action) {
      state.isLoading = action.payload;
    },

    setAuthError(state, action) {
      state.error = action.payload;
    },
  },
});


export const {
  setUser,
  clearUser,
  setAuthLoading,
  setAuthError,
} = authSlice.actions;

export default authSlice.reducer;