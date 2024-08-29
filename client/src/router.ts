import { createRouter, createWebHistory }  from 'vue-router'
import { getToken } from '@/utils/auth';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'Index'
    },
    {
      path: '/vocals',
      name: 'VocalList',
      component: ()=> import('@/pages/VocalList/Index.vue')
    },
    {
      path: '/vocals/process',
      name: 'Process',
      component: ()=> import('@/pages/Process/Index.vue')
    },
    {
      path: '/login',
      name: 'Login',
      component: ()=> import('@/pages/Login/Index.vue')
    }
  ]
})

router.beforeEach((to, _from, next) => {
  // to 即将进入的路由
  // from 在哪个路由进入的
  // next 放行
  let token = getToken(); //在本地存储中获取token
  if (token) {
    //判断是否有token
    next();
  } else {
    //在没有token的前提下，to下面的path是否为/login，如果不是则页面跳转到登录页面
    if (to.path == "/login") {
      next();
    } else {
      next({ path: "/login" }); //跳转页面到login页
    }
  }
})

export default router