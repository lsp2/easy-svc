<script setup lang='ts'>
  import { ref } from "vue";
  import "@/styles/input.less";
  import "@/utils/regex";
  import { checkUserId, checkPassword } from "@/utils/regex";
  import { Message } from '@arco-design/web-vue';
  import useUserStore from "@/store/user";

  const userStore = useUserStore();

  const mode = ref(true);
  const clickLogin = ()=>{
    if(!mode.value){
      switchMode(true);
      return;
    }

    const userId = (document.getElementById("login-uId") as HTMLInputElement).value;
    const password =(document.getElementById("login-pw") as HTMLInputElement).value;
    if(!userId){
      Message.warning("未输入账号");
      return;
    }
    if(!password){
      Message.warning("未输入密码");
      return;
    }
    if(!checkUserId(userId)){
      Message.warning("账号格式不对");
      return;
    }
    if(!checkPassword(password)){
      Message.warning("密码格式不对");
      return;
    }
    userStore.login({ userId, password });
  }
  const clickRegister = ()=>{
    if(mode.value){
      switchMode(false);
      return;
    }

    const userId = (document.getElementById("reg-uId") as HTMLInputElement).value;
    const password =(document.getElementById("reg-pw") as HTMLInputElement).value;
    const password2 =(document.getElementById("reg-pw2") as HTMLInputElement).value;
    if(!userId){
      Message.warning("未输入账号");
      return;
    }
    if(!password){
      Message.warning("未输入密码");
      return;
    }
    if(!password2){
      Message.warning("未确认密码");
      return;
    }
    if(!checkUserId(userId)){
      Message.warning("账号格式不对");
      return;
    }
    if(!checkPassword(password)){
      Message.warning("密码格式不对");
      return;
    }
    if(!(password===password2)){
      Message.warning("两次密码不一致");
      return;
    }

    
    userStore.register({ userId, password });

  }
  const switchMode = (value: boolean)=>{
    mode.value = value;
  }
</script>

<template>
  <div class="container">
    <div class="content">
      <form action="#" class="row" v-if="mode">
        <h3 class="mb-3">登录</h3>
        <input class="input-text mb-1" type="text" placeholder="账号" id="login-uId" >
        <input class="input-text mb-1" type="password" placeholder="密码" id="login-pw" >
      </form>
      <form action="#" id="reister" class="row" v-else>
        <h3 class="mb-3">注册</h3>
        <input class="input-text mb-1" type="text" placeholder="设置账号（2-12位字母或数字的组合）" id="reg-uId">
        <input class="input-text mb-1" type="password" placeholder="设置密码（6-18位字母或数字的组合）" id="reg-pw">
        <input class="input-text mb-1" type="password" placeholder="确认密码" id="reg-pw2">
      </form>
      <a-row class="row mt-1">
        <a-col :span="11" :offset="0">
          <button class="btn normal long" :class="!mode?'normal':'hollow'" @click="clickRegister">注册</button>
        </a-col>
        <a-col :span="11" :offset="2">
          <button class="btn normal long" :class="mode?'normal':'hollow'" @click="clickLogin">登录</button>
        </a-col>
      </a-row>
    </div>
  </div>
</template>

<style scoped lang='less'>
  .container{

    input{
      border-radius: 0;
      border: transparent;
      border-bottom: 0.2vh solid @theme-blue;
      position: relative;
    }
  }
</style>
