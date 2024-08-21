import { createSlice, PayloadAction } from "@reduxjs/toolkit"

type TypeTheme = {
    type: string,
    data?: any
}

const initialState:TypeTheme = {
    type: '',
    data: {}
}

const modalSlice = createSlice({
    name: 'modal',
    initialState,
    reducers: {
        toggleModal: (state, action: PayloadAction<TypeTheme>) => {
            const payload = action.payload
            state = {type: payload.type, data: payload.data || {}}
            return state
        }
    }
})
export const  {actions,reducer } = modalSlice;