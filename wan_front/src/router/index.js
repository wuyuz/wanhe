import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '../components/user/Login.vue'
import Home from '../components/Home.vue'
import Welcome from '../components/Welcome.vue'
import Medicine from '../components/functions/medicine.vue'
import Plans from '../components/functions/plans.vue'

Vue.use(VueRouter)

const routes = [
  { path: '/login', component: Login, meta: { title: '登录' } },
  {
    path: '/home', component: Home, redirect: '/welcome', meta: { title: '主页' }, children: [
      { path: '/welcome', component: Welcome, meta: { title: '欢迎界面' } },
      { path: '/medicine', component: Medicine, meta: { title: '药品信息' } },
      { path: '/plans', component: Plans, meta: { title: '方案信息' } },
    ]
  }
]

const router = new VueRouter({
  routes
})

// 路由导航守卫，所有请求的拦截者
router.beforeEach((to, from, next) => {
  if (to.meta.title) {
    document.title = to.meta.title
  }

  // 拦截没有token的用户
  if (to.path == '/login') return next()
  const tokenStr = window.sessionStorage.getItem('token')
  if (!tokenStr) return next('/login')
  next()

  if (to.path == '/welcome') {
    window.sessionStorage.setItem("saveActive", '/home')
    next('/home')
  }
})


export default router
