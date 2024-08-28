import { Response } from "./http.ts";

export interface Vocal {
  id: string,
  name: string,
  imgUrl: string 
}

export interface AllVocalRes extends Response {
  vocals: Array<Vocal>
}
