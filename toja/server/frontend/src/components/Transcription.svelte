<script lang="ts">
    import { onMount, onDestroy } from 'svelte';
    import { Editor } from '@tiptap/core';
    import Document from '@tiptap/extension-document';
    import Paragraph from '@tiptap/extension-paragraph';
    import Text from '@tiptap/extension-text';

    import { getJsonApiObjects } from '../stores';

    export let source: SourceDocument;

    let selectedJoke = null as JokeDocument;
    let jokes = [];

    let editorElement: HTMLElement;
    let editor: Editor;

    async function loadJokes(source: SourceDocument) {
        const jokeIds = source.relationships.jokes.data.map((rel) => {
                return rel.id;
            })
            jokes = await getJsonApiObjects('jokes', 'filter[id]=' + jokeIds.join(',')) as JokeDocument[];
    }

    onMount(() => {
        editor = new Editor({
            element: editorElement,
            extensions: [
                Document,
                Paragraph,
                Text,
            ],
        });
    });

    onDestroy(() => {
        if (editor) {
            editor.destroy();
        }
    });

    $: {
        loadJokes(source);
    }

    function selectJoke(joke: JokeDocument) {
        selectedJoke = joke;
    }
</script>

<div class="flex flex-col h-full overflow-hidden">
    <nav class="flex-none">
        <ul class="flex flex-row flex-wrap justify-end">
            <li role="presentation">
                <button class="block p-2 {selectedJoke === null ? 'text-gray-400' : 'text-accent'}">
                    <svg viewBox="0 0 24 24" class="w-6 h-6">
                        <path fill="currentColor" d="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z" />
                    </svg>
                </button>
            </li>
            <li role="presentation">
                <button class="block p-2 {selectedJoke === null ? 'text-gray-400' : 'text-accent'}">
                    <svg viewBox="0 0 24 24" class="w-6 h-6">
                        <path fill="currentColor" d="M21,7L9,19L3.5,13.5L4.91,12.09L9,16.17L19.59,5.59L21,7Z" />
                    </svg>
                </button>
            </li>
        </ul>
    </nav>
    <div class="flex-1 flex flex-row space-x-4 overflow-hidden">
        <div class="flex-1 overflow-auto">
            <ul>
                {#each jokes as joke}
                    <li role="presentation" class="border-b border-gray pb-2 mb-2">
                        <button on:click={() => { selectJoke(joke); }} class="block w-full {selectedJoke === joke ? 'border-2 border-primary' : ''}">
                            <img src={joke.attributes.data} alt="" class="max-w-full"/>
                        </button>
                    </li>
                {/each}
            </ul>
        </div>
        <div bind:this={editorElement} class="flex-1 overflow-hidden">
        </div>
    </div>
</div>