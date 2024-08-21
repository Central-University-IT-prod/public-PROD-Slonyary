export type TPostItem = {
  channelsAvatar?: string[],
  channelName: string,
  date: string,
  admin: string,
  postImages: string[],
  category: 'pending' | 'moderation' | 'published',
  ownerName: string,
  htmlText: string,
}
