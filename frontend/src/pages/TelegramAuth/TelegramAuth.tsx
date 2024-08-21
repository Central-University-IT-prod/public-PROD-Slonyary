// @ts-ignore
import TelegramLoginButton from 'react-telegram-login'
import { FC } from 'react'
import axios from 'axios'
import { BACKEND_HOST } from '../../constants'
import { useActions } from '../../hooks/useActions'
import './TelegramAuth.scss'
import { useNavigate } from 'react-router'
import { NavigatePath, paths } from '../../routes'

export const TelegramAuth: FC = () => {
	const { setUser } = useActions()
	const navigate = useNavigate()

	const handleTelegramResponse = async (response: any) => {
		if (response) {
			setUser(response)

			const res = await axios.post(`${BACKEND_HOST}/auth`, {
				...response
			})

			if (res) {
				localStorage.setItem('accessToken', res.data.token)
				localStorage.setItem('userData', JSON.stringify(response))
				setUser(response)
				navigate(NavigatePath(paths.HOME))
			}
		}
	}

	return (
		<div className="TelegramAuth">
			<h4>Авторизация</h4>
			<TelegramLoginButton
				className="auth-btn"
				dataOnauth={handleTelegramResponse}
				botName="StackSMM_Bot"
			/>
		</div>
	)
}
