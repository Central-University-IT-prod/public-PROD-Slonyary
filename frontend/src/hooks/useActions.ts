import { useDispatch } from "react-redux"
import {actions as userActions} from '../store/slices/userSlice'
import { useMemo } from "react"
import { bindActionCreators } from "@reduxjs/toolkit"
import { actions as themeActions } from "../store/slices/themeSlice"
import { actions as modalActions } from "../store/slices/modalSlice"
import { actions as authActions } from "../store/slices/authSlice"

const rootActions = {
    ...userActions,
    ...themeActions,
    ...modalActions,
    ...authActions
}

export const useActions = () => {
    const dispatch = useDispatch()
    return useMemo(() => bindActionCreators(rootActions, dispatch), [dispatch])
}