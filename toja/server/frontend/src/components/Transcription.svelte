<script lang="ts">
    import { getJsonApiObjects } from '../stores';

    export let source: SourceDocument;

    let selectedJoke: JokeDocument;

    let jokes = [];

    async function loadJokes(source: SourceDocument) {
        const jokeIds = source.relationships.jokes.data.map((rel) => {
                return rel.id;
            })
            jokes = await getJsonApiObjects('jokes', 'filter[id]=' + jokeIds.join(',')) as JokeDocument[];
    }

    $: {
        loadJokes(source);
    }

    function selectJoke(joke: JokeDocument) {
        selectedJoke = joke;
    }
</script>

<div class="flex flex-col h-full overflow-hidden">
    <nav class="flex-none">
    </nav>
    <div class="flex-1 flex flex-row space-x-4">
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
        <div class="flex-1 bg-primary">
        </div>
    </div>
</div>