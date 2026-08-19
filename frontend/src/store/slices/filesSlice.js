import { createSlice } from "@reduxjs/toolkit";


const initialState = {
  items: [],
  isLoading: false,
  error: null,
};


const filesSlice = createSlice({
  name: "files",
  initialState,
  reducers: {
    setFiles(state, action) {
      state.items = action.payload;
      state.error = null;
    },

    clearFiles(state) {
      state.items = [];
      state.error = null;
    },

    setFilesLoading(state, action) {
      state.isLoading = action.payload;
    },

    setFilesError(state, action) {
      state.error = action.payload;
    },
  },
});


export const {
  setFiles,
  clearFiles,
  setFilesLoading,
  setFilesError,
} = filesSlice.actions;

export default filesSlice.reducer;