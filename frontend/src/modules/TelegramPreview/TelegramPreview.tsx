// @ts-ignore
import { FC } from 'react'
import { TelegramImagesGrid } from './TelegramImagesGrid.tsx'
import s from './TelegramPreview.module.scss'
import Tail from './Tail.tsx'
import { TelegramBg } from './TelegramBg.tsx'
import useModal from '../../hooks/useModal.ts'
import CloseIcon from '@mui/icons-material/Close'
import { Button } from '@mui/material'
import axios from 'axios'
import { BACKEND_HOST } from '../../constants.ts'

type Props = {
	htmlText: string
	images: File[]
	plainText: string
}

export const TelegramPreview: FC<{ data: Props }> = ({ data }) => {
	const { htmlText, images, plainText } = data
	const { closeOnClickWrapper, setModal } = useModal(
		'',
		`.${s.TelegramPreviewWrapper}`,
		{}
	)

	const previewTelega = async () => {
		const formData = new FormData()
		formData.append('html_text', htmlText)
		formData.append('plain_text', plainText)

		if (images?.length > 0) {
			for (let index = 0; index < images.length; index++) {
				const element = images[index]
				formData.append('files', element)
			}
		}

		await axios.post(`${BACKEND_HOST}/posts/draft`, formData, {
			headers: {
				token: localStorage.getItem('accessToken')
			}
		})
	}

	return (
		<div className={s.TelegramPreviewWrapper} onClick={closeOnClickWrapper}>
			<aside className={s.main}>
				<div className={s.header}>
					<h5>Предпросмотр</h5>
					<button onClick={setModal}>
						<CloseIcon />
					</button>
				</div>
				<div className={s.telegramMessage}>
					{images && <TelegramImagesGrid images={images} />}
					<div
						dangerouslySetInnerHTML={{ __html: htmlText }}
						className={s.textContainer}
					></div>
					<Tail className={s.tail} />
				</div>
				<Button
					onClick={previewTelega}
					sx={{ mt: '15px', ml: 'auto', display: 'block' }}
					variant="contained"
				>
					Посмотреть в телеграмм
				</Button>
				<TelegramBg className={s.background} />
			</aside>
		</div>
	)
}
