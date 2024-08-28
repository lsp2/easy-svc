import request from "./requst.ts"
import { AllVocalRes } from "@/types/vocal.ts";

export function getAllVocal(): Promise<AllVocalRes>{
  return request.get('/vocal/all');
}