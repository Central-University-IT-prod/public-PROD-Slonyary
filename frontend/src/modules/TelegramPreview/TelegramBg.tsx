import {FC} from "react";
import bg from '../../assets/imgs/telegramBackground.png'

type Props = {
  className: string
}
export const TelegramBg: FC<Props> = (props) => (
  <img src={bg} className={props.className} alt=""/>
)

