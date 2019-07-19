import Vue from 'vue';
import Router from 'vue-router';
import Workbench from './views/Workbench.vue';
import About from './views/About.vue';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'workbench',
      component: Workbench,
    },
    {
      path: '/about',
      name: 'about',
      component: About,
    },
  ],
});
