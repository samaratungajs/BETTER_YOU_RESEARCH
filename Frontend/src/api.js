import axios from "axios";

const RASA_BASE = "http://127.0.0.1:5005/webhooks/rest/webhook/"
const SENTI_BASE = "http://127.0.0.1:8000"
const ACTIVITY_BASE = "http://127.0.0.1:5500"


export async function sendToRasa (body){
    return axios({
        url:RASA_BASE,
        method: "POST",
        data: body
    })
}

export async function predict (body){
    return axios({
        url:`${SENTI_BASE}/test`,
        method: "POST",
        data: body
    })
}

export async function getChats (id){
    return axios({
        url:`${SENTI_BASE}/chats/${id}`,
        method:"GET"
    })
}

export async function audioPredict (body){
    return fetch({
        url:AUDIO_BASE,
        method: "POST",
        data: body
    })
}

export async function friendSuggest (body){
    return axios({
        url:`${ACTIVITY_BASE}/friend_suggestion`,
        method: "POST",
        data: body
    })
}

