import axios from 'axios';
import { getToken } from '@/utils/auth';
import type  { AxiosRequestConfig, AxiosResponse, AxiosError } from 'axios';

// 创建axios实例
const request = axios.create({
   baseURL: '/api', // 设置API的基础URL
  //  baseURL: '',
   timeout: 600000, 
});

// declare module 'axios' {
//   interface AxiosInstance {
//       (config: AxiosRequestConfig): Promise<any>
//   }
// }

export interface HttpResponse<T = any> {
  code: number,
  msg: string,
  data: T;
}

export interface HttpError {
  status: number
}

// 请求拦截器
request.interceptors.request.use(
   (config: AxiosRequestConfig):any => {
      // 可在请求发送前对config进行修改，如添加请求头等
      const token = getToken();
      if (token) {
        config.headers!.Authorization = `Bearer ${token}`;
      }
      return config;
   },
   (error: AxiosError) => {
      // 处理请求错误
      return Promise.reject(error);
   }
);

// 响应拦截器
request.interceptors.response.use(
  (response: AxiosResponse) => {
    const { data } = response;
    return data;
  },
  (error: HttpError) => {
    const { status } = error;
    if (status === 401) {
      // TODO: token 监听，自动刷新，重新登录
    }
    return Promise.reject(error);
  }
);


export default request;
