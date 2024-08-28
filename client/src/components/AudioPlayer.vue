<script setup lang='ts'>
  import { ref, watch } from "vue";
  import { formatTime } from "@/utils/format";
  
  const props = defineProps(['src']);
  const isPlaying = ref(false);
  const duration = ref(0);
  const percent = ref(0);
  const audioRef = ref<HTMLAudioElement | null>(null);

  let updateInterval = null;

  watch(
    () => props.src,
    (newSrc) => {
      audioRef.value.src = newSrc;
      audioRef.value.load();
    }
  );

  const getDuration = () => {
    duration.value = audioRef.value.duration;
  }

  const onDrag = (value: number) => {
    if (audioRef.value) {
      const cur = value / 100 * duration.value;
      audioRef.value.currentTime = cur;
    }  
  }  

  const clickPlay = ()=> {
    isPlaying.value = true;
    audioRef.value.play();
  }

  const clickPause = () => {
    isPlaying.value = false;
    audioRef.value.pause();
  }

  const onPlay = () => {

    if(!updateInterval){
      updateInterval = window.setInterval(() => {
        percent.value = audioRef.value.currentTime / duration.value * 100;
      }, 1000)
    }
  }

  const onPause = () => {
    percent.value = audioRef.value.currentTime / duration.value * 100;
    if (updateInterval) {
      window.clearInterval(updateInterval);
      updateInterval = null;
    }
  }

  const onEnded = () => {
    isPlaying.value = false;
    audioRef.value.currentTime = 0;
    percent.value = 0;
    audioRef.value.pause();
  }

  const forward = (val: number) => {
    let newTime = audioRef.value.currentTime + val;
    newTime = newTime > duration.value ? duration.value : newTime;
    audioRef.value.currentTime = newTime;
    percent.value = newTime / duration.value * 100;
  }

  const backward = (val: number) => {
    let newTime = audioRef.value.currentTime - val;
    newTime = newTime < 0 ? 0 : newTime;
    audioRef.value.currentTime = newTime;
    percent.value = newTime / duration.value * 100;
  }

</script>

<template>
  <div class="container">
    <audio ref="audioRef" :src="src" 
    @canplay="getDuration"
    @play="onPlay"
    @pause="onPause"
    @ended="onEnded"
    ></audio>
    <a-slider :default-value="0" v-model="percent" @change="onDrag" :show-tooltip="false"/>
    <div class="time">
      <div v-if="audioRef">{{ formatTime(audioRef.currentTime) }}</div>
      <div>{{ formatTime(duration) }}</div>
    </div>
    <div class="command">
      <div class="small inter" @click="backward(5)">
        <icon-double-left style="stroke-width: 5;"/>
      </div>
      <div class="large inter">
        <icon-play-arrow-fill style="stroke-width: 5;" v-show="!isPlaying" @click="clickPlay"/>
        <icon-pause style="stroke-width: 5;" v-show="isPlaying" @click="clickPause"/>
      </div>
      <div class="small inter" @click="forward(5)">
        <icon-double-right style="stroke-width: 5;" />
      </div>
    </div>
  </div>
</template>

<style scoped lang='less'>
  .container{
    padding: 2rem;

    ::v-deep(.arco-slider-track){
      height: 1rem;
    }

    ::v-deep(.arco-slider-track::before){
      display: flex;
      height:0.5rem;
      width: 100%;
      background: #ddd;
      border-radius: 0.25rem;
      position: relative;
      margin-bottom: 1.5vh;
    }

    ::v-deep(.arco-slider-bar){
      height: 0.5rem;
      background: @theme-blue;
      border-radius: 0.25rem;
    }

    ::v-deep(.arco-slider-btn){
      background: #fff;
      width: 1rem;
      height: 1rem;
      border-radius: 0.5rem;
      box-shadow: 0 0 0.2rem @theme-black;
    }

    ::v-deep(.arco-slider-btn::after){
      border: none;
    }

    .time{
      width: 100%;
      display: flex;
      justify-content: space-between;
      margin-bottom: 2vh;
      color: #888;
      font-size: 0.7rem;
    }

    .command{
      width: 100%;
      display: flex;
      justify-content: space-around;
      align-items: center;
      margin-bottom: 5vh;

      .small{
        width: 3rem;
        height: 3rem;
        font-size: 1.5rem;
      }

      .large{
        width: 4rem;
        height: 4rem;
        font-size: 2rem;
      }

      .inter{
        box-shadow: 0.1rem 0.1rem 0.5rem #ccc;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
      }

      .inter:active{
        box-shadow: 0 0 0 #ccc;
      }
    }
  }
</style>
