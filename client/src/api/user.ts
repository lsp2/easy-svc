import request from "./requst.ts";
import { UserReq, InfoRes, RegisterRes, LoginRes } from "@/types/user.ts";

export function login(data: UserReq): Promise<LoginRes> {
  return request.post('/user/login', data);
}

export function register(data: UserReq): Promise<RegisterRes> {
  return request.post('/user/register', data);
}

export function getUserInfo(): Promise<InfoRes> {
  return request.get(`/user/info`);
}
