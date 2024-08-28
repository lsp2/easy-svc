import { defineStore } from "pinia";
import { clearToken, setToken, getToken } from '@/utils/auth';
import { login as userLogin, register as userRegister, getUserInfo} from "@/api/user";
import { UserReq, UserInfo } from "@/types/user";
import { Message } from "@arco-design/web-vue";
import router from "@/router";


const useUserStore = defineStore('user', {
  state: (): UserInfo => ({
    userId: '',
  }),
  getters: {
    isLogin: (state): boolean => state.userId ? true: false
  },
  actions: { 

    setInfo(data: UserInfo) {
      this.userId = data.userId
    },

    // Reset user's information
    resetInfo() {
      this.reset();
    },

    async info() {
      const token = getToken()
      if(!token){
        this.logout();
        return;
      }
      const res = await getUserInfo();   
      this.setInfo(res.user);
    },

    async login(data: UserReq){
      try {
        const res = await userLogin(data);
        if(res.flag === 1){
          setToken(res.token);
          this.info();
          Message.success("登录成功");
          setTimeout(()=>{
            router.push("/");
          }, 500)
        }
        else if(res.flag === -1){
          Message.error("密码错误");
        }
        else{
          Message.error("服务器异常错误");
        }
      } catch (err) {
        clearToken();
        throw err;
      }
    },

    async logout(){

    },

    async register(data: UserReq){
      try {
        console.log(data);
        // new FormData({ "userId": data.userId, "password": data.password });
        const res = await userRegister(data);
        console.log(res);
        
        if(res.flag === 1){
          this.login(data);
          Message.success("注册成功");
        }
        else if(res.flag === -1){
          Message.warning("注册失败，请更换用户名重试");
        }
      } catch (err) {
        throw err;
      }
    }
 
  },

  persist: true

})

export default useUserStore;