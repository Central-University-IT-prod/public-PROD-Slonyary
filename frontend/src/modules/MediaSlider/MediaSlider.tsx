import { useMemo, useState } from 'react'
import './MediaSlider.css'
import useModal from '../../hooks/useModal'
import CloseIcon from '@mui/icons-material/Close'

const MediaSlider = ({ data }: any) => {
	const { media, mediaCount, startIndex } = data
	const [index, setIndex] = useState(startIndex)
	const leftDisabled = index <= 0
	const rightDisabled = index >= mediaCount - 1
	const { setModal } = useModal('', null, {})

	const mediaElement = useMemo(() => {
		const element = media[index]

		switch (element.mediaType) {
			case 'image':
				return (
					<img src={`data:image/gif;base64, ${element.src}`} loading="lazy" />
				)
			default:
				return (
					<img src={`data:image/gif;base64, ${element.src}`} loading="lazy" />
				)
		}
	}, [index])

	const changeIndex = (x: number) => {
		const newIndex = index + x

		if (newIndex > mediaCount - 1 || newIndex < 0) return

		setIndex(newIndex)
	}

	return (
		<div className="MediaSlider__wrapper">
			<div className="tool-bar-menu">
				<div className="element-index">
					<span>{`${index + 1}/${mediaCount}`}</span>
				</div>
				<button className="close-modal" onClick={setModal}>
					<CloseIcon />
				</button>
			</div>
			<div className="slider">
				<button
					className={`back-btn control-btn ${leftDisabled && 'disabled'}`}
					onClick={() => changeIndex(-1)}
					disabled={leftDisabled}
				>
					<div className="left-arrow__wrapper arrow-wrapper">
						<svg
							viewBox="0 0 14 28"
							fill="none"
							xmlns="http://www.w3.org/2000/svg"
						>
							<path
								d="M13 26.25L1.33337 14L13 1.75"
								strokeWidth="2"
								strokeLinecap="round"
								strokeLinejoin="round"
							/>
						</svg>
					</div>
				</button>
				<div className="media">{mediaElement}</div>
				<button
					className={`next-btn control-btn ${rightDisabled && 'disabled'}`}
					onClick={() => changeIndex(1)}
					disabled={rightDisabled}
				>
					<div className="right-arrow__wrapper arrow-wrapper">
						<svg
							viewBox="0 0 17 34"
							fill="none"
							xmlns="http://www.w3.org/2000/svg"
						>
							<path
								d="M1.625 1.25L15.3333 17L1.625 32.75"
								strokeWidth="2"
								strokeLinecap="round"
								strokeLinejoin="round"
							/>
						</svg>
					</div>
				</button>
			</div>
		</div>
	)
}

export default MediaSlider
