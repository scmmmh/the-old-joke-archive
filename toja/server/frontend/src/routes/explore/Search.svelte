<script lang="ts">
    import { onDestroy, onMount } from 'svelte';
    import { get } from 'svelte/store';
    import { useParams } from 'svelte-navigator';
    import deepcopy from 'deepcopy';

    import { getCookie } from '../../stores/jsonapi';
    import { authToken } from '../../stores';
    import { titleCase, languageToHuman } from '../../util';

    import Busy from '../../components/Busy.svelte';
    import SearchResultEntry from '../../components/SearchResultEntry.svelte';

    const params = useParams();
    const FACETS = [
        {name: 'categories', label: 'Categories'},
        {name: 'topics', label: 'Topics'},
        {name: 'publisher', label: 'Publisher'},
        {name: 'publication', label: 'Publication'},
        {name: 'section', label: 'Chapter / Column'},
        {name: 'year', label: 'Year'},
        {name: 'language', label: 'Language', format: languageToHuman},
    ];
    const DEFAULT_QUERY = {
        query: '',
        facets: {
            'categories': {},
            'topics': {},
            'publication': {},
            'section': {},
            'year': {},
            'publisher': {},
            'language': {},
        }
    }
    let queryElement = null as HTMLInputElement;
    let searchCounter = 0;
    let debounceTimeout = 0;
    let exhaustiveTimeout = 0;
    let countsExhaustive = false;
    let results = [] as JokeDocument[];
    let resultFacets = {} as {[facet: string]: {[value: string]: number}};
    let query = deepcopy(DEFAULT_QUERY);
    let isActiveQuery = false;

    async function search() {
        if (searchCounter > 0) {
            clearTimeout(debounceTimeout);
            debounceTimeout = window.setTimeout(search, 80);
            return;
        }
        clearTimeout(exhaustiveTimeout);
        searchCounter = searchCounter + 1;
        isActiveQuery = query.query !== '';
        let queryString = ['q=' + encodeURIComponent(query.query)];
        for (const [facet, values] of Object.entries(query.facets)) {
            for (const [value, selected] of Object.entries(values)) {
                if (selected) {
                    queryString.push(facet + '=' + encodeURIComponent(value));
                    isActiveQuery = true;
                }
            }
        }
        let href = window.location.href;
        if (href.indexOf('?') >= 0) {
            href = href.substring(0, href.indexOf('?'));
        }
        window.history.replaceState(null, '', href + '?' + queryString.join('&'));
        const response = await window.fetch('/api/search', {
            method: 'POST',
            body: JSON.stringify(query),
            headers: {
                'Content-Type': 'application/json',
                'X-XSRFToken': getCookie('_xsrf'),
                'X-Toja-Auth': get(authToken)
            }
        });
        searchCounter = searchCounter - 1;
        if (response.status === 200) {
            const data = await response.json();
            results = data.data;
            resultFacets = data.meta.facets;
            query = query;
            countsExhaustive = data.meta.total < 50;
            exhaustiveTimeout = window.setTimeout(exhaustiveSearchCounts, 5000);
        }
    }

    async function exhaustiveSearchCounts() {
        const response = await window.fetch('/api/search/exhaustive-counts', {
            method: 'POST',
            body: JSON.stringify(query),
            headers: {
                'Content-Type': 'application/json',
                'X-XSRFToken': getCookie('_xsrf'),
                'X-Toja-Auth': get(authToken)
            }
        });
        if (response.status === 200) {
            const data = await response.json();
            resultFacets = data.meta.facets;
            countsExhaustive = true;
        }
    }

    function requestSearch() {
        if (queryElement) {
            query.query = queryElement.value;
        }
        clearTimeout(debounceTimeout);
        debounceTimeout = window.setTimeout(search, 80);
    }

    function sortedFacets(facet: {[value: string]: number}): {value: String, count: number}[] {
        const items = Object.entries(facet);
        items.sort(([valueA, countA], [valueB, countB]) => {
            return countB[1] - countA[1];
        })
        return items.map(([value, count]) => {
            return {value: value, count: count};
        }).slice(0, 10);
    }

    function extractParams() {
        for (const [name, value] of new URLSearchParams(window.location.search)) {
            if (name === 'q') {
                query.query = value;
                if (queryElement) {
                    queryElement.value = value;
                }
            } else {
                if (query.facets[name] !== undefined) {
                    query.facets[name][value] = true;
                }
            }
        }
        search();
    }

    const paramsUnsubscribe = params.subscribe(extractParams);

    onMount(extractParams);

    onDestroy(paramsUnsubscribe);
