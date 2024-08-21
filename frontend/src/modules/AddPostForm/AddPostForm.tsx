// @ts-ignore

import React, { FC, useCallback, useMemo, useState } from 'react'
import {
	CompositeDecorator,
	ContentBlock,
	ContentState,
	DraftDecorator,
	DraftEntityMutability,
	DraftEntityType,
	Editor,
	EditorState,
	RichUtils
} from 'draft-js'
import { stateToHTML } from 'draft-js-export-html'
import {
	Avatar,
	Button,
	Checkbox,
	CircularProgress,
	Grid,
	TextField
} from '@mui/material'
import FormatBoldIcon from '@mui/icons-material/FormatBold'
import FormatItalicIcon from '@mui/icons-material/FormatItalic'
import FormatUnderlinedIcon from '@mui/icons-material/FormatUnderlined'
import FormatStrikethroughIcon from '@mui/icons-material/FormatStrikethrough'
import LinkIcon from '@mui/icons-material/Link'
import ImageIcon from '@mui/icons-material/Image'
import './AddPostForm.scss'
import ImageTable from '../ImageTable/ImageTable'
import { addImageToPost, addMessages, getSpellcheckingWords } from './API'
import useModal from '../../hooks/useModal'
import { channelsAPI } from '../../store/services/ChannelService'
import axios from 'axios'
import { BACKEND_HOST } from '../../constants'
import { Bounce, toast } from 'react-toastify'

const AddPostForm: FC = () => {
	const [date, setDate] = useState('')
	const [time, setTime] = useState('00:00')
	const [ChannelsTarget, setChannelsTarget] = useState(false)
	const [isGptLoading, setIsGptLoading] = useState<boolean | null>(null)
	const [GPTText, setGPTText] = useState<string>('')

	let options = {
		inlineStyles: {
			BOLD: { element: 'b' },
			ITALIC: {
				element: 'i'
			},
			STRIKETHROUGH: {
				element: 's'
			},
			UNDERLINE: {
				element: 'u'
			}
		}
	}

	const maxLength = 9
	type LinkProps = {
		children: React.ReactNode
		contentState: ContentState
		entityKey: string
	}

	const Link: FC<LinkProps> = ({ contentState, entityKey, children }) => {
		const { url } = contentState.getEntity(entityKey).getData()

		const handlerClick = () => alert(`URL: ${url}`)

		return (
			<a href={url} onClick={handlerClick}>
				{children}
			</a>
		)
	}

	const decorator: DraftDecorator = {
		strategy: findLinkEntities,
		component: Link
	}

	const dec = new CompositeDecorator([decorator])
	const [editorState, setEditorState] = useState<EditorState>(() =>
		EditorState.createEmpty(dec)
	)
	const [spellcheckingString, setSpellcheckingString] = useState<string>('')
	const [isSpellcheckingLoading, setIsSpellcheckingLoading] =
		useState<boolean>(false)
	enum InlineStyle {
		BOLD = 'BOLD',
		ITALIC = 'ITALIC',
		UNDERLINE = 'UNDERLINE',
		STRIKE = 'STRIKETHROUGH'
	}
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

	const handleKeyCommand = (command: string, editorState: EditorState) => {
		const newState = RichUtils.handleKeyCommand(editorState, command)
		if (newState) {
			setEditorState(newState)
			return 'handled'
		}
		return 'not-handled'
	}

	const onBoldClick = () => {
		setEditorState(RichUtils.toggleInlineStyle(editorState, InlineStyle.BOLD))
	}

	const onItalicClick = () => {
		setEditorState(RichUtils.toggleInlineStyle(editorState, InlineStyle.ITALIC))
	}

	const onUnderLineClick = () => {
		setEditorState(
			RichUtils.toggleInlineStyle(editorState, InlineStyle.UNDERLINE)
		)
	}

	const onStrikeClick = () => {
		setEditorState(RichUtils.toggleInlineStyle(editorState, InlineStyle.STRIKE))
	}

	const getText = async () => {
		const contentState = editorState.getCurrentContent()
		let html = stateToHTML(contentState, options).replace(/<br>/g, '\n')
		const text = contentState.getPlainText()

		let publish_time: string = ''

		if (date) {
			const [year, month, day] = date.split('-')
			const [hours, minut] = time.split(':')

			publish_time = new Date(+year, +month - 1, +day, +hours, +minut)
				.toISOString()
				.replace('Z', '')
		}

		const channels: any[] = []

		document.querySelectorAll('.channelsCheckbox').forEach((i) => {
			const input = i.querySelector('input')
			const id = i.getAttribute('data-id')

			if (input?.checked) {
				channels.push({ id: Number(id), type: 'tg' })
			}
		})

		const data = {
			publish_time: publish_time ? publish_time : null,
			channels: channels,
			plain_text: text,
			html_text: html
		}

		const { id } = await addMessages(data)

		for (let index = 0; index < files.length; index++) {
			const form = new FormData()
			form.append('file', files[index])
			addImageToPost(id, form)
		}
		console.log(id)
		if (id) {
			setEditorState(() => EditorState.createEmpty(dec))
			setDate('')
			setTime('00:00')
			setIsGptLoading(null)
			setFiles([])
			setGPTText('')
			setSpellcheckingString('')
			setIsSpellcheckingLoading(false)
			document.querySelectorAll('')

			successNotify('Пост успешно создан')
		}
	}

	const addEntity = useCallback(
		(
			entityType: DraftEntityType,
			data: Record<string, string>,
			mutability: DraftEntityMutability
		) => {
			setEditorState((currentState) => {
				const contentState = currentState.getCurrentContent()
				const contentStateWithEntity = contentState.createEntity(
					entityType,
					mutability,
					data
				)
				const entityKey = contentStateWithEntity.getLastCreatedEntityKey()
				const newState = EditorState.set(currentState, {
					currentContent: contentStateWithEntity
				})
				return RichUtils.toggleLink(
					newState,
					newState.getSelection(),
					entityKey
				)
			})
		},
		[]
	)

	const addLink = useCallback(
		(url: string) => addEntity('link', { url }, 'MUTABLE'),
		[addEntity]
	)

	const handlerAddLink = () => {
		const url = prompt('URL:')

		if (!url) return
		addLink(url)
	}
	type TypeFileList = FileList | null

	function findLinkEntities(
		contentBlock: ContentBlock,
		callback: (start: number, end: number) => void,
		contentState: ContentState
	): void {
		contentBlock.findEntityRanges((character) => {
			const entityKey = character.getEntity()
			return (
				entityKey !== null &&
				contentState.getEntity(entityKey).getType() === 'link'
			)
		}, callback)
	}

	const [files, setFiles] = useState<File[]>([])

	const onDragEnter = (e: any) => {
		e.preventDefault()
		e.stopPropagation()
	}

	const filterFiles = (newFiles: TypeFileList): File[] => {
		if (!newFiles) return []

		const res: File[] = [...files]
		for (let index = newFiles.length - 1; index >= 0; index--) {
			const file = newFiles[index]

			if (res.length === maxLength) break

			if ('image/jpeg,image/png'.split(',').includes(file.type)) {
				res.push(file)
			} else {
			}
		}
		return res
	}

	const onDrop = (e: any) => {
		e.preventDefault()
		e.stopPropagation()
		setFiles(filterFiles(e.dataTransfer.files))
	}

	const changeInput = (e: React.ChangeEvent<HTMLInputElement>) => {
		e.preventDefault()
		e.stopPropagation()
		const input = document.querySelector(
			'#upload-postImage'
		) as HTMLInputElement
		setFiles(filterFiles(input.files))
	}

	const deleteMedia = (
		e: React.MouseEvent<HTMLButtonElement>,
		index: number
	) => {
		e.preventDefault()
		e.stopPropagation()

		const arrFiles = [...files]
		arrFiles.splice(index, 1)
		setFiles(arrFiles)
	}

	const { setModal } = useModal('TELEGRAM-PREVIEW', null, {})

	const spellchecking = async () => {
		setIsSpellcheckingLoading(true)

		const contentState = editorState.getCurrentContent()
		const html = stateToHTML(contentState, options)

		const words = await getSpellcheckingWords(html)

		let text = html
		let displacement = 0

		for (let index = 0; index < words.length; index++) {
			const element = words[index]
			const { pos, len, s } = element
			const word = s[0].replace(/^,+/, '')

			const leftStr = text.slice(0, pos + displacement)
			const rightStr = text.slice(pos + len + displacement)

			text = leftStr + word + rightStr
			const newDisplacement = word.length - len
			displacement += newDisplacement
		}

		setSpellcheckingString(text)
		setIsSpellcheckingLoading(false)
	}

	const gpt = async () => {
		try {
			setSpellcheckingString('')
			const contentState = editorState.getCurrentContent()
			const text = contentState.getPlainText()

			if (!text.length) return
			setIsGptLoading(true)

			const gptData = await axios.get(
				`${BACKEND_HOST}/gpt_response?prompt=${text}`,
				{
					headers: {
						token: localStorage.getItem('accessToken')
					}
				}
			)

			if (gptData) {
				setGPTText(gptData.data)
			}
			setIsGptLoading(false)
		} catch (error) {
			console.log(error)
		}
	}

	const spellcheckingBtnDisabled = useMemo(
		() => editorState.getCurrentContent().getPlainText().trim().length < 2,
		[editorState]
	)

	const { data: channels, isLoading } = channelsAPI.useGetChannelsQuery(null)

	const continueDisabled = useMemo(
		() => spellcheckingBtnDisabled,
		[spellcheckingBtnDisabled]
	)

	const mainBtn = useMemo(
		() => !ChannelsTarget || continueDisabled,
		[ChannelsTarget, continueDisabled]
	)

	const toggleChannels = (e: React.ChangeEvent<HTMLInputElement>) => {
		if (e.target.checked) {
			setChannelsTarget(true)
		} else {
			const h =
				document.querySelectorAll('.channelsCheckbox input:checked').length > 0
			setChannelsTarget(h)
		}
	}

	const dateChange = (e: React.ChangeEvent<HTMLInputElement>) =>
		setDate(e.target.value)
	const timeChange = (e: React.ChangeEvent<HTMLInputElement>) =>
		setTime(e.target.value)
	const onDragOver = (e: any) => e.preventDefault()

	return (
		<div className="AddPostForm">
			<ImageTable deleteImage={deleteMedia} files={files} />
			<label
				className="fileInputLabel"
				htmlFor="upload-postImage"
				onDragEnter={onDragEnter}
				onDrop={onDrop}
				onDragOver={onDragOver}
			>
				<ImageIcon />
				<h4>Добавить</h4>
			</label>
			<h2>Текст поста</h2>
			<p>Выделите текст и нажмите на кнопку стиля или ссылки.</p>
			<input
				type="file"
				maxLength={maxLength}
				name="upload-postImage"
				id="upload-postImage"
				style={{ display: 'none' }}
				onChange={changeInput}
				multiple
				hidden
				accept="image/jpeg,image/png"
			/>
			<div className="AddPostForm-buttonGroup">
				<button onClick={onBoldClick}>
					<FormatBoldIcon />
				</button>
				<button onClick={onItalicClick}>
					<FormatItalicIcon />
				</button>
				<button onClick={onUnderLineClick}>
					<FormatUnderlinedIcon />
				</button>
				<button onClick={onStrikeClick}>
					<FormatStrikethroughIcon />
				</button>
				<button onClick={handlerAddLink}>
					<LinkIcon />
				</button>
			</div>
			<div className="AddPost_input">
				<Editor
					editorState={editorState}
					handleKeyCommand={handleKeyCommand}
					onChange={setEditorState}
				/>
			</div>
			<Grid container spacing="10px" sx={{ mt: '10px' }}>
				<Grid item xl={6} lg={6} md={6} sm={6} xs={12}>
					<TextField
						fullWidth
						size="small"
						type="date"
						value={date}
						onChange={dateChange}
						placeholder="Дата публикации"
					/>
				</Grid>
				<Grid item xl={6} lg={6} md={6} sm={6} xs={12}>
					<TextField
						fullWidth
						size="small"
						value={time}
						onChange={timeChange}
						placeholder="Время публикации"
						type="time"
					/>
				</Grid>
			</Grid>
			<div className="AddPostForm-btnsbox">
				<Button
					variant="contained"
					onClick={spellchecking}
					disabled={spellcheckingBtnDisabled}
				>
					Проверить орфографию
				</Button>
				<button
					disabled={spellcheckingBtnDisabled}
					className="gptButton"
					onClick={gpt}
				>
					Сгенерировать текст
				</button>
				<Button
					variant="contained"
					disabled={spellcheckingBtnDisabled}
					onClick={() => {
						const cont = editorState.getCurrentContent()
						const data = {
							htmlText: stateToHTML(cont),
							images: files,
							plainText: cont.getPlainText()
						}
						setModal(data)
					}}
				>
					Показать превью
				</Button>
			</div>
			{isGptLoading !== null &&
				(!isGptLoading ? (
					<div className="AddPostForm-gpt-box">
						<h3>Текст от нейросети:</h3>
						<div
							className="AddPostForm-gpt"
							dangerouslySetInnerHTML={{ __html: GPTText }}
						></div>
					</div>
				) : (
					<CircularProgress
						sx={{ margin: 'auto', mt: '20px', display: 'block' }}
					/>
				))}
			{spellcheckingString.length ? (
				<div className="AddPostForm-spellchecking-box">
					{isSpellcheckingLoading ? (
						<CircularProgress sx={{ margin: 'auto', display: 'block' }} />
					) : (
						<>
							<h3>Отредактированный текст:</h3>
							<div
								className="AddPostForm-spellchecking"
								dangerouslySetInnerHTML={{ __html: spellcheckingString }}
							></div>
						</>
					)}
				</div>
			) : (
				''
			)}
			<Button
				variant="contained"
				disabled={mainBtn}
				className="main-btn"
				onClick={getText}
			>
				Отправить
			</Button>
			<div className="chanelsToPost" id="chanelsToPost">
				<h2>Отметьте каналы в которые нужно послать пост</h2>
				{!isLoading ? (
					channels?.length > 0 ? (
						channels?.map((channel: ChannelItem) => {
							return (
								<div className="chanelsToPost-item" key={channel.id}>
									<Checkbox
										data-id={channel.id}
										className="channelsCheckbox"
										onChange={toggleChannels}
									/>
									<Avatar src={channel.url}>{channel.name}</Avatar>
									<h3>{channel.name}</h3>
								</div>
							)
						})
					) : (
						<h3 className="noHaveChannels">У вас нет каналов добавьте их</h3>
					)
				) : (
					<CircularProgress className="loader" />
				)}
			</div>
		</div>
	)
}

export default AddPostForm
