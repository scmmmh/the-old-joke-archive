<script lang="ts">
    import { onMount, onDestroy } from 'svelte';
    import { Editor } from '@tiptap/core';
    import Document from '@tiptap/extension-document';
    import Paragraph from '@tiptap/extension-paragraph';
    import Text from '@tiptap/extension-text';
    import BubbleMenu from '@tiptap/extension-bubble-menu';
    import deepcopy from 'deepcopy';
    import deepequal from 'deep-equal';

    import Busy from './Busy.svelte';
    import IconButton from './IconButton.svelte';
    import Input from './Input.svelte';
    import { getJsonApiObjects, authUser, saveJsonApiObject } from '../stores';
    import { PersonMark, SpokenTextMark, TitleMark, AttributionMark, AsideMark, LocationMark, ObjectMark, QuestionMark, AnswerMark } from './tiptap';

    export let source: SourceDocument;

    let selectedJoke = null as JokeDocument;
    let originalSelectedJoke = null as JokeDocument;
    let jokes = [];

    let editorElement: HTMLElement;
    let bubbleMenuElement: HTMLElement;
    let editor: Editor;
    let saveBusy = false;
    let mode = 'text';
    let newJokeTopic = '';
    let newJokeTopicSuggestions = [];
    let suggestTopicsDebounce = 0;
    let newJokeTopicElement: HTMLInputElement;

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
                AsideMark,
                LocationMark,
                ObjectMark,
                QuestionMark,
                AnswerMark,
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
        selectedJoke = deepcopy(joke);
        originalSelectedJoke = joke;
        if (selectedJoke) {
            if ((selectedJoke.attributes as JokeDocumentAttributes).transcriptions[$authUser.id]) {
                editor.commands.setContent((selectedJoke.attributes as JokeDocumentAttributes).transcriptions[$authUser.id]);
            } else if ((selectedJoke.attributes as JokeDocumentAttributes).transcriptions.auto) {
                editor.commands.setContent((selectedJoke.attributes as JokeDocumentAttributes).transcriptions.auto);
            }
        }
    }

    function toggleJokeCategory(category: string, enabled: boolean) {
        if (selectedJoke) {
            if (enabled && (selectedJoke.attributes as JokeDocumentAttributes).categories.indexOf(category) < 0) {
                (selectedJoke.attributes as JokeDocumentAttributes).categories.push(category);
            } else if (!enabled && (selectedJoke.attributes as JokeDocumentAttributes).categories.indexOf(category) >= 0) {
                (selectedJoke.attributes as JokeDocumentAttributes).categories.splice((selectedJoke.attributes as JokeDocumentAttributes).categories.indexOf(category), 1);
            }
        }
    }

    function jokeTopicKeyup(ev: KeyboardEvent) {
        if (selectedJoke) {
            if (ev.key === 'Enter') {
                ev.preventDefault();
                addJokeTopic(newJokeTopic);
                newJokeTopic = '';
            } else if (newJokeTopic.trim() !== '') {
                suggestTopics();
            }
        }
    }

    function suggestTopics() {
        window.clearTimeout(suggestTopicsDebounce);
        window.setTimeout(async () => {
            const response = await window.fetch('/api/suggest/joke_topics?q=' + newJokeTopic);
            if (response.status === 200) {
                const data = await response.json();
                newJokeTopicSuggestions = data.data.filter((suggestion) => {
                    return selectedJoke.attributes.topics.indexOf(suggestion.id) < 0;
                });
            }
        }, 80);
    }

    function addJokeTopic(topic: string) {
        if (!Array.isArray(selectedJoke.attributes.topics)) {
            selectedJoke.attributes.topics = [];
        }
        if (selectedJoke.attributes.topics.indexOf(topic) < 0 && topic.trim() !== '') {
            selectedJoke.attributes.topics.push(topic);
            selectedJoke = selectedJoke;
        }
    }

    function removeJokeTopic(topic: string) {
        if (!Array.isArray(selectedJoke.attributes.topics)) {
            selectedJoke.attributes.topics = [];
        }
        if (selectedJoke.attributes.topics.indexOf(topic) >= 0) {
            selectedJoke.attributes.topics.splice(selectedJoke.attributes.topics.indexOf(topic), 1);
            selectedJoke = selectedJoke;
        }
    }

    function addSuggestedTopic(topic: string) {
        addJokeTopic(topic);
        newJokeTopic = '';
        newJokeTopicSuggestions = [];
        newJokeTopicElement.focus();
    }

    async function publishJoke(status: 'published' | 'annotated') {
        const updatedJoke = {
            type: 'jokes',
            id: selectedJoke.id,
            attributes: {
                actions: [
                    {status: status}
                ],
            },
            relationships: selectedJoke.relationships
        }
        originalSelectedJoke = await saveJsonApiObject(updatedJoke) as JokeDocument;
        for (let idx = 0; idx < jokes.length; idx++) {
            if (jokes[idx].id === selectedJoke.id) {
                jokes[idx] = originalSelectedJoke;
            }
        }
        selectedJoke = deepcopy(originalSelectedJoke);
    }

    async function saveJoke() {
        saveBusy = true;
        try {
            let actions = [] as JokeUpdateAction[];
            const text = editor.state.doc.toJSON() as TiptapNode;
            if (!deepequal(text, (originalSelectedJoke.attributes as JokeDocumentAttributes).transcriptions[$authUser.id])) {
                actions = actions.concat([
                    {
                        annotated: text,
                    },
                    {
                        status: 'annotated',
                    }
                ]);
            }
            if (!deepequal((selectedJoke.attributes as JokeDocumentAttributes).categories, (originalSelectedJoke.attributes as JokeDocumentAttributes).categories)) {
                actions.push({
                    categories: (selectedJoke.attributes as JokeDocumentAttributes).categories,
                });
            }
            if (!deepequal((selectedJoke.attributes as JokeDocumentAttributes).topics, (originalSelectedJoke.attributes as JokeDocumentAttributes).topics)) {
                actions.push({
                    topics: (selectedJoke.attributes as JokeDocumentAttributes).topics,
                });
            }
            if ((selectedJoke.attributes as JokeDocumentAttributes).language !== (originalSelectedJoke.attributes as JokeDocumentAttributes).language) {
                actions.push({
                    language: (selectedJoke.attributes as JokeDocumentAttributes).language,
                });
            }
            const updatedJoke = {
                type: 'jokes',
                id: selectedJoke.id,
                attributes: {
                    actions: actions,
                },
                relationships: selectedJoke.relationships
            }
            originalSelectedJoke = await saveJsonApiObject(updatedJoke) as JokeDocument;
            for (let idx = 0; idx < jokes.length; idx++) {
                if (jokes[idx].id === selectedJoke.id) {
                    jokes[idx] = originalSelectedJoke;
                }
            }
            selectedJoke = deepcopy(originalSelectedJoke);
        } finally {
            saveBusy = false;
        }
    }
