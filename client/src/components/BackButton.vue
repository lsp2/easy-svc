<script setup lang='ts'>
  const onBack = ()=>{
    history.back();
  }
</script>

<template>
  <button class="btn transparent"  @click="onBack">
    <icon-left style="stroke-width: 6;"/>
  </button>
</template>

<style scoped lang='less'>
  button{
    font-size: 1.1rem;
  }
</style>
