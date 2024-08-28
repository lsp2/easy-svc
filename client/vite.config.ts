import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path';
// https://vitejs.dev/config/
export default defineConfig({
  base: "/static",
  // base: "./",
  plugins: [vue()],
  resolve: {
    // 设置文件./src路径为 @
    alias: [
      {
        find: '@',
        replacement: resolve(__dirname, './src')
      }
    ]
  },
  css:{
    preprocessorOptions:{
      less: {
        import: resolve("@/styles/base.less"),
        modifyVars: {
          hack: 'true; @import "@/styles/variable.less"'
        },
        javascriptEnabled: true
      }
    }
  },
  server: {
    host: '127.0.0.1', 
    port: 5000,
    open: true, //启动后是否自动打开浏览器,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8888', // 设置代理目标    
        changeOrigin: true, // 是否改变请求源地址
        rewrite: (path) => path.replace(/^\/api/, '') // 将 /api 替换为空字符串
      }
    }
  },
  build:{
    minify: 'terser', // 必须启用：terserOptions配置才会有效
    terserOptions: {
      compress: {
        // 生产环境时移除console.log调试代码
        drop_console:true,
        drop_debugger: true,
      }
    },
    target: "esnext"
  }
})