</script>

<div class="flex flex-col h-full overflow-hidden">
    <div class="flex-none flex flex-row space-x-4">
        <div class="flex-1"></div>
        <nav class="flex-1">
            <ul class="flex flex-row flex-wrap gap-1 pb-1">
                <li role="presentation">
                    <IconButton on:action={() => { mode = 'text'; }} disabled={selectedJoke === null} label="Transcribe and annotate the joke" active={mode === 'text'}><path fill="currentColor" d="M4,5H20V7H4V5M4,9H20V11H4V9M4,13H20V15H4V13M4,17H14V19H4V17Z" /></IconButton>
                </li>
                <li role="presentation">
                    <IconButton on:action={() => { mode = 'settings'; }} disabled={selectedJoke === null} label="Edit the joke's settings" active={mode === 'settings'}><path fill="currentColor" d="M15.9,18.45C17.25,18.45 18.35,17.35 18.35,16C18.35,14.65 17.25,13.55 15.9,13.55C14.54,13.55 13.45,14.65 13.45,16C13.45,17.35 14.54,18.45 15.9,18.45M21.1,16.68L22.58,17.84C22.71,17.95 22.75,18.13 22.66,18.29L21.26,20.71C21.17,20.86 21,20.92 20.83,20.86L19.09,20.16C18.73,20.44 18.33,20.67 17.91,20.85L17.64,22.7C17.62,22.87 17.47,23 17.3,23H14.5C14.32,23 14.18,22.87 14.15,22.7L13.89,20.85C13.46,20.67 13.07,20.44 12.71,20.16L10.96,20.86C10.81,20.92 10.62,20.86 10.54,20.71L9.14,18.29C9.05,18.13 9.09,17.95 9.22,17.84L10.7,16.68L10.65,16L10.7,15.31L9.22,14.16C9.09,14.05 9.05,13.86 9.14,13.71L10.54,11.29C10.62,11.13 10.81,11.07 10.96,11.13L12.71,11.84C13.07,11.56 13.46,11.32 13.89,11.15L14.15,9.29C14.18,9.13 14.32,9 14.5,9H17.3C17.47,9 17.62,9.13 17.64,9.29L17.91,11.15C18.33,11.32 18.73,11.56 19.09,11.84L20.83,11.13C21,11.07 21.17,11.13 21.26,11.29L22.66,13.71C22.75,13.86 22.71,14.05 22.58,14.16L21.1,15.31L21.15,16L21.1,16.68M6.69,8.07C7.56,8.07 8.26,7.37 8.26,6.5C8.26,5.63 7.56,4.92 6.69,4.92A1.58,1.58 0 0,0 5.11,6.5C5.11,7.37 5.82,8.07 6.69,8.07M10.03,6.94L11,7.68C11.07,7.75 11.09,7.87 11.03,7.97L10.13,9.53C10.08,9.63 9.96,9.67 9.86,9.63L8.74,9.18L8,9.62L7.81,10.81C7.79,10.92 7.7,11 7.59,11H5.79C5.67,11 5.58,10.92 5.56,10.81L5.4,9.62L4.64,9.18L3.5,9.63C3.41,9.67 3.3,9.63 3.24,9.53L2.34,7.97C2.28,7.87 2.31,7.75 2.39,7.68L3.34,6.94L3.31,6.5L3.34,6.06L2.39,5.32C2.31,5.25 2.28,5.13 2.34,5.03L3.24,3.47C3.3,3.37 3.41,3.33 3.5,3.37L4.63,3.82L5.4,3.38L5.56,2.19C5.58,2.08 5.67,2 5.79,2H7.59C7.7,2 7.79,2.08 7.81,2.19L8,3.38L8.74,3.82L9.86,3.37C9.96,3.33 10.08,3.37 10.13,3.47L11.03,5.03C11.09,5.13 11.07,5.25 11,5.32L10.03,6.06L10.06,6.5L10.03,6.94Z" /></IconButton>
                </li>
                <li role="presentation" class="flex-1"></li>
                {#if selectedJoke && selectedJoke.attributes.status === 'published'}
                    <li role="presentation">
                        <IconButton on:action={() => { publishJoke('annotated'); }} disabled={selectedJoke === null} label="Unpublish the joke"><path fill="currentColor" d="M20.8 22.7L15 16.9V20H9V14H5L8.6 10.4L1.1 3L2.4 1.7L22.1 21.4L20.8 22.7M19 6V4H7.2L9.2 6H19M17.2 14H19L12 7L11.1 7.9L17.2 14Z" /></IconButton>
                    </li>
                {:else}
                    <li role="presentation">
                        <IconButton on:action={() => { publishJoke('published'); }} disabled={selectedJoke === null} label="Publish the joke"><path fill="currentColor" d="M5,4V6H19V4H5M5,14H9V20H15V14H19L12,7L5,14Z" /></IconButton>
                    </li>
                {/if}
                <li role="presentation" class="flex-none w-4"></li>
                <li role="presentation">
                    <IconButton on:action={() => { selectJoke(null); }} disabled={selectedJoke === null} label="Discard all changes"><path fill="currentColor" d="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z" /></IconButton>
                </li>
                <li role="presentation">
                    <IconButton on:action={saveJoke} disabled={selectedJoke === null} busy={saveBusy} label="Save the transcription" busyLabel="Saving the transcription"><path fill="currentColor" d="M21,7L9,19L3.5,13.5L4.91,12.09L9,16.17L19.59,5.59L21,7Z" /></IconButton>
                </li>
            </ul>
        </nav>
    </div>
    <div class="flex-1 flex flex-row space-x-4 overflow-hidden">
        <div class="flex-1 overflow-auto border border-gray">
            <ul>
                {#each jokes as joke}
                    <li role="presentation" class="border-b border-gray">
                        {#if ['extracted', 'extraction-verified'].indexOf(joke.attributes.status) < 0}
                            <button on:click={() => { selectJoke(joke); }} class="block p-2 w-full {originalSelectedJoke === joke ? 'border-2 border-primary' : ''}">
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
            <div bind:this={editorElement} class="h-1/2 overflow-auto border border-gray p-2 {selectedJoke === null || mode === 'settings' ? 'hidden' : ''} text-lg"></div>
            <nav bind:this={bubbleMenuElement} class="bg-white/95 border border-primary shadow-lg">
                <ul class="flex flex-row flex-wrap x-1 py-1 gap-1">
                    {#if editor}
                        <li role="presentation">
                            <IconButton on:action={() => { editor.chain().focus().toggleMark('TitleMark').run(); }} active={editor.isActive('TitleMark')} label="Annotate as Title"><path fill="currentColor" d="M5,4V7H10.5V19H13.5V7H19V4H5Z" /></IconButton>
                        </li>
                        <li role="presentation">
                            <IconButton on:action={() => { editor.chain().focus().toggleMark('AsideMark').run(); }} active={editor.isActive('AsideMark')} label="Annotate as Aside"><path fill="currentColor" d="M18.5,1.15C17.97,1.15 17.46,1.34 17.07,1.73L11.26,7.55L16.91,13.2L22.73,7.39C23.5,6.61 23.5,5.35 22.73,4.56L19.89,1.73C19.5,1.34 19,1.15 18.5,1.15M10.3,8.5L4.34,14.46C3.56,15.24 3.56,16.5 4.36,17.31C3.14,18.54 1.9,19.77 0.67,21H6.33L7.19,20.14C7.97,20.9 9.22,20.89 10,20.12L15.95,14.16" /></IconButton>
                        </li>
                        <li role="presentation">
                            <IconButton on:action={() => { editor.chain().focus().toggleMark('AttributionMark').run(); }} active={editor.isActive('AttributionMark')} label="Annotate as Attribution"><path fill="currentColor" d="M22,22H2V20H22V22M6.2,17.3L5.5,18L4.1,16.6L2.7,18L2,17.3L3.4,15.9L2,14.5L2.7,13.8L4.1,15.2L5.5,13.8L6.2,14.5L4.8,15.9L6.2,17.3M16.22,14.43C16.22,13.85 15.5,13.2 14.06,12.46C12.23,11.54 11,10.79 10.36,10.24C9.71,9.68 9.39,9.06 9.39,8.37C9.39,6.59 10.3,5.12 12.12,3.95C13.94,2.78 15.43,2.19 16.57,2.19C17.31,2.19 17.85,2.32 18.18,2.58C18.5,2.83 18.68,3.27 18.68,3.9C18.68,4.18 18.56,4.42 18.31,4.63C18.07,4.83 17.87,4.93 17.74,4.93C17.63,4.93 17.43,4.83 17.13,4.64L16.55,4.38C16.08,4.38 15.14,4.71 13.71,5.38C12.29,6.04 11.58,6.79 11.58,7.63C11.58,8.14 11.82,8.6 12.32,9C12.82,9.42 13.71,9.93 15,10.53C16.03,11 16.86,11.5 17.5,12.07C18.1,12.61 18.41,13.25 18.41,14C18.41,15.34 17.47,16.41 15.58,17.17C13.7,17.94 11.9,18.32 10.19,18.32C8.75,18.32 8,17.83 8,16.86C8,16.5 8.19,16.27 8.5,16.11C8.83,15.95 9.16,15.87 9.5,15.87L10.25,16L10.97,16.13C11.95,16.13 13,15.97 14.13,15.64C15.26,15.32 15.96,14.91 16.22,14.43Z" /></IconButton>
                        </li>
                        <li role="presentation" class="flex-none w-4"></li>
                        <li role="presentation">
                            <IconButton on:action={() => { editor.chain().focus().toggleMark('PersonMark').run(); }} active={editor.isActive('PersonMark')} label="Annotate as a Person"><path fill="currentColor" d="M12,4A4,4 0 0,1 16,8A4,4 0 0,1 12,12A4,4 0 0,1 8,8A4,4 0 0,1 12,4M12,14C16.42,14 20,15.79 20,18V20H4V18C4,15.79 7.58,14 12,14Z" /></IconButton>
                        </li>
                        <li role="presentation">
                            <IconButton on:action={() => { editor.chain().focus().toggleMark('SpokenTextMark').run(); }} active={editor.isActive('SpokenTextMark')} label="Annotate as Spoken Text"><path fill="currentColor" d="M20,2H4A2,2 0 0,0 2,4V22L6,18H20A2,2 0 0,0 22,16V4A2,2 0 0,0 20,2M8,14H6V12H8V14M8,11H6V9H8V11M8,8H6V6H8V8M15,14H10V12H15V14M18,11H10V9H18V11M18,8H10V6H18V8Z" /></IconButton>
                        </li>
                        <li role="presentation" class="flex-none w-4"></li>
                        <li role="presentation">
                            <IconButton on:action={() => { editor.chain().focus().toggleMark('LocationMark').run(); }} active={editor.isActive('LocationMark')} label="Annotate as Location"><path fill="currentColor" d="M12,11.5A2.5,2.5 0 0,1 9.5,9A2.5,2.5 0 0,1 12,6.5A2.5,2.5 0 0,1 14.5,9A2.5,2.5 0 0,1 12,11.5M12,2A7,7 0 0,0 5,9C5,14.25 12,22 12,22C12,22 19,14.25 19,9A7,7 0 0,0 12,2Z" /></IconButton>
                        </li>
                        <li role="presentation">
                            <IconButton on:action={() => { editor.chain().focus().toggleMark('ObjectMark').run(); }} active={editor.isActive('ObjectMark')} label="Annotate as Object"><path fill="currentColor" d="M21,16.5C21,16.88 20.79,17.21 20.47,17.38L12.57,21.82C12.41,21.94 12.21,22 12,22C11.79,22 11.59,21.94 11.43,21.82L3.53,17.38C3.21,17.21 3,16.88 3,16.5V7.5C3,7.12 3.21,6.79 3.53,6.62L11.43,2.18C11.59,2.06 11.79,2 12,2C12.21,2 12.41,2.06 12.57,2.18L20.47,6.62C20.79,6.79 21,7.12 21,7.5V16.5M12,4.15L6.04,7.5L12,10.85L17.96,7.5L12,4.15M5,15.91L11,19.29V12.58L5,9.21V15.91M19,15.91V9.21L13,12.58V19.29L19,15.91Z" /></IconButton>
                        </li>
                        <li role="presentation" class="flex-none w-4"></li>
                        <li role="presentation">
                            <IconButton on:action={() => { editor.chain().focus().toggleMark('QuestionMark').run(); }} active={editor.isActive('QuestionMark')} label="Annotate as Question"><path fill="currentColor" d="M12 3C6.5 3 2 6.6 2 11C2 13.1 3 15.1 4.8 16.5C4.8 17.1 4.4 18.7 2 21C2 21 5.5 21 8.5 18.5C9.6 18.8 10.8 19 12 19C17.5 19 22 15.4 22 11S17.5 3 12 3M13 15H11V13H13V15M14.8 10C14.5 10.4 14.1 10.6 13.7 10.8C13.4 11 13.3 11.1 13.2 11.3C13 11.5 13 11.7 13 12H11C11 11.5 11.1 11.2 11.3 10.9C11.5 10.7 11.9 10.4 12.4 10.1C12.7 10 12.9 9.8 13 9.6C13.1 9.4 13.2 9.1 13.2 8.9C13.2 8.6 13.1 8.4 12.9 8.2C12.7 8 12.4 7.9 12.1 7.9C11.8 7.9 11.6 8 11.4 8.1C11.2 8.2 11.1 8.4 11.1 8.7H9.1C9.2 8 9.5 7.4 10 7C10.5 6.6 11.2 6.5 12.1 6.5C13 6.5 13.8 6.7 14.3 7.1C14.8 7.5 15.1 8.1 15.1 8.8C15.2 9.2 15.1 9.6 14.8 10Z" /></IconButton>
                        </li>
                        <li role="presentation">
                            <IconButton on:action={() => { editor.chain().focus().toggleMark('AnswerMark').run(); }} active={editor.isActive('AnswerMark')} label="Annotate as Answer"><path fill="currentColor" d="M17,12V3A1,1 0 0,0 16,2H3A1,1 0 0,0 2,3V17L6,13H16A1,1 0 0,0 17,12M21,6H19V15H6V17A1,1 0 0,0 7,18H18L22,22V7A1,1 0 0,0 21,6Z" /></IconButton>
                        </li>
                    {/if}
                </ul>
            </nav>
            <div class="h-1/2 overflow-auto p-2 {selectedJoke === null || mode === 'settings' ? 'hidden' : ''}">
                {#if editor}
                    {#if editor.isActive('PersonMark')}
                        <Input on:change={(ev) => { editor.chain().focus().extendMarkRange('PersonMark').updateAttributes('PersonMark', {age: ev.detail}).run(); }} type="select" value={editor.getAttributes('PersonMark').age} values={[[null, 'Unknown'], ['baby', 'Baby'], ['child', 'Child'], ['adolescent', 'Adolescent'], ['adult', 'Adult'], ['elderly', 'Elderly']]}>Age</Input>
                        <Input on:change={(ev) => { editor.chain().focus().extendMarkRange('PersonMark').updateAttributes('PersonMark', {gender: ev.detail}).run(); }} type="select" value={editor.getAttributes('PersonMark').gender} values={[[null, 'Unknown'], ['female', 'Female'], ['male', 'Male']]}>Gender</Input>
                        <Input on:change={(ev) => { editor.chain().focus().extendMarkRange('PersonMark').updateAttributes('PersonMark', {class: ev.detail}).run(); }} type="select" value={editor.getAttributes('PersonMark').class} values={[[null, 'Unknown'], ['working', 'Working Class'], ['middle', 'Middle Class'], ['upper', 'Upper Class']]}>Social Status</Input>
                        <Input on:change={(ev) => { editor.chain().focus().extendMarkRange('PersonMark').updateAttributes('PersonMark', {role: ev.detail}).run(); }} type="text" value={editor.getAttributes('PersonMark').role}>Role / Job</Input>
                        <Input on:change={(ev) => { editor.chain().focus().extendMarkRange('PersonMark').updateAttributes('PersonMark', {nationality: ev.detail}).run(); }} type="text" value={editor.getAttributes('PersonMark').nationality}>Nationality</Input>
                    {/if}
                {/if}
            </div>
            {#if selectedJoke && mode === 'settings'}
                <div class="h-full overflow-auto p-2">
                    <div class="mb-2 text-sm">Categories</div>
                    <ul class="columns-3 mb-4">
                        {#each [['pun', 'Pun'], ['dialogue', 'Dialogue'], ['story', 'Story'], ['wit-wisdom', 'Wit-Wisdom'], ['conundrum', 'Conundrum'], ['verse', 'Verse'], ['definition', 'Definition'], ['factoid', 'Factoid']] as [key, label]}
                            <li class="pr-4">
                                <Input on:change={(ev) => { toggleJokeCategory(key, ev.detail); }} type="checkbox" value={selectedJoke.attributes.categories.indexOf(key) >= 0}>{label}</Input>
                            </li>
                        {/each}
                    </ul>
                    <label class="block mb-4 relative">
                        <span class="block mb-1 text-sm">Topics</span>
                        <ul class="flex flex-row flex-wrap w-full bg-gray-200 rounded-t px-4 py-3 text-sm">
                            {#each selectedJoke.attributes.topics as topic}
                                <li role="presentation" class="flex-none mr-4">
                                    <span>{topic}</span>
                                    <button on:click={() => { removeJokeTopic(topic); }} class="inline-block rounded-full bg-primary text-white" aria-label="Remove topic {topic}">
                                        <svg aria-hidden="true" viewBox="0 0 24 24" class="w-4 h-4">
                                            <path fill="currentColor" d="M20 6.91L17.09 4L12 9.09L6.91 4L4 6.91L9.09 12L4 17.09L6.91 20L12 14.91L17.09 20L20 17.09L14.91 12L20 6.91Z" />
                                        </svg>
                                    </button>
                                </li>
                            {/each}
                        </ul>
                        <input bind:this={newJokeTopicElement} bind:value={newJokeTopic} on:keyup={jokeTopicKeyup} class="block w-full bg-gray-200 rounded-b px-4 py-3 focus:outline-primary"/>
                        {#if newJokeTopicSuggestions.length > 0}
                            <ol class="absolute l-0 t-0 w-full shadow bg-white z-10 px-4 py-3">
                                {#each newJokeTopicSuggestions as suggestion}
                                    <li><button on:click={() => { addSuggestedTopic(suggestion.id); }} class="block w-full text-left text-accent hover:text-primary focus:text-primary py-1">{suggestion.id}</button></li>
                                {/each}
                            </ol>
                        {/if}
                    </label>
                    <Input on:change={(ev) => { selectedJoke.attributes.language = ev.detail; }} type="select" value={selectedJoke.attributes.language} values={[[null, 'Unknown'], ['en', 'English']]}>Language</Input>
                </div>
            {/if}
        </div>
    </div>
</div>
