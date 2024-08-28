<script setup lang='ts'>
  import { watch, ref } from "vue";
  
  const props = defineProps(["percent", "height", "label"]);
  const bar = ref(null);

  watch(
    ()=>props.percent, 
    (newValue: number)=>{
      bar.value.style = `width: ${newValue > 100? 100: newValue}%`;
  })
  
  
</script>

<template>
  <div class="label">{{ label }}进度: <span>{{ percent }}%</span></div>
  <div class="bar-box" :style="`height:${height}`">
    <div class="bar" ref="bar"></div>
  </div>
</template>

<style scoped lang='less'>

  .label{
    font-size: 2vh;
    margin-bottom: 1vh;
  }
  .bar-box{
    width: 100%;
    background-color: @theme-gray;
    position: relative;
    overflow: hidden;
    
    .bar{
      position: absolute;
      background-color: @theme-blue;
      height: 100%;
    }
  }
</style>
