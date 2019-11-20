<template>
    <div class="joke-transcriber">
        <editor-menu-bar :editor="editor" v-slot="{ commands, isActive }">
            <nav>
                <ul role="menu" class="menu">
                    <li role="presentation">
                        <a data-action="confirm" role="menuitem" @click="saveChanges">
                            <svg viewBox="0 0 24 24" class="icon mdi">
                                <path d="M21,7L9,19L3.5,13.5L4.91,12.09L9,16.17L19.59,5.59L21,7Z" />
                            </svg>
                        </a>
                    </li>
                    <li role="presentation">
                        <a data-action="cancel" role="menuitem" @click="discardChanges">
                            <svg viewBox="0 0 24 24" class="icon mdi">
                                <path d="M12,2A10,10 0 0,1 22,12A10,10 0 0,1 12,22A10,10 0 0,1 2,12A10,10 0 0,1 12,2M12,4A8,8 0 0,0 4,12C4,13.85 4.63,15.55 5.68,16.91L16.91,5.68C15.55,4.63 13.85,4 12,4M12,20A8,8 0 0,0 20,12C20,10.15 19.37,8.45 18.32,7.09L7.09,18.32C8.45,19.37 10.15,20 12,20Z" />
                            </svg>
                        </a>
                    </li>
                    <li role="separator"></li>
                    <li role="presentation">
                        <a role="menuitem" :aria-current="isActive.title() ? 'true' : null" @click="commands.title">Title</a>
                    </li>
                    <li role="presentation">
                        <a role="menuitem" :aria-current="isActive.speaker() ? 'true' : null" @click="commands.speaker">Speaker</a>
                    </li>
                    <li role="presentation">
                        <a role="menuitem" :aria-current="isActive.speech() ? 'true' : null" @click="commands.speech">Speech</a>
                    </li>
                    <li role="presentation">
                        <a role="menuitem" :aria-current="isActive.attribution() ? 'true' : null" @click="commands.attribution">Attribution</a>
                    </li>
                </ul>
            </nav>
        </editor-menu-bar>
        <editor-content :editor="editor"></editor-content>
        <div>Attributes</div>
        <div class="overlay" v-if="noTranscription">
            <p>Please select a joke from the list to transcribe and annotate it.</p>
        </div>
    </div>
</template>

<script lang="ts">
import { Component, Vue, Watch } from 'vue-property-decorator';
// @ts-ignore
import { Editor, EditorContent, EditorMenuBar } from 'tiptap';
import ConfigurableMark from '@/markup/ConfigurableMark';

import { Joke, Transcription } from '@/interfaces';

@Component({
    components: {
        EditorContent,
        EditorMenuBar,
    },
})
export default class JokeTranscriber extends Vue {

    public data() {
        return {
            editor: new Editor({
                extensions: [
                    new ConfigurableMark('title'),
                    new ConfigurableMark('speaker'),
                    new ConfigurableMark('speech'),
                    new ConfigurableMark('attribution'),
                ],
            }),
        };
    }

    // ****************
    // Lifecycle events
    // ****************

    public beforeDestroy() {
        this.$data.editor.destroy();
    }

    // **************
    // Event handlers
    // **************

    public saveChanges() {
        this.$store.dispatch('updateTranscription', {
            text: this.$data.editor.getJSON(),
        });
    }

    public discardChanges() {
        this.$data.editor.setContent(this.$store.state.transcription.attributes.text);
    }

    // ************
    // Dynamic data
    // ************

    public get noTranscription() {
        return this.$store.state.transcription === null;
    }

    @Watch('$store.state.selected')
    public watchSelectedJoke(newValue: Joke, oldValue: Joke) {
        this.$store.dispatch('loadTranscription');
    }

    @Watch('$store.state.transcription')
    public watchTranscription(newValue: Transcription, oldValue: Transcription) {
        if (newValue) {
            this.$data.editor.setContent(newValue.attributes.text);
        } else {
            this.$data.editor.setContent('');
        }
    }
}
</script>
