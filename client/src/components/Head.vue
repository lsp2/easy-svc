<script setup lang='ts'>
 
</script>

<template>
  <div id="Head" class="flex-center fix">
    <div class="left flex-center">
      <slot name="left"></slot>
    </div>
    <div class="middle title">
      <slot name="middle"></slot>
    </div>
    <div class="right flex-center">
      <slot name="right"></slot>
    </div>
  </div>
</template>

<style scoped lang='less'>

  #Head{
    background-color: #fff;
    width: 100vw;
    height: @headHight;
    padding: 0 @padding-x;
    // box-shadow: 0 0 3px 3px #eee;

    .left, .right{
      width: @headHight;
      height: 100%;
    }
    .middle{
      flex: 1;
    }
  }

  .fix{
    position: fixed;
    top: 0;
    z-index: 999;
  }

  .flex-center{
    display: flex;
    align-items: center;
    justify-content: center;
  }
</style>
