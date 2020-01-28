<template>
    <div id="app" class="workbench">
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
})
export default class App extends Vue {
    public mounted() {
        this.$store.dispatch('loadSource');
        this.$store.dispatch('loadJokes');
    }
}
</script>
