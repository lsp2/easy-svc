<script setup lang='ts'>
  import { Swiper, SwiperSlide } from 'swiper/vue';
  import { ref } from 'vue';
  import Head from "@/components/Head.vue";
  import BackButton from '@/components/BackButton.vue';
  import router from '@/router';

  import { getAllVocal } from "@/api/vocal";
  import { getCover } from "@/api/resource";

  import 'swiper/less';

  let vocalList = ref([]);

  const spkId = ref('');

  const onSlideChange = (e: {activeIndex: Number}) => {
    spkId.value = vocalList.value[e.activeIndex+""].id;
  };

  const onSelectVocal = () => {
    router.push({ name:'Process', query:{ 'spk': spkId.value } });
  }

  const fetchVocalData = async ()=>{
    
    const res = await getAllVocal();
    if(res.flag){
      vocalList.value = res.vocals   
      spkId.value = vocalList.value[0].id;
    }
  }
  fetchVocalData();
</script>

<template>
  <div class="container">

    <Head>
      <template #left><BackButton></BackButton></template>
      <template #middle><span class="title">音色库</span></template>
    </Head>

    <div class="content">
      <swiper
        class="vocals"
        :slides-per-view="1"
        :space-between="0"
        @slideChange="onSlideChange"
        v-if="vocalList.length>0"
      >
        <swiper-slide v-for="item in vocalList" :key="item.id">
          <div class="item flex-center">
            <div class="img-outer flex-center">
              <img :src='getCover(item.imgUrl)' alt="">
            </div>
            <div class="spk-name">{{item.name}}</div>
          </div>

        </swiper-slide>
      </swiper>
      <div class="command flex-center">
        <button class="btn normal" @click="onSelectVocal">选择音色</button>
      </div>
    </div>
  </div>  
</template>

<style scoped lang='less'>


  .vocals{
    width: 100vw;
    flex: 1;

    .item{
      width: 90%;
      flex-direction: column;
      height: 100%;

      .img-outer{
        height: 100vw;
        img{
          width: 75vw;
          height: 75vw;
          border-radius: 50%;
          border: 2vw solid @theme-gray;
          box-shadow: 0 0 10px #bbb;
          box-sizing: border-box;
        }
      }
    }
    .spk-name{
      font-weight: bold;
      font-size: 1.2rem;
    }
  }
  .command{
    height: 25vh;
    min-height: 8rem;
  }
</style>
