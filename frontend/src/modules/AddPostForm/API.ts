import axios from "axios";
import { BACKEND_HOST } from "../../constants";

export const getSpellcheckingWords = async (html:string) => {
    try {
        const res = await axios.get(`https://speller.yandex.net/services/spellservice.json/checkText`, {params:{text: html, format: 'html'}});
        return res?.data
    } catch (error) {
        return null;
    }
}

export const addMessages = async (data:any) => {
    try {
        const response = await axios.post(`${BACKEND_HOST}/posts`, data, {
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

export const addImageToPost = async (id: number, form: FormData) => {
    try {
        const response = await axios.post(`${BACKEND_HOST}/posts/${id}/images`, form, {
            headers: {
                'token': localStorage.getItem('accessToken')
            }
        })
        return response;
    } catch (error) {
        console.log(error)
        return error;
    }
}