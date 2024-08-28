import request from "./requst.ts"
import { UploadRes, DeleteRes, GetUploadRes, ProgressRes, GetProcessRes, DownloadRes } from "@/types/audio.ts";

export function startUpload(data: FormData, cb: Function): Promise<UploadRes>{
  return request.post('/upload/start', data, {
    headers: {
      'content-type': 'multipart/form-data'
    },
    onUploadProgress: cb as any
  });
}

export function deleteUploadAudio(fileName: string): Promise<DeleteRes>{
  return request.delete(`/upload/audio?name=${fileName}`);
}

export function getUploadAudio(): Promise<GetUploadRes>{
  return request.get('/upload/audio');
}

export function startProcess(spk: string, fileName: string): Promise<GetProcessRes>{
  return request.get(`/process/start?spk=${spk}&name=${fileName}`);
}

export function deleteProcessAudio(fileName: string): Promise<DeleteRes>{
  return request.delete(`/process/audio?name=${fileName}`);
}

export function getProcessAudio(): Promise<GetProcessRes>{
  return request.get('/process/audio');
}

export function getProgressValue(): Promise<ProgressRes>{
  return request.get(`/process/progress`);
}

export function downloadAudio(fileName: string): Promise<DownloadRes>{
  return request.get(`/process/audio/download/${fileName}`, {
    responseType: 'blob'
  });
}