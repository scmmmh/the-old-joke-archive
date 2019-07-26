import axios from 'axios';
import Vue from 'vue';
import Vuex from 'vuex';

import { State, Config, Joke } from '@/interfaces';

Vue.use(Vuex);

function makeInitialState(config: Config): State {
    return {
        baseURL: config.baseURL,
        sourceId: config.sourceId,
        source: {},
        jokes: [],
        selected: null,
    };
}

export default function makeStore(config: Config) {
    return new Vuex.Store({
        state: makeInitialState(config),
        mutations: {
            updateSource(state, source) {
                state.source = source;
            },
            updateJokesList(state, jokes: Joke[]) {
                state.jokes = jokes;
            },
            selectJoke(state, joke: Joke) {
                if (state.selected === joke) {
                    state.selected = null;
                } else {
                    state.selected = joke;
                }
            },
        },
        actions: {
            loadSource(store) {
                axios.get(store.state.baseURL + '/sources/' + store.state.sourceId).then((response) => {
                    store.commit('updateSource', response.data.data);
                    store.dispatch('loadJokes');
                });
            },
            loadJokes(store) {
                axios.get(store.state.baseURL + '/sources/' + store.state.sourceId + '/jokes').then((response) => {
                    store.commit('updateJokesList', response.data.data);
                });
            },
            addJoke(store, bbox) {
                axios.post(store.state.baseURL + '/sources/' + store.state.sourceId + '/jokes', {
                    data: {
                        type: 'jokes',
                        attributes: {
                            parent_id: store.state.sourceId,
                            bbox,
                        },
                    },
                }).then((response) => {
                    const jokes = store.state.jokes.slice();
                    jokes.push(response.data.data);
                    store.commit('updateJokesList', jokes);
                });
            },
            updateJoke(store, { jid, attrs }) {
                store.state.jokes.forEach((joke: Joke) => {
                    if (joke.id === jid) {
                        joke = { ...joke };
                        joke.attributes = { ...joke.attributes, ...attrs };
                        axios.put(store.state.baseURL + '/sources/' + store.state.sourceId + '/jokes/' + joke.id, {
                            data: joke,
                        }).then((response) => {
                            const newJokes: Joke[] = [];
                            store.state.jokes.forEach((joke2: Joke) => {
                                if (joke2.id === jid) {
                                    newJokes.push(response.data.data);
                                } else {
                                    newJokes.push(joke2);
                                }
                            });
                            store.commit('updateJokesList', newJokes);
                        });
                    }
                });
            },
            deleteJoke(store, joke: Joke) {
                axios.delete(store.state.baseURL + '/sources/' + store.state.sourceId + '/jokes/' + joke.id).
                      then((response) => {
                          store.dispatch('loadJokes');
                      });
            },
        },
    });
}
