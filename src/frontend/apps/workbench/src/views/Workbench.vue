<template>
  <div>
    <joke-selector></joke-selector>
    <joke-list></joke-list>
    <div>Transcription and Annotation interface</div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import JokeSelector from '@/components/JokeSelector.vue';
import JokeList from '@/components/JokeList.vue';

@Component({
    components: {
        JokeSelector,
        JokeList,
    },
    mounted() {
        this.$store.dispatch('loadSource');
        this.$store.dispatch('loadJokes');
    },
})
export default class Workbench extends Vue {}
</script>