</script>

<div class="flex flex-row">
    <div class="flex-none md:w-1/3 lg:w-1/4 md:order-2">
        <div class="flex flex-row items-top mb-8">
            <h1 class="flex-1 font-blackriver-bold text-2xl">Find something funny</h1>
            {#if isActiveQuery}
                <button on:click={() => { query = deepcopy(DEFAULT_QUERY); queryElement.value = ''; search(); }} class="block flex-none relative -top-2 text-accent p-2 text-sm" aria-label="Clear your search" title="Clear your search">
                    <svg viewBox="0 0 24 24" class="w-6 h-6">
                        <path fill="currentColor" d="M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20M12,2C6.47,2 2,6.47 2,12C2,17.53 6.47,22 12,22C17.53,22 22,17.53 22,12C22,6.47 17.53,2 12,2M14.59,8L12,10.59L9.41,8L8,9.41L10.59,12L8,14.59L9.41,16L12,13.41L14.59,16L16,14.59L13.41,12L16,9.41L14.59,8Z" />
                    </svg>
                </button>
            {/if}
        </div>
        <label class="block relative mb-8">
            <span class="sr-only">Search for</span>
            <input bind:this={queryElement} type="search" class="block w-full bg-gray-200 rounded px-4 py-3 focus:outline-primary" on:keyup={requestSearch}/>
        </label>
        {#if searchCounter > 0}
            <span class="absolute right-2 top-1/2 transform -translate-y-1/2 text-neutral-600">
                <Busy message="Searching..."/>
            </span>
        {/if}
        {#each FACETS as facetDef}
            <section class="mb-8">
                <h2 class="font-blackriver-bold text-xl mb-2">{facetDef.label}</h2>
                {#if resultFacets[facetDef.name]}
                    <ol>
                        {#each sortedFacets(resultFacets[facetDef.name]) as facet}
                            <li>
                                <label class="flex flex-row cursor-pointer {query.facets[facetDef.name][facet.value] ? 'text-primary' : 'text-accent'} py-1" tabindex="0" on:keyup={(ev) => {if (ev.key === 'Enter') {ev.target.click();} }}>
                                    <input type="checkbox" class="sr-only" tabindex="-1" bind:checked={query.facets[facetDef.name][facet.value]} on:change={requestSearch} />
                                    <span class="flex-1">{#if facetDef.format}{facetDef.format(facet.value)}{:else}{titleCase(facet.value)}{/if}</span>
                                    <span class="flex-none">{#if !countsExhaustive}~{/if}{facet.count}</span>
                                </label>
                            </li>
                        {/each}
                    </ol>
                {/if}
            </section>
        {/each}
    </div>
    <div class="flex-1 md:order-1 md:mr-12">
        {#if results.length > 0}
            <h2 class="font-blackriver-bold text-4xl mb-8">
                {#if queryElement.value}
                    Jokes containing <span class="text-primary">{query.query}</span>
                {:else}
                    All Jokes
                {/if}
            </h2>
            <ul>
                {#each results as joke}
                    <SearchResultEntry joke={joke}/>
                {/each}
            </ul>
        {:else if searchCounter > 0}
            <p>The amazing search automaton is looking for something funny.</p>
        {:else}
            <p>Unfortunately the amazing search automaton couldn't find anything funny for that search.</p>
        {/if}
    </div>
</div>
