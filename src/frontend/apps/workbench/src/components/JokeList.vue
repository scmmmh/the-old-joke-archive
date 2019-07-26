<template>
    <div class="joke-list" v-if="jokes">
        <nav>
            <ul role="menu" class="menu">
                <li role="presentation">
                    <a data-action="move" role="menuitem" v-bind:disabled="nothingSelected" @click="deleteSelected()">
                        <svg viewBox="0 0 24 24" class="icon mdi">
                            <path d="M6,19A2,2 0 0,0 8,21H16A2,2 0 0,0 18,19V7H6V19M8,9H16V19H8V9M15.5,4L14.5,3H9.5L8.5,4H5V6H19V4H15.5Z" />
                        </svg>
                    </a>
                </li>
            </ul>
        </nav>
        <div>
            <ul>
                <li v-for="joke in jokes">
                    <a v-if="joke === selectedJoke" class="selected" @click="select(joke)">
                        <img v-bind:src="joke.attributes.raw"/>
                    </a>
                    <a v-else @click="select(joke)">
                        <img v-bind:src="joke.attributes.raw"/>
                    </a>
                </li>
            </ul>
        </div>
    </div>
    <div v-else>
        <p>Draw joke outlines on the left-hand side to extract jokes.</p>
    </div>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from 'vue-property-decorator';
import { Joke } from '@/interfaces';

@Component
export default class JokeList extends Vue {

    // **************
    // Event handlers
    // **************

    public select(joke: Joke) {
        this.$store.commit('selectJoke', joke);
    }

    public deleteSelected() {
        this.$store.dispatch('deleteJoke', this.$store.state.selected);
    }

    // ************
    // Dynamic data
    // ************

    public get jokes() {
        return this.$store.state.jokes;
    }

    public get selectedJoke() {
        return this.$store.state.selected;
    }

    public get nothingSelected() {
        return this.$store.state.selected === null ? 'disabled' : null;
    }
}
</script>
