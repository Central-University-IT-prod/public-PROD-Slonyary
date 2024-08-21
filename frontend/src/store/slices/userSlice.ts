import {createSlice, PayloadAction} from "@reduxjs/toolkit"
import {IUserModel} from "../../models/UserModels"

const initialState: IUserModel | any = {}

const userSlice = createSlice({
  name: 'user',
  initialState,
  reducers: {
    setUser: (state, action: PayloadAction<IUserModel>) => {
      state = action.payload
      return state
    }
  }
})
export const {actions, reducer} = userSlice;