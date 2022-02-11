<script lang="ts">
    import ImageEditor from '../../components/ImageEditor.svelte';
    import Loading from '../../components/Loading.svelte';
    import Button from '../../components/Button.svelte';
    import { yearFromDate, monthDayFromDate } from '../../util';
    import { getJsonApiObjects } from '../../stores';

    let sources = null as SourceDocument[];
    let selectedSource = null;

    async function loadSources() {
        sources = await getJsonApiObjects('sources') as SourceDocument[];
    }

    loadSources();
</script>

<div class="h-9/10-screen flex flex-col">
    <div class="flex-none flex flex-row">
        <h1 class="flex-1 font-blackriver-bold text-2xl md:text-3xl lg:text-4xl mb-8">Joke Workbench</h1>
        {#if selectedSource}
            <div class="flex-none">
                <Button on:action={() => { selectedSource = null; }} class="text-sm">&larr; Back to all sources</Button>
            </div>
        {/if}
    </div>
    {#if selectedSource}
        <div class="flex-1 flex flex-row overflow-hidden">
            <div class="w-1/3 h-full"><ImageEditor source={selectedSource}/></div>
            <div class="w-1/3"></div>
            <div class="w-1/3"></div>
        </div>
    {:else}
        <div class="flex-1 overflow-auto">
            {#if sources}
                <ul class="flex flex-row flex-wrap">
                    {#each sources as source}
                        <li class="flex-0 w-1/2">
                            <button on:click={() => { selectedSource = source; }} class="block w-full flex flex-row space-x-8 text-left">
                                <span class="block flex-none w-60 h-32 border border-gray-500 rounded-lg overflow-hidden">
                                    <img src={source.attributes.data} alt="" class="max-w-none"/>
                                </span>
                                <span class="block flex-1 font-merriweather-bold text-2xl md:text-3xl italic uppercase mb-2">{source.attributes.title}</span>
                                <time class="block flex-none block w-24">
                                    <p class="font-blackriver-bold text-2xl md:text-4xl text-center">{yearFromDate(source.attributes.date)}</p>
                                    {#if monthDayFromDate(source.attributes.date)}
                                        <p class="text-center">{monthDayFromDate(source.attributes.date)}</p>
                                    {/if}
                                </time>
                            </button>
                        </li>
                    {/each}
                </ul>
            {:else}
                <Loading/>
            {/if}
        </div>
    {/if}
</div>
