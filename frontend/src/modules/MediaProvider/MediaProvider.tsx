import {
	createContext,
	ReactNode,
	useCallback,
	useContext,
	useState
} from 'react'
import useModal from '../../hooks/useModal'

const MediaContext = createContext({})

interface props {
	children: ReactNode
	mediaCount: number
}
const MediaProvider = ({ children, mediaCount }: props) => {
	const [media, setMedia] = useState([])
	const modalPath = 'MEDIA-SLIDER-MODAL'
	const { setModal } = useModal(modalPath, null, { media, mediaCount })

	type TypeFileObject = { index: number; src: string }
	const addMedia = (fileObject: TypeFileObject) => {
		const index = fileObject.index
		setMedia((prevMedia) => {
			const updatedMedia: any = [...prevMedia] // Создаем копию исходного массива
			updatedMedia[index] = fileObject // Заменяем элемент по указанному индексу
			return updatedMedia // Обновляем состояние
		})
	}

	const openSlider = useCallback(
		(index: number) => {
			if (media.length < mediaCount) return

			setModal({ startIndex: index })
		},
		[media]
	)

	return (
		<MediaContext.Provider value={{ media, addMedia, openSlider }}>
			{children}
		</MediaContext.Provider>
	)
}

const useMediaContext = () => {
	const context = useContext(MediaContext)
	if (!context) {
		throw new Error('useMediaContext must be used within a MediaProvider')
	}
	return context
}

export { MediaProvider, useMediaContext }
