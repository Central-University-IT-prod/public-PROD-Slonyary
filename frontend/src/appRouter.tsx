import { createBrowserRouter } from 'react-router-dom'
import { changePostPath, channelInfoPath, paths } from './routes'
import App from './App'
import PostPage from './pages/PostPage/PostPage.tsx'
import { TelegramAuth } from './pages/TelegramAuth/TelegramAuth.tsx'
import { ChannelPage } from './pages/ChannelPage/ChannelPage.tsx'
import AddPostPage from './pages/AddPostPage/AddPostPage.tsx'
import ChannelInfoPage from './pages/ChannelInfoPage/ChannelInfoPage.tsx'
import ChangePostPage from './pages/ChangePostPage/ChangePostPage.tsx'

export const router = createBrowserRouter([
	{
		element: <App />,
		path: '/',
		children: [
			{
				path: paths.TELEGRAMAUTH,
				element: <TelegramAuth />
			},
			{
				path: paths.ADD_POST,
				element: <AddPostPage />
			},
			{
				path: changePostPath(),
				element: <ChangePostPage />
			},
			{
				path: paths.CHANNELS,
				element: <ChannelPage />
			},
			{
				path: channelInfoPath(),
				element: <ChannelInfoPage />
			},
			{
				path: paths.HOME,
				element: <PostPage />
			}
		]
	}
])
