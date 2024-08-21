import React, {memo, ReactNode, useEffect, useMemo} from 'react'
import {useMediaContext} from '../../modules/MediaProvider/MediaProvider'

interface IProps {
  children: ReactNode
  src: string
  index: number
}

type TContext = {
  media: { index: number; src: string }[]
  addMedia: (fileObject: { index: number; src: string }) => void
  openSlider: (index: number) => void
}

const MediaView = memo(({children, src, index}: IProps) => {
  const {media, addMedia, openSlider} = useMediaContext() as TContext

  const onClick = () => {
    console.log('dsd')
    openSlider(index)
  }
  useEffect(() => {
    if (media[index]?.src !== src) {
      addMedia({
        index,
        src
      })
    }
  }, [src])

  const childNode = useMemo(
    () =>
      React.Children.map(children, (child) => {
        if (React.isValidElement(child)) {
          return React.cloneElement(child, {onClick} as any)
        }
      }),
    [openSlider]
  )
  return <>{childNode}</>
})

export default MediaView
