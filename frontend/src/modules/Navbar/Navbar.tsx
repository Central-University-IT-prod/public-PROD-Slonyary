import { FC, Fragment, useState } from 'react'
import s from './Navbar.module.scss'
import { NavLink } from 'react-router-dom'
import { NavigatePath, paths } from '../../routes.ts'
import siteLogoImg from '../../assets/imgs/siteLogo.png'
import useAppSelector from '../../hooks/useAppSelector.ts'
import { useNavigate } from 'react-router'
import { Avatar, Button, Drawer } from '@mui/material'
import MenuIcon from '@mui/icons-material/Menu'
import CloseIcon from '@mui/icons-material/Close'

export const Navbar: FC = () => {
	const userData: any = useAppSelector((state) => state.user)
	const navigate = useNavigate()
	const [showMenu, setShowMenu] = useState<boolean>(false)

	if (!userData) navigate(paths.TELEGRAMAUTH)
	return (
		<header className={s.navBar}>
			<div className="container">
				<div className={s.inner}>
					<div className={s.burgerMenu}>
						<Fragment>
							<Button onClick={() => setShowMenu(true)}>
								<MenuIcon />
							</Button>
							<Drawer
								anchor={'left'}
								open={showMenu}
								onClose={() => setShowMenu(false)}
							>
								<div className={s.burgerMenuInner}>
									<div className={s.burgerMenuHeader}>
										<img src={siteLogoImg} alt="" className={s.logo} />
										<CloseIcon onClick={() => setShowMenu(false)} />
									</div>
									<NavLink
										onClick={() => setShowMenu(false)}
										className={({ isActive }) =>
											isActive ? `${s.link} ${s.active}` : s.link
										}
										to={NavigatePath(paths.HOME)}
									>
										Главная
									</NavLink>
									<NavLink
										onClick={() => setShowMenu(false)}
										className={({ isActive }) =>
											isActive ? `${s.link} ${s.active}` : s.link
										}
										to={NavigatePath(paths.CHANNELS)}
									>
										Мои каналы
									</NavLink>
								</div>
							</Drawer>
						</Fragment>
					</div>
					<div className={s.left}>
						<img src={siteLogoImg} alt="" className={s.logo} />
						<nav className={s.links}>
							<NavLink
								className={({ isActive }) =>
									isActive ? `${s.link} ${s.active}` : s.link
								}
								to={NavigatePath(paths.HOME)}
							>
								Главная
							</NavLink>
							<NavLink
								className={({ isActive }) =>
									isActive ? `${s.link} ${s.active}` : s.link
								}
								to={NavigatePath(paths.CHANNELS)}
							>
								Мои каналы
							</NavLink>
						</nav>
					</div>
					<div className={s.right}>
						<Avatar src={userData.photo_url} className={s.userLogo} />
						<span className={s.userName}>{userData.first_name}</span>
					</div>
				</div>
			</div>
		</header>
	)
}
