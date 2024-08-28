

export const setStorage = (key: string, obj: any)=>{
  localStorage.setItem(key, JSON.stringify(obj));
}

export const getStorage = (key: string)=>{
  let target = localStorage.getItem(key);
  if(target){
    return JSON.parse(target);
  }
  return null;
}

export const removeStorage = (key: string)=>{
  localStorage.removeItem(key);
}