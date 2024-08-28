import { Response } from "./http.ts";

export interface UserInfo {
  userId: string
}

export interface UserReq extends UserInfo{
  password: string
}

export interface RegisterRes extends Response {
  userId: string,
  password: string,
}

export interface LoginRes extends Response {
  token: string
}

export interface InfoRes extends Response{
  user: UserInfo
}