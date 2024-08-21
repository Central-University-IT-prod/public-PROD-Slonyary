import { useEffect, useState } from 'react'

interface IImage {
	img: File
}

const ImageForPreview = ({ img }: IImage) => {
	const [srcImage, setSrcImage] = useState(null)

	useEffect(() => {
		const reader = new FileReader()

		reader.onload = (event: any) => {
			const imageDataUrl = event.target.result
			setSrcImage(imageDataUrl)
		}
		reader.readAsDataURL(img)
	}, [img])

	return <>{srcImage && <img src={srcImage} />}</>
}

export default ImageForPreview
