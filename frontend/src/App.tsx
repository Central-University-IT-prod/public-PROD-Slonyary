import { useEffect, useMemo } from 'react'
import './App.css'
import { Outlet, useLocation, useNavigate } from 'react-router-dom'
import { createTheme, ThemeProvider } from '@mui/material'
import useAppSelector from './hooks/useAppSelector'
import { Navbar } from './modules/Navbar/Navbar.tsx'
import MediaSlider from './modules/MediaSlider/MediaSlider.tsx'
import { TelegramPreview } from './modules/TelegramPreview/TelegramPreview.tsx'
import { useActions } from './hooks/useActions.ts'
import { ToastContainer } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'
import { NavigatePath, paths } from './routes.ts'

function App() {
	const { mode: themeMode } = useAppSelector((state) => state.theme)
	const user = useAppSelector((state) => state.user)
	const { type, data } = useAppSelector((state) => state.modal)
	const { isAuth } = useAppSelector((state) => state.auth)
	const { setUser, setAuth } = useActions()
	const navigate = useNavigate()
	const location = useLocation()

	const theme = useMemo(
		() =>
			createTheme({
				palette: {
					mode: themeMode,
					primary: {
						main: '#5578e3'
					}
				}
			}),
		[themeMode]
	)

	useEffect(() => {
		if (isAuth === true || isAuth === null) return

		if (user?.id || location.pathname === '/' + paths.TELEGRAMAUTH) return

		navigate(NavigatePath(paths.TELEGRAMAUTH))
	}, [location.pathname, isAuth])

	useEffect(() => {
		const body = document.querySelector('body')
		body?.setAttribute('theme', themeMode)
	}, [themeMode])

	useEffect(() => {
		const data = localStorage.getItem('userData')
		if (data) {
			setUser(JSON.parse(data))
			setAuth(true)
		} else {
			setAuth(false)
		}
	}, [])

	return (
		<div className="App">
			<ThemeProvider theme={theme}>
				<Navbar />
				<div className="container">
					<Outlet />
					{type === 'MEDIA-SLIDER-MODAL' && <MediaSlider data={data} />}
					{type === 'TELEGRAM-PREVIEW' && <TelegramPreview data={data} />}
				</div>
			</ThemeProvider>
			<ToastContainer
				position="top-center"
				autoClose={5000}
				hideProgressBar={false}
				newestOnTop={false}
				closeOnClick
				rtl={false}
				pauseOnFocusLoss
				draggable
				pauseOnHover
				theme="light"
			/>
		</div>
	)
}

export default App
