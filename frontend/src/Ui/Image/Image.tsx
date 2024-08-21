import { useEffect, useState } from 'react'

interface IImage {
	index: number
	deleteImage: (e: React.MouseEvent<HTMLButtonElement>, index: number) => void
	img: File
}

const Image = ({ index, deleteImage, img }: IImage) => {
	const deleteImageOnClick = (e: React.MouseEvent<HTMLButtonElement>) =>
		deleteImage(e, index)
	const [srcImage, setSrcImage] = useState(null)

	useEffect(() => {
		const reader = new FileReader()

		reader.onload = (event: any) => {
			const imageDataUrl = event.target.result
			setSrcImage(imageDataUrl)
		}
		reader.readAsDataURL(img)
	}, [img])

	return (
		<div className={`image-wrapper ${srcImage === null ? 'loaded' : ''}`}>
			{srcImage && <img src={srcImage} />}
			<div className="delete-btn-wrapper">
				<button className="delete" onClick={deleteImageOnClick}>
					<svg
						width="12"
						height="12"
						viewBox="0 0 12 12"
						fill="none"
						xmlns="http://www.w3.org/2000/svg"
					>
						<path d="M0.994858 1.00636C0.604334 1.39689 0.604334 2.03005 0.994859 2.42058L4.58001 6.00573L0.994856 9.59088C0.604333 9.98141 0.604333 10.6146 0.994857 11.0051C1.38538 11.3956 2.01855 11.3956 2.40907 11.0051L5.99422 7.41994L9.57936 11.0051C9.96989 11.3956 10.6031 11.3956 10.9936 11.0051C11.3841 10.6146 11.3841 9.98139 10.9936 9.59087L7.40844 6.00573L10.9936 2.42059C11.3841 2.03007 11.3841 1.3969 10.9936 1.00638C10.603 0.615854 9.96988 0.615854 9.57936 1.00638L5.99422 4.59152L2.40907 1.00636C2.01855 0.615839 1.38538 0.615839 0.994858 1.00636Z" />
					</svg>
				</button>
			</div>
		</div>
	)
}

export default Image
