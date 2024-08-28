import { createApp } from 'vue';
import { createPinia } from 'pinia';
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import ArcoVue from '@arco-design/web-vue';
import ArcoVueIcon from '@arco-design/web-vue/es/icon';
import '@arco-design/web-vue/dist/arco.css';

import App from '@/App.vue';
import Router from "@/router";

import '@/styles/base.less';
import '@/styles/button.less';
import '@/styles/display.less';

import { register } from 'swiper/element/bundle';
register();

const app = createApp(App);
app.use(ArcoVue);
app.use(ArcoVueIcon);
app.use(Router);
app.use(createPinia().use(piniaPluginPersistedstate));
app.mount('#app');
