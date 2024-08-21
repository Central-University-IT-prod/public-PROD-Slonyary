import {combineReducers, configureStore} from "@reduxjs/toolkit";
import {reducer as userReducer} from "./slices/userSlice";
import {reducer as themeReducer} from "./slices/themeSlice";
import {reducer as modalReducer} from "./slices/modalSlice";
import {postsAPI} from "./services/PostsService.ts";
import {channelsAPI} from "./services/ChannelService.ts";
import { reducer as authReducer } from "./slices/authSlice.ts";

const reducer = combineReducers({
  user: userReducer,
  theme: themeReducer,
  modal: modalReducer,
  auth: authReducer,
  [postsAPI.reducerPath]: postsAPI.reducer,
  [channelsAPI.reducerPath]: channelsAPI.reducer,
})

export const store = configureStore({
  reducer,
  middleware: (getDefaultMiddleware) => getDefaultMiddleware().concat(postsAPI.middleware, channelsAPI.middleware)
})

export type RootState = ReturnType<typeof store.getState>