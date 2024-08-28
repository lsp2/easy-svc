<script setup lang='ts'>
  import { ref, onBeforeUnmount } from "vue";
  import router from '@/router';
  import request from "@/api/requst";
  import '@/api/audio';

  import useProcessStore from "@/store/process";
  import useUserStore from "@/store/user";
  import { startUpload, getUploadAudio, deleteUploadAudio, startProcess, getProgressValue, getProcessAudio,deleteProcessAudio, downloadAudio } from "@/api/audio";
  import Head from "@/components/Head.vue";
  import BackButton from '@/components/BackButton.vue';
  import ProgressBar from "@/components/ProgressBar.vue";
  import AudioPlayer from "@/components/AudioPlayer.vue";
  import { Message } from "@arco-design/web-vue";

  const processStore = useProcessStore();
  const userStore = useUserStore();

  const file = ref(null);
  const progressPercent = ref(0);
  const audioSrc = ref('');

  const stateText = ["选择音频", "待上传", "上传中", "已上传", "处理中", "已处理"]

  const onSelectLocalFile = (e: Event)=>{
    file.value = (e.target as HTMLInputElement).files[0]; 
    processStore.selectFile();
  }

  const onUpload = async ()=>{
    try{
      let formData = new FormData();
      formData.set("audio_file", file.value);
      formData.set("id", userStore.userId)
      processStore.startUploading();
      const data = await startUpload(formData, function (progressEvent) {
          progressPercent.value = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          );
        }
      );
      if(data.flag === 1){
        processStore.successUpload(data.file);
      }
      else{
        Message.error("上传失败");
      }
    }
    catch{    
      processStore.selectFile();
    }
  }

  let query = null;

  const onStartProcess = async ()=>{
    processStore.startProcess();
    updateProgressBar();
    const res = await startProcess(router.currentRoute.value.query.spk as string, processStore.file.name);

    if(res.flag){
      if(query){
        clearInterval(query);
        query = null;
      }
      processStore.endProcess(res.file);
      audioSrc.value = `${request.defaults.baseURL}/src/${processStore.file.url}`;
    }
  }

  const clearSelect = ()=>{
    processStore.clearSelect();
    (document.getElementById("select") as HTMLInputElement).value='';
    file.value = null
  }

  const onDownloadFile = async()=>{
    const res = await downloadAudio(processStore.file.name);
    const blobUrl = window.URL.createObjectURL(new Blob([res.data]));
    const a = document.createElement('a');
    a.style.display = 'none';
    a.download = `${processStore.file.spk}-${processStore.file.name}`;
    a.href = blobUrl;
    a.click();
    a.remove();
    Message.success("下载完成了喵");
  }

  const removeUpload = async()=>{
    try{
      const { flag } = await deleteUploadAudio(processStore.file.name);
      
      if(flag){
        processStore.clearSelect();
      }
      else{
        Message.error("删除失败");
      }
    }
    catch{
      Message.error("删除失败");
    }
  }

  const removeProcess = async()=>{
    try{
      const { flag } = await deleteProcessAudio(processStore.file.name);
      if(flag){
        processStore.successUpload(processStore.file);
      }
      else{
        Message.error("删除失败");
      }
    }
    catch{
      Message.error("删除失败");
    }
  }

  const onRemoveFile = ()=>{
    if(processStore.stage === 3){
      removeUpload();
    }
    else if(processStore.stage === 5){
      removeProcess();
    }
    else if(processStore.stage === 1){
      clearSelect();
    }
  }

  const fetchData = async ()=>{ // 获取处理状态数据
    const processData = await getProcessAudio();

    if(processData.flag){//后台有处理记录
      processStore.endProcess(processData.file); //处理后状态
      audioSrc.value = `${request.defaults.baseURL}/src${processStore.file.url}`;
    }
    else{ 

      const uploadData = await getUploadAudio();

      if(uploadData.flag){//后台有上传记录
        const res = await getProgressValue();

        if(res.flag) { //后台有正在处理的进度
          if(res.value < 100){ //处理中
            processStore.startProcess();
            updateProgressBar();
          }
        }
        else{ //上传后初始状态（准备处理）
          processStore.successUpload(uploadData.file);
        }

      }
      else{//后台没有上传记录
        processStore.clearSelect();
      }  
    }
  }

  const updateProgressBar = ()=>{ // 进度条轮询更新
    if(!query){ 
      query = setInterval(async function(){
        const res = await getProgressValue();
        progressPercent.value = res.value;
      }, 1000); //每秒轮询
    }
  }

  onBeforeUnmount(()=>{
    if(query){
      clearInterval(query); // 清除进度条轮询
      query = null;
    }
  })

  fetchData();

</script>

<template>
  <div class="container">
    <Head>
      <template #left><BackButton></BackButton></template>
      <template #middle><span class="title">转换器-{{ router.currentRoute.value.query.spk }}</span></template>
      <template #right>
        <a-dropdown  position="br">
          <button class="btn transparent" v-show="processStore.stage===1 || processStore.stage===3 || processStore.stage===5">
            <icon-more-vertical />
          </button>
          <template #content>
            <a-doption @click="onRemoveFile" v-show="file || processStore.stage===3 || processStore.stage===5">
              <template #icon>
                <icon-delete style="stroke-width: 5;"/>
              </template>
              <template #default>删除</template>
            </a-doption>
            <a-doption @click="onDownloadFile" v-show="processStore.stage===5">
              <template #icon>
                <icon-download style="stroke-width: 5;"/>
              </template>
              <template #default>下载</template>
            </a-doption>
          </template>
        </a-dropdown>
      </template>
    </Head>
    <div class="content">
      <label class="file-preview flex-center" for="select">
        <div>
          <icon-folder-add v-if="processStore.stage===0" class="icon"/>
          <icon-file-audio v-else  class="icon"/>
          <div class="text mt-1 file-name" v-if="processStore.stage>=3 ">{{ processStore.file.name }}</div>
          <div class="text mt-1 file-name" v-if="file && processStore.stage<3">{{ file.name }}</div>
          <div class="text mt-1 stage">{{ stateText[processStore.stage] }}</div>
        </div>
      </label>
      <input id="select" type="file" accept=".wav, .mp3, .flac" @change="onSelectLocalFile" style="display: none;" :disabled="processStore.stage!==0"/>
    </div>
    <div class="foot-box flex-center">
      <button class="btn normal long mb-1" v-if="processStore.stage===1" @click="onUpload">上传</button>
      <ProgressBar class="progress" v-if="processStore.stage===2 || processStore.stage===4" height="0.3rem" :label="processStore.label" :percent="progressPercent"/>
      <button class="btn normal long mb-1" v-if="processStore.stage===3" @click="onStartProcess">开始转换</button>
      <h3 v-if="processStore.stage===5">{{ processStore.file.spk }}</h3>
      <AudioPlayer :src="audioSrc" v-if="processStore.stage===5"/>
    </div>
  </div>
</template>

<style scoped lang='less'>

  .file-preview{
    height:50vh;
    flex: 1;

    ::v-deep(.arco-progress){
      font-size: 2rem;
    }

    .icon{
      width: 100%;
      height: 5rem;
      color: @theme-blue;
    }

    .file-name{
      font-weight: bold;
      color: #666;
    }

    .stage{
      padding: 0.2rem;
      background-color: @theme-blue;
      border-radius: 0.2rem;
      color: @font-white;
    }
  }

  .foot-box{
    height: 25vh;
    width: 90vw;
    flex-direction: column;
  }
</style>
