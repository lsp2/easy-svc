
export const checkUserId = (str: string) => /^[a-zA-Z0-9]{2,12}$/.test(str); 

export const checkPassword = (str: string) => /^[a-zA-Z0-9]{6,18}$/.test(str); 