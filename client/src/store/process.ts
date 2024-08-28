
import { UploadAudio, ProcessAudio } from '@/types/audio';
import { defineStore } from 'pinia';

const useProcessStore = defineStore('process', {
    state: () => ({
      stage: 0, // 1: 未上传 2: 上传中 3: 已上传 4: 处理中 5: 处理完成
      label: '',
      file: null
    }),
    getters: { 
      
    },
    actions: { 
      selectFile(){
        this.stage = 1; 
      },
      clearSelect(){
        this.stage = 0;
        this.file = null;
      },
      startUploading(){
        this.stage = 2; 
        this.label = '上传';
      },
      successUpload(file: UploadAudio){
        this.file = file;
        this.stage = 3;
      },
      startProcess(){
        this.stage = 4;
        this.label = '转换';
      },
      endProcess(file: ProcessAudio){
        this.stage = 5;
        this.file = file
      }
    },
    
    persist: true
})

export default useProcessStore;