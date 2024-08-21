// @ts-ignore
import {FC} from 'react'
import Channel from '../../modules/Channel/Channel.tsx'
import {Button, styled} from '@mui/material'
import s from './ChannelPage.module.scss'
import {channelsAPI} from '../../store/services/ChannelService.ts'
import {Loading} from '../../modules/Loading/Loading.tsx'

export const ChannelPage: FC = () => {
  const {data: channels, isLoading} = channelsAPI.useGetChannelsQuery(null)

  if (isLoading) return <Loading/>
  const BootstrapButton = styled(Button)({
    background: '#FFB13C',
    '&:hover': {
      background: '#c98c31'
    }
  })

  return (
    <section>
      <div className={s.buttons}>
        <a href="https://t.me/StackSMM_Bot?start=add_channel" target="_blank">
          <BootstrapButton sx={{borderRadius: '20px'}} variant="contained">
            Добавить канал
          </BootstrapButton>
        </a>
      </div>
      <div>
        {channels &&
          channels.map((channel: any) => (
            <Channel
              title={channel.name}
              subscribers={channel.subscribers}
              avatar={channel.photo_url}
              posts={{
                pending: channel.on_pending,
                moderation: channel.on_moderation
              }}
              id={channel.id}
            />
          ))}
      </div>
    </section>
  )
}
