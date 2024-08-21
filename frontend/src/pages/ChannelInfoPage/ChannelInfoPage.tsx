import s from './ChannelInfoPage.module.scss'
import { useParams } from 'react-router'
import { channelsAPI } from '../../store/services/ChannelService.ts'
import { Loading } from '../../modules/Loading/Loading.tsx'
import { Avatar, Button } from '@mui/material'
import { Bounce, toast } from 'react-toastify'

const translateStatus = (status: string): string => {
	const russianWords = {
		owner: 'владелец',
		moderator: 'модератор',
		redactor: 'редактор'
	}

	// @ts-ignore
	return status in russianWords ? russianWords[status] : ''
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

const successNotify = (text: string) =>
	toast.success(text, {
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

const ChannelInfoPage = () => {
	const params = useParams()
	const { data: channel, isLoading } = channelsAPI.useGetChannelByIdQuery(
		params.id
	)
	if (isLoading) return <Loading />
	if (!channel) return <p>Канал не найден</p>
	return (
		<section className={s.main}>
			<div className={s.infoContainer}>
				<div className={s.left}>
					{channel.photo_url ? (
						<img
							src={
								channel.photo_url.slice(0, 4) === 'http'
									? channel.photo_url
									: `data:image/gif;base64, ${channel.photo_url}`
							}
							className={s.avatar}
							alt=""
						/>
					) : (
						<Avatar>{channel.name.slice(0, 2)}</Avatar>
					)}
					<div className={s.infoText}>
						<h3 className={s.channelTitle}>{channel.name}</h3>
						<a
							target="_blank"
							href={`https://t.me/${channel.username.slice(1)}`}
						>
							<p className={s.channelLink}>{channel.username}</p>
						</a>
						<p className={s.channelDescription}>{channel.description ?? ''}</p>
					</div>
				</div>
				<div className={s.right}>
					<div className={s.members}>
						<h5 className={s.membersTitle}>Участники</h5>
						<div className={s.membersList}>
							{channel.workers.map((user: any, index: number) => (
								<div className={s.user} key={user.id}>
									<span className={s.number}>{index + 1}.</span>
									<div className={s.userText}>
										<h5 className={s.userName}>{user.name}</h5>
										<p className={s.userStatus + ' ' + s[user.role]}>
											{translateStatus(user.role)}
										</p>
									</div>
								</div>
							))}
							<div className={s.memberLinks}>
								<Button
									sx={{ width: '100%' }}
									onClick={() => {
										navigator.clipboard
											.writeText(
												`https://t.me/StackSMM_Bot?start=invite${channel.id}_editor`
											)
											.then(
												function () {
													successNotify(
														'Ссылка успешно скопирован в буфер обмена!'
													)
												},
												function (err) {
													warningNotify(
														'Произошла ошибка при копировании текста: ' + err
													)
												}
											)
									}}
									variant="contained"
								>
									Добавить модератора
								</Button>
								<Button
									sx={{ width: '100%' }}
									variant="contained"
									onClick={() => {
										navigator.clipboard
											.writeText(
												`https://t.me/StackSMM_Bot?start=invite${channel.id}_editor`
											)
											.then(
												function () {
													successNotify(
														'Ссылка успешно скопирован в буфер обмена!'
													)
												},
												function (err) {
													warningNotify(
														'Произошла ошибка при копировании текста: ' + err
													)
												}
											)
									}}
								>
									Добавить редактора
								</Button>
							</div>
						</div>
					</div>
				</div>
			</div>
		</section>
	)
}

export default ChannelInfoPage
