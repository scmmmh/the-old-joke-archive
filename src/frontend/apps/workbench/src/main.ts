import Vue from 'vue';
import App from './App.vue';
import makeStore from './store';
import { Config } from '@/interfaces';

Vue.config.productionTip = false;

const configElement = document.getElementById('config');
let config: Config = {
    baseURL: '',
    sourceId: null,
    userId: null,
    annotations: [],
    metadata: [],
};
if (configElement) {
    config = JSON.parse(configElement.innerHTML);
}
const store = makeStore(config);

new Vue({
    store,
    render: (h) => h(App),
}).$mount('#app');
