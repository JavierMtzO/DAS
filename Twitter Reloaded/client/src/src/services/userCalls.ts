import axios from "axios";
import generateError from "./generateError";
import { getToken } from "./tokenUtilities";
// const BASE_URL = process.env.REACT_APP_SERVER_URL + '/user';
const BASE_URL = "http://127.0.0.1:3001";

export async function login (email: string, password: string) {
    try {
        const { data } : { data : any } = await axios.post(BASE_URL + '/login', {email, password});
        // sessionStorage.setItem('token', data.token);
        sessionStorage.setItem('userId', data.user_id);
        sessionStorage.setItem('userName', data.username);
        return Promise.resolve(data.success);
    } catch (error : any) {
        return Promise.reject(generateError(error));
    }
}
// userId: string, username: string, 
export async function postTweet(content: string){
    try{
        let userId = sessionStorage.getItem('userId');
        let username = sessionStorage.getItem('userName');
        const { data } : { data : any } = await axios.post(BASE_URL + '/tweets', {userId, username, content});
        return Promise.resolve(data.success);
    } catch (error : any) {
        return Promise.reject(generateError(error));
    }
}

export async function signup (
    username : string, 
    email : string, 
    password: string, 
    confirmPassword : string, 
    name : string) {
        const signupData = {
            username, 
            email, 
            password, 
            confirmPassword, 
            name
        };
        try {
            const { data } : { data : any } = await axios.post(BASE_URL + '/users', signupData);
            // sessionStorage.setItem('token', data.token);
            sessionStorage.setItem('userId', data.user_id);
            sessionStorage.setItem('userName', data.username);
            return Promise.resolve(data.success);
        } catch (error : any) {
            return Promise.reject(generateError(error));
        }
}

export async function updateUser (updatedUserReq: any) {
    try {
        const { updatedUser } : { updatedUser : User } = await axios.put(BASE_URL, {updatedUser: updatedUserReq}, {
            headers: {
                Authorization: `Bearer ${getToken()}`
            }
        });
        return Promise.resolve(updatedUser); 
    } catch (error : any) {
        return Promise.reject(generateError(error));
    }
}

export async function getLoggedInUser() {
    try {
        const {data} = await axios.get(BASE_URL + '/get_logged_in_user/', {
            headers: {
                Authorization: `Bearer ${getToken()}`
            }
        });
        return Promise.resolve(data);
    } catch (error) {
        return Promise.reject(generateError(error));
    }
}