import { FC } from 'react'
import s from './TelegramPreview.module.scss'
import ImageForPreview from '../../Ui/ImageForPreview/ImageForPreview'

type Props = {
	images: File[]
}

export const TelegramImagesGrid: FC<Props> = (props) => {
	return (
		<div className={`${s.imagesGrid} ${s['length' + props.images.length]}`}>
			{props.images.map((image, index) => (
				<ImageForPreview img={image} key={index} />
			))}
		</div>
	)
}
