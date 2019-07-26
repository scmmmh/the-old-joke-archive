import axios from 'axios';
import Vue from 'vue';
import Vuex from 'vuex';

import { State, Config, Joke, Transcription } from '@/interfaces';

Vue.use(Vuex);

function makeInitialState(config: Config): State {
    return {
        baseURL: config.baseURL,
        sourceId: config.sourceId,
        userId: config.userId,
        source: {},
        jokes: [],
        selected: null,
        transcription: null,
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
                    state.transcription = null;
                } else {
                    state.selected = joke;
                }
            },
            setTranscription(state, transcription: Transcription) {
                state.transcription = transcription;
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
                axios.get(store.state.baseURL + '/jokes', {
                    params: {
                        'filter[owner_id]': store.state.userId,
                        'filter[parent_id]': store.state.sourceId,
                    },
                }).then((response) => {
                    store.commit('updateJokesList', response.data.data);
                });
            },
            loadTranscription(store) {
                if (store.state.selected) {
                    axios.get(store.state.baseURL + '/transcriptions', {
                        params: {
                            'filter[owner_id]': store.state.userId,
                            'filter[source_id]': store.state.selected.id,
                        },
                    }).then((response) => {
                        if (response.data.data.length === 0) {
                            store.commit('setTranscription', {
                                type: 'transcriptions',
                                attributes: {
                                    source_id: store.state.selected.id,
                                    text: '',
                                    status: 'new',
                                },
                            });
                        } else {
                            store.commit('setTranscription', response.data.data[0]);
                        }
                    });
                }
            },
            addJoke(store, bbox) {
                axios.post(store.state.baseURL + '/jokes', {
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
                        axios.put(store.state.baseURL + '/jokes/' + joke.id, {
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
                axios.delete(store.state.baseURL + '/jokes/' + joke.id).
                      then((response) => {
                          store.dispatch('loadJokes');
                      });
            },
            updateTranscription(store, attrs: object) {
                const transcription = { ...store.state.transcription } as Transcription;
                transcription.attributes = { ...transcription.attributes, ...attrs };
                if (transcription.id) {
                    axios.patch(store.state.baseURL + '/transcriptions/' + transcription.id, {
                        data: transcription,
                    }).then((response) => {
                        store.commit('setTranscription', response.data.data);
                    });
                } else {
                    axios.post(store.state.baseURL + '/transcriptions', {
                        data: transcription,
                    }).then((response) => {
                        store.commit('setTranscription', response.data.data);
                    });
                }
            },
        },
    });
}
