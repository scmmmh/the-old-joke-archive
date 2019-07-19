import axios from 'axios';
import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

function makeInitialState(config: object) {
    return {
        baseURL: config.baseURL,
        source: {},
    };
}

export default function makeStore(config: object) {
    return new Vuex.Store({
        state: makeInitialState(config),
        mutations: {
            updateSource(state, source) {
                state.source = source;
            },
        },
        actions: {
            loadSource(ctx, sourceId) {
                axios.get('/api/sources/' + sourceId).then((data) => {
                    ctx.commit('updateSource', data.data);
                });
            },
        },
    });
}
