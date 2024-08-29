
import { Response } from "./http";

export interface UploadAudio {
  name: string,
  url: string,
}

export interface ProcessAudio extends UploadAudio{
  spk: string,
  createTime: Date
}

export interface UploadRes extends Response { 
  file: UploadAudio
}

export interface GetUploadRes extends Response {
  file: UploadAudio,
}

export interface GetProcessRes extends Response {
  file: ProcessAudio,
}

export interface DeleteRes extends Response {}


export interface ProgressRes extends Response {
  value: number
}
