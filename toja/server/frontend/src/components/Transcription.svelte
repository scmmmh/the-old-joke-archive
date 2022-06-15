<script lang="ts">
    import { onMount, onDestroy } from 'svelte';
    import { Editor, isActive } from '@tiptap/core';
    import Document from '@tiptap/extension-document';
    import Paragraph from '@tiptap/extension-paragraph';
    import Text from '@tiptap/extension-text';
    import BubbleMenu from '@tiptap/extension-bubble-menu';

    import Busy from './Busy.svelte';
    import IconButton from './IconButton.svelte';
    import Input from './Input.svelte';
    import { getJsonApiObjects, authUser, saveJsonApiObject } from '../stores';
    import { PersonMark, SpokenTextMark, TitleMark, AttributionMark } from './tiptap';

    export let source: SourceDocument;

    let selectedJoke = null as JokeDocument;
    let jokes = [];

    let editorElement: HTMLElement;
    let bubbleMenuElement: HTMLElement;
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
                TitleMark,
                PersonMark,
                SpokenTextMark,
                AttributionMark,
                BubbleMenu.configure({
                    element: bubbleMenuElement,
                }),
            ],
            onTransaction: () => {
                editor = editor
            },
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
        <ul class="flex flex-row flex-wrap justify-end gap-1 pb-1">
            <li role="presentation">
                <IconButton on:action={() => { selectJoke(null); }} disabled={selectedJoke === null} label="Discard all changes"><path fill="currentColor" d="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z" /></IconButton>
            </li>
            <li role="presentation">
                <IconButton on:action={saveJoke} disabled={selectedJoke === null} busy={saveBusy} label="Save the transcription" busyLabel="Saving the transcription"><path fill="currentColor" d="M21,7L9,19L3.5,13.5L4.91,12.09L9,16.17L19.59,5.59L21,7Z" /></IconButton>
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
            <div bind:this={editorElement} class="h-1/2 overflow-auto border border-gray p-2 {selectedJoke === null ? 'hidden' : ''} text-lg"></div>
            <nav bind:this={bubbleMenuElement} class="bg-white/95 border border-primary shadow-lg">
                <ul class="flex flex-row px-1 py-1 gap-1">
                    {#if editor}
                        <li role="presentation">
                            <IconButton on:action={() => { editor.chain().focus().toggleMark('TitleMark').run(); }} active={editor.isActive('TitleMark')} label="Annotate as Title"><path fill="currentColor" d="M5,4V7H10.5V19H13.5V7H19V4H5Z" /></IconButton>
                        </li>
                        <li role="presentation">
                            <IconButton on:action={() => { editor.chain().focus().toggleMark('PersonMark').run(); }} active={editor.isActive('PersonMark')} label="Annotate as a Person"><path fill="currentColor" d="M12,4A4,4 0 0,1 16,8A4,4 0 0,1 12,12A4,4 0 0,1 8,8A4,4 0 0,1 12,4M12,14C16.42,14 20,15.79 20,18V20H4V18C4,15.79 7.58,14 12,14Z" /></IconButton>
                        </li>
                        <li role="presentation">
                            <IconButton on:action={() => { editor.chain().focus().toggleMark('SpokenTextMark').run(); }} active={editor.isActive('SpokenTextMark')} label="Annotate as Spoken Text"><path fill="currentColor" d="M20,2H4A2,2 0 0,0 2,4V22L6,18H20A2,2 0 0,0 22,16V4A2,2 0 0,0 20,2M8,14H6V12H8V14M8,11H6V9H8V11M8,8H6V6H8V8M15,14H10V12H15V14M18,11H10V9H18V11M18,8H10V6H18V8Z" /></IconButton>
                        </li>
                        <li role="presentation">
                            <IconButton on:action={() => { editor.chain().focus().toggleMark('AttributionMark').run(); }} active={editor.isActive('AttributionMark')} label="Annotate as Attribution"><path fill="currentColor" d="M22,22H2V20H22V22M6.2,17.3L5.5,18L4.1,16.6L2.7,18L2,17.3L3.4,15.9L2,14.5L2.7,13.8L4.1,15.2L5.5,13.8L6.2,14.5L4.8,15.9L6.2,17.3M16.22,14.43C16.22,13.85 15.5,13.2 14.06,12.46C12.23,11.54 11,10.79 10.36,10.24C9.71,9.68 9.39,9.06 9.39,8.37C9.39,6.59 10.3,5.12 12.12,3.95C13.94,2.78 15.43,2.19 16.57,2.19C17.31,2.19 17.85,2.32 18.18,2.58C18.5,2.83 18.68,3.27 18.68,3.9C18.68,4.18 18.56,4.42 18.31,4.63C18.07,4.83 17.87,4.93 17.74,4.93C17.63,4.93 17.43,4.83 17.13,4.64L16.55,4.38C16.08,4.38 15.14,4.71 13.71,5.38C12.29,6.04 11.58,6.79 11.58,7.63C11.58,8.14 11.82,8.6 12.32,9C12.82,9.42 13.71,9.93 15,10.53C16.03,11 16.86,11.5 17.5,12.07C18.1,12.61 18.41,13.25 18.41,14C18.41,15.34 17.47,16.41 15.58,17.17C13.7,17.94 11.9,18.32 10.19,18.32C8.75,18.32 8,17.83 8,16.86C8,16.5 8.19,16.27 8.5,16.11C8.83,15.95 9.16,15.87 9.5,15.87L10.25,16L10.97,16.13C11.95,16.13 13,15.97 14.13,15.64C15.26,15.32 15.96,14.91 16.22,14.43Z" /></IconButton>
                        </li>
                    {/if}
                </ul>
            </nav>
            <div class="h-1/2 overflow-auto pt-2 {selectedJoke === null ? 'hidden' : ''}">
                {#if editor}
                    {#if editor.isActive('PersonMark')}
                        <Input on:change={(ev) => { editor.chain().focus().extendMarkRange('PersonMark').updateAttributes('PersonMark', {gender: ev.detail}).run(); }} type="select" value={editor.getAttributes('PersonMark').gender} values={[['unknown', 'Unknown'], ['female', 'Female'], ['male', 'Male']]}>Gender</Input>
                    {/if}
                {/if}
            </div>
        </div>
    </div>
</div>
