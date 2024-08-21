import { createSlice } from "@reduxjs/toolkit"

type TypeAuth = {
    isAuth: boolean | null,
}

const initialState:TypeAuth = {
    isAuth: null
}

const themeSlice = createSlice({
    name: 'auth',
    initialState,
    reducers: {
        setAuth: (state, action) => {
            state = action.payload
            return state
        }
    }
})
export const  {actions,reducer } = themeSlice;