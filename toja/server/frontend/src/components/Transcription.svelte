<script lang="ts">
    import { onMount, onDestroy } from 'svelte';
    import { Editor } from '@tiptap/core';
    import Document from '@tiptap/extension-document';
    import Paragraph from '@tiptap/extension-paragraph';
    import Text from '@tiptap/extension-text';

    import { getJsonApiObjects, authUser, saveJsonApiObject } from '../stores';
    import Busy from './Busy.svelte';

    export let source: SourceDocument;

    let selectedJoke = null as JokeDocument;
    let jokes = [];

    let editorElement: HTMLElement;
    let editor: Editor;
    let saveBusy = false;

    function sleep(ms: number) {
        return new Promise((resolve) => {
            setTimeout(resolve, ms);
        });
    }

    async function loadJokes(source: SourceDocument) {
        let foundSelectedJoke = false;
        const jokeIds = source.relationships.jokes.data.map((rel) => {
            if (selectedJoke && rel.id === selectedJoke.id) {
                foundSelectedJoke = true;
            }
            return rel.id;
        });
        if (selectedJoke !== null && !foundSelectedJoke) {
            selectJoke(null);
        }
        jokes = await getJsonApiObjects('jokes', 'filter[id]=' + jokeIds.join(',')) as JokeDocument[];
        while (jokes.filter((joke) => { return !joke.attributes.transcriptions || !joke.attributes.transcriptions.auto; }).length > 0) {
            await sleep(1000);
            jokes = await getJsonApiObjects('jokes', 'filter[id]=' + jokeIds.join(',')) as JokeDocument[];
        }
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
        if (selectedJoke) {
            if ((selectedJoke.attributes as JokeDocumentAttributes).transcriptions[$authUser.id]) {
                editor.commands.setContent((selectedJoke.attributes as JokeDocumentAttributes).transcriptions[$authUser.id]);
            } else if ((selectedJoke.attributes as JokeDocumentAttributes).transcriptions.auto) {
                editor.commands.setContent((selectedJoke.attributes as JokeDocumentAttributes).transcriptions.auto);
            }
        }
    }

    async function saveJoke() {
        saveBusy = true;
        try {
            const updatedJoke = {
                type: 'jokes',
                id: selectedJoke.id,
                attributes: {
                    actions: [
                        {
                            annotated: editor.state.doc.toJSON(),
                        },
                        {
                            status: 'annotated'
                        }
                    ]
                },
                relationships: selectedJoke.relationships
            }
            selectedJoke = await saveJsonApiObject(updatedJoke) as JokeDocument;
            for (let idx = 0; idx < jokes.length; idx++) {
                if (jokes[idx].id === selectedJoke.id) {
                    jokes[idx] = selectedJoke;
                }
            }
        } finally {
            saveBusy = false;
        }
    }
</script>

<div class="flex flex-col h-full overflow-hidden">
    <nav class="flex-none">
        <ul class="flex flex-row flex-wrap justify-end">
            <li role="presentation">
                <button on:click={() => { selectJoke(null); }} class="block p-2 {selectedJoke === null ? 'text-gray-400' : 'text-accent'}">
                    <svg viewBox="0 0 24 24" class="w-6 h-6">
                        <path fill="currentColor" d="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z" />
                    </svg>
                </button>
            </li>
            <li role="presentation">
                {#if saveBusy}
                    <div class="p-2">
                        <Busy message="Saving..." size="icon"/>
                    </div>
                {:else}
                    <button on:click={saveJoke} class="block p-2 {selectedJoke === null ? 'text-gray-400' : 'text-accent'}">
                        <svg viewBox="0 0 24 24" class="w-6 h-6">
                            <path fill="currentColor" d="M21,7L9,19L3.5,13.5L4.91,12.09L9,16.17L19.59,5.59L21,7Z" />
                        </svg>
                    </button>
                {/if}
            </li>
        </ul>
    </nav>
    <div class="flex-1 flex flex-row space-x-4 overflow-hidden">
        <div class="flex-1 overflow-auto border border-gray">
            <ul>
                {#each jokes as joke}
                    <li role="presentation" class="border-b border-gray">
                        {#if ['extracted', 'extraction-verified'].indexOf(joke.attributes.status) < 0}
                            <button on:click={() => { selectJoke(joke); }} class="block p-2 w-full {selectedJoke === joke ? 'border-2 border-primary' : ''}">
                                <img src={joke.attributes.data} alt="" class="max-w-full"/>
                            </button>
                        {:else}
                            <div class="relative p-2">
                                <img src={joke.attributes.data} alt="" class="max-w-full opacity-60"/>
                                <div class="absolute left-1/2 top-1/2 transform -translate-x-1/2 -translate-y-1/2">
                                    <Busy message="Waiting for the OCR text"/>
                                </div>
                            </div>
                        {/if}
                    </li>
                {/each}
            </ul>
        </div>
        <div class="relative flex-1 overflow-hidden">
            {#if selectedJoke === null}
                <p class="absolute text-gray-700 left-1/2 top-1/2 transform -translate-x-1/2 -translate-y-1/2 text-center">Select a joke on the left to edit its text and annotations.</p>
            {/if}
            <div bind:this={editorElement} class="h-1/2 overflow-auto border border-gray p-2 {selectedJoke === null ? 'hidden' : ''}"></div>
            <div class="h-1/2 overflow-auto border border-gray {selectedJoke === null ? 'hidden' : ''}"></div>
        </div>
    </div>
</div>
