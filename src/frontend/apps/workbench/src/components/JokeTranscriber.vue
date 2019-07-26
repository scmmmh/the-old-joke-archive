<template>
    <div v-if="selectedJoke">
    </div>
    <div v-else>
        <p>Please select a joke from the list to transcribe and annotate it.</p>
    </div>
</template>

<script lang="ts">
import { Component, Vue, Watch } from 'vue-property-decorator';

@Component
export default class JokeTranscriber extends Vue {

    // **************
    // Event handlers
    // **************

    // ************
    // Dynamic data
    // ************

    public get selectedJoke() {
        return this.$store.state.selected;
    }
}
</script>
