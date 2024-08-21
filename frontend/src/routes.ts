enum paths {
  TELEGRAMAUTH = 'telegramauth',
  HOME = '',
  POSTS = 'posts',
  CHANNELS = "channels",
  ADD_POST = "addpost",
  CHANNEL_INFO = "channelinfo",
}

const changePostPath = (id = ':id') => `post/${id}/change`
const channelInfoPath = (id = ':id') => `channels/${id}/info`

const NavigatePath = (path: string): string => `/${path}`

export {paths, NavigatePath, channelInfoPath, changePostPath}