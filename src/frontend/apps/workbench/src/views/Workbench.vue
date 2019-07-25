<template>
  <div>
    <joke-selector></joke-selector>
    <div>List of extracted jokes</div>
    <div>Transcription and Annotation interface</div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import JokeSelector from '@/components/JokeSelector.vue'; // @ is an alias to /src

@Component({
    components: {
        JokeSelector,
    },
    mounted() {
        this.$store.dispatch('loadSource');
        this.$store.dispatch('loadJokes');
    },
})
export default class Workbench extends Vue {}
</script>
