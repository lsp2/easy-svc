<script setup lang='ts'>
  import Router from "@/router"

  const onOption = (name: string)=>{
    // const id = (e.currentTarget as HTMLInputElement).dataset.id
      Router.push({name});
  }

</script>

<template>

  <div class="container">
    <div class="banner">
      <div class="img-box">
        <img src="@/assets/img/vite.svg" alt="">
      </div>
      <h3>Voice Changer</h3>
    </div>
    <div class="entry">
      <button class="btn normal" @click="onOption('VocalList')">启动！</button>
      <!-- <button class="btn normal" @click="onOption('Record')">转换记录</button> -->
    </div>
  </div>
</template>

<style lang="less" scoped>
.container{
  background-color: @theme-black;
  justify-content: center;

  .banner{
    width: 40vw;
    max-width: 20vh;

    .img-box{
      width: 100%;
    }
    h3{
      color:@theme-white;
    }
  }

  .entry{
    max-width: 20vh;
    margin-top: 3vh;
    height: 10vh;
    width: 50vw;
    display: flex;
    flex-direction: column;
    justify-content: space-between;

    button{
      margin-bottom: 1rem;
    }
  }

}

</style>
