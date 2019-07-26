<template>
    <div class="joke-transcriber">
        <nav>
            <ul role="menu" class="menu">
                <li role="presentation">
                    <a role="menuitem">Title</a>
                </li>
            </ul>
        </nav>
        <editor-content :editor="editor"></editor-content>
        <div class="overlay" v-if="!selectedJoke">
            <p>Please select a joke from the list to transcribe and annotate it.</p>
        </div>
    </div>
</template>

<script lang="ts">
import { Component, Vue, Watch } from 'vue-property-decorator';
// @ts-ignore
import { Editor, EditorContent } from 'tiptap';

@Component({
    components: {
        EditorContent,
    },
})
export default class JokeTranscriber extends Vue {

    private editor = new Editor({
        content: '<p></p>',
    });

    // ****************
    // Lifecycle events
    // ****************

    public beforeDestroy() {
        this.$data.editor.destroy();
    }

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
