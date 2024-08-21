import React, { memo } from 'react'
import './ImageTable.css'
import Image from '../../Ui/Image/Image'
import { ImageList, ImageListItem } from '@mui/material'

interface IImageTable {
	files: File[]
	deleteImage: (e: React.MouseEvent<HTMLButtonElement>, index: number) => void
}
const ImageTable = memo(({ files, deleteImage }: IImageTable) => {
	return (
		<ImageList sx={{ width: '100%' }} cols={3} rowHeight={164}>
			{files.map((img, index) => (
				<ImageListItem key={index}>
					<Image img={img} deleteImage={deleteImage} index={index} />
				</ImageListItem>
			))}
		</ImageList>
	)
})

export default ImageTable
