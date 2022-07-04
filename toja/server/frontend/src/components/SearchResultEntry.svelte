<script lang="ts">
    import { Link } from 'svelte-navigator';

    import { formatText, titleCase } from '../util';

    import ImagePopup from './ImagePopup.svelte';

    export let joke: JokeDocument;
    let showPopup = false;
</script>

{#if joke}
    <li class="flex flex-row mb-12">
        <div class="flex-none mr-8">
            <div class="w-60 h-32 border border-gray-500 rounded-lg overflow-hidden">
                <button on:click={() => { showPopup = true; }} aria-label="Show a popup with the source in full size">
                    <img src={joke.attributes.data} alt="" class="max-w-none"/>
                </button>
            </div>
        </div>
        <div class="flex-1">
            <h3 class="font-blackriver-bold text-2xl mb-2"><Link to="/jokes/{joke.id}" class="text-accent">{joke.attributes.title}</Link></h3>
            <p>{@html formatText(joke.attributes.transcriptions.final)}</p>
            {#if joke.attributes.categories}
                <ul class="flex flex-row flex-wrap space-x-4 items-center">
                    <li role="presentation" class="font-bold text-sm">Categories:</li>
                    {#each joke.attributes.categories as category}
                        <li role="presentation"><Link to="/search?categories={category}" class="text-accent text-sm">{titleCase(category)}</Link></li>
                    {/each}
                </ul>
            {/if}
            {#if joke.attributes.topics}
                <ul class="flex flex-row flex-wrap space-x-4 items-center">
                    <li role="presentation" class="font-bold text-sm">Topics:</li>
                    {#each joke.attributes.topics as topic}
                        <li><Link to="/search?topics={topic}" class="text-accent text-sm">{titleCase(topic)}</Link></li>
                    {/each}
                </ul>
            {/if}
        </div>
        {#if showPopup}
            <ImagePopup imageUrl={joke.attributes.data} on:close={() => { showPopup = false; }}/>
        {/if}
    </li>
{/if}
