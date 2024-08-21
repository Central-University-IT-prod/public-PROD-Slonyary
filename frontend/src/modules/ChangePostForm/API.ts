import axios from "axios";
import { BACKEND_HOST } from "../../constants";

export const changeMessage = async (id:number, data:any) => {
    try {
        const response = await axios.patch(`${BACKEND_HOST}/posts/${id}`, data, {
            headers: {
                'token': localStorage.getItem('accessToken')
            }
        })
        return response.data;
    } catch (error) {
        console.log(error)
        return error;
    }
}