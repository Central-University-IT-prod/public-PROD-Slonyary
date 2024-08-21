import s from './Channel.module.scss'
import { FC, useEffect, useState } from 'react'
import MoreHorizIcon from '@mui/icons-material/MoreHoriz'
import { Avatar, Button } from '@mui/material'
import { Link } from 'react-router-dom'
import { channelInfoPath, NavigatePath } from '../../routes.ts'
import { channelsAPI } from '../../store/services/ChannelService.ts'
import { Loading } from '../Loading/Loading.tsx'
import { Bounce, toast } from 'react-toastify'

type Props = {
	title: string
	subscribers: number
	avatar: string
	posts: {
		pending: number
		moderation: number
	}
	id: number
}

const warningNotify = (text: string) =>
	toast.error(text, {
		position: 'top-center',
		autoClose: 5000,
		hideProgressBar: false,
		closeOnClick: true,
		pauseOnHover: true,
		draggable: true,
		progress: undefined,
		theme: 'light',
		transition: Bounce
	})

const Channel: FC<Props> = (props) => {
	const [showPopup, setShowPopup] = useState<boolean>(false)
	const [deleteChannel, { isLoading, error }] =
		channelsAPI.useDeleteChannelMutation()

	useEffect(() => {
		if (!isLoading && error !== undefined) {
			warningNotify('Ошибка!!!')
		}
	}, [error, isLoading])

	if (isLoading) return <Loading />
	return (
		<Link
			to={NavigatePath(channelInfoPath(props.id.toString()))}
			className={s.main}
		>
			<div className={s.avatarContainer}>
				{props.avatar ? (
					<img
						src={
							props.avatar.slice(0, 4) === 'http'
								? props.avatar
								: `data:image/gif;base64, ${props.avatar}`
						}
						alt=""
						className={s.avatar}
					/>
				) : (
					<Avatar sx={{ width: '60px', height: '60px' }}>
						{props.title.slice(0, 2)}
					</Avatar>
				)}
			</div>
			<div className={s.aboutChannel}>
				<h5 className={s.title}>{props.title}</h5>
				<p className={s.subscribers}>{props.subscribers} Подписчика</p>
			</div>
			<div className={s.posts}>
				<h5 className={s.postTitle}>Посты</h5>
				<div className={s.postStatus}>
					<div className={s.pending}></div>
					<p>Ожидают отправки: {props.posts.pending}</p>
				</div>
				<div className={s.postStatus}>
					<div className={s.moderation}></div>
					<p>На модерации: {props.posts.moderation}</p>
				</div>
			</div>
			<div
				onClick={(event) => {
					event.stopPropagation()
					event.preventDefault()
					setShowPopup((show) => !show)
				}}
				className={s.actions}
			>
				<button>
					<MoreHorizIcon sx={{ fontSize: 50 }} color="primary" />
				</button>
				{showPopup && (
					<div className={s.popup}>
						<Button onClick={() => deleteChannel(props.id)} variant="contained">
							Удалить
						</Button>
					</div>
				)}
			</div>
		</Link>
	)
}

export default Channel
