<template>
  <div>
    <joke-selector></joke-selector>
    <joke-list></joke-list>
    <joke-transcriber></joke-transcriber>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import JokeSelector from '@/components/JokeSelector.vue';
import JokeList from '@/components/JokeList.vue';
import JokeTranscriber from '@/components/JokeTranscriber.vue';

@Component({
    components: {
        JokeSelector,
        JokeList,
        JokeTranscriber,
    },
    mounted() {
        this.$store.dispatch('loadSource');
        this.$store.dispatch('loadJokes');
    },
})
export default class Workbench extends Vue {}
</script>
