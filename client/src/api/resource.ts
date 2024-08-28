import request from "./requst.ts";

export const getCover = (obj_name: string) => {
  if (!obj_name) {
    obj_name = "img/music.jpg";
  }
  return `${request.defaults.baseURL}/src/${obj_name}`;
};