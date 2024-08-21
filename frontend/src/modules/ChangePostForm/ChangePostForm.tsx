// @ts-ignore

import React, { ChangeEvent, FC, useCallback, useMemo, useState } from 'react'
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
import { Button, CircularProgress, Grid, TextField } from '@mui/material'
import FormatBoldIcon from '@mui/icons-material/FormatBold'
import FormatItalicIcon from '@mui/icons-material/FormatItalic'
import FormatUnderlinedIcon from '@mui/icons-material/FormatUnderlined'
import FormatStrikethroughIcon from '@mui/icons-material/FormatStrikethrough'
import LinkIcon from '@mui/icons-material/Link'
import './ChangePostForm.scss'
import { getSpellcheckingWords } from '../AddPostForm/API'
import { changeMessage } from './API'
import { useParams } from 'react-router'

const ChangePostForm: FC = () => {
	const [date, setDate] = useState('')
	const [time, setTime] = useState('00:00')

	const { id } = useParams()

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

	enum InlineStyle {
		BOLD = 'BOLD',
		ITALIC = 'ITALIC',
		UNDERLINE = 'UNDERLINE',
		STRIKE = 'STRIKETHROUGH'
	}

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
		if (!Number(id)) return
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
		const contentState = editorState.getCurrentContent()
		let html = stateToHTML(contentState, options)
			.replace(/<br>/g, '\n')
			.replace(/<p>/g, '')
			.replace(/<\/p>/g, '')
		const text = contentState.getPlainText()

		let publish_time: string = ''

		if (date) {
			const [year, month, day] = date.split('-')
			const [hours, minut] = time.split(':')

			publish_time = new Date(+year, +month - 1, +day, +hours, +minut)
				.toISOString()
				.replace('Z', '')
		}

		const data = {
			plain_text: text,
			html_text: html,
			publish_time: publish_time ? publish_time : null
		}
		await changeMessage(Number(id), data)
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

	const [spellcheckingString, setSpellcheckingString] = useState<string>('')
	const [isSpellcheckingLoading, setIsSpellcheckingLoading] =
		useState<boolean>(false)

	const spellchecking = async () => {
		setIsSpellcheckingLoading(true)

		const contentState = editorState.getCurrentContent()
		const html = stateToHTML(contentState)
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

	const mainBtn = useMemo(
		() => editorState.getCurrentContent().getPlainText().trim().length > 0,
		[editorState]
	)

	const dateChange = (e: ChangeEvent<HTMLInputElement>) =>
		setDate(e.target.value)
	const timeChange = (e: ChangeEvent<HTMLInputElement>) =>
		setTime(e.target.value)
	return (
		<div className="ChangePostForm">
			<h2>Изменение текста поста</h2>
			<p>Выделите текст и нажмите на кнопку стиля или ссылки.</p>
			<div className="ChangePostForm-buttonGroup">
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
			<div className="ChangePostForm-btnsbox">
				<Button variant="outlined" onClick={spellchecking} disabled={!mainBtn}>
					Проверить орфографию
				</Button>
				<Button
					variant="contained"
					disabled={!mainBtn}
					className="main-btn"
					onClick={getText}
				>
					Отправить
				</Button>
			</div>
			{spellcheckingString.length ? (
				<div className="ChangePostForm-spellchecking-box">
					{isSpellcheckingLoading ? (
						<CircularProgress sx={{ margin: 'auto', display: 'block' }} />
					) : (
						<>
							<h3>Отредактированный текст:</h3>
							<div
								className="ChangePostForm-spellchecking"
								dangerouslySetInnerHTML={{ __html: spellcheckingString }}
							></div>
						</>
					)}
				</div>
			) : (
				''
			)}
		</div>
	)
}

export default ChangePostForm
