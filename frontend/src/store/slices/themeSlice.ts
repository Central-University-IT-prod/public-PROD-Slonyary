import { createSlice } from "@reduxjs/toolkit"
import { THEME_KEY } from "../../constants"

type typeThemeModes =  "dark" | "light"
type TypeTheme = {
    mode: typeThemeModes,
}

const initialState:TypeTheme = {
    mode: localStorage.getItem(THEME_KEY) as  typeThemeModes | undefined ?? "light"
}

const themeSlice = createSlice({
    name: 'theme',
    initialState,
    reducers: {
        changeTheme: (state) => {
            const newMode = state.mode === 'dark' ? 'light' : 'dark'
            state.mode = newMode;
            localStorage.setItem(THEME_KEY, newMode)
            return state;
        }
    }
})
export const  {actions,reducer } = themeSlice;