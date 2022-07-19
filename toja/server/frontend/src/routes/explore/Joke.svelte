<script lang="ts">
    import { onDestroy, tick } from 'svelte';
    import { useParams, Link } from 'svelte-navigator';

    import Busy from '../../components/Busy.svelte';

    import { getJsonApiObject, saveJsonApiObject, isAuthenticated } from '../../stores';
    import { formatText, titleCase, monthDayFromDate, yearFromDate } from '../../util';

    const JUDGEMENTS = [
        {
            name: 'lol',
            label: 'LOL',
        },
        {
            name: 'eye-roll',
            label: 'Eye-roll'
        },
        {
            name: 'confused',
            label: 'Confused'
        },
        {
            name: 'neutral',
            label: 'Neutral'
        },
    ];

    const params = useParams();
    let headingElement: HTMLElement;
    let loading = false;
    let joke = null;
    let source = null;
    let judgementBusy = null;

    const paramsUnsubscribe = params.subscribe(async (params) => {
        if ((joke === null || params.joke_id !== joke.id) && !loading) {
            loading = true;
            try {
                joke = await getJsonApiObject('jokes', params.joke_id);
                source = await getJsonApiObject('sources', joke.relationships.source.data.id);
                loading = false;
                await tick();
                if (headingElement) {
                    headingElement.focus();
                }
            } finally {
                loading = false;
            }
        }
    });

    function iconGroup(id: string): string {
        const components = id.split('-');
        const toggle = Number.parseInt(components[components.length - 1], 16) % 2;
        if (toggle === 0) {
            return 'a';
        } else {
            return 'b';
        }
    }

    async function judgeJoke(judgement: string) {
        if ($isAuthenticated) {
            const updatedJoke = {
                type: 'jokes',
                id: joke.id,
                attributes: {
                    actions: [
                        {toggleJudgement: judgement}
                    ],
                },
                relationships: joke.relationships
            };
            try {
                judgementBusy = judgement;
                joke = await saveJsonApiObject(updatedJoke) as JokeDocument;
            } finally {
                judgementBusy = null;
            }
        } else {
            alert('Please log in to judge a joke.')
        }
    }

    onDestroy(() => {
        paramsUnsubscribe();
    });
</script>

<div>
    {#if loading}
        <Busy/>
    {:else}
        <h1 bind:this={headingElement} class="font-blackriver-bold text-2xl md:text-3xl lg:text-4xl mb-8" tabindex="-1">{joke.attributes.title}</h1>
        <div class="lg:flex lg:flex-row">
            <div class="lg:w-2/3">
                <p>{@html formatText(joke.attributes.transcriptions.final)}</p>
                <div class="my-8 lg:my-16">
                    <img src={joke.attributes.data} alt=""/>
                </div>
                <h2 class="font-blackriver-bold text-xl mb-2">Contributors</h2>

            </div>
            <div class="lg:w-1/3 lg:pl-12">
                <h2 class="font-blackriver-bold text-xl mb-4 mt-8 lg:mt-0 lg:sr-only">Judge this Joke</h2>
                <ul class="flex flex-row space-x-8 mb-8">
                    {#each JUDGEMENTS as judgement}
                        <li role="presentation" class="relative">
                            <button on:click={() => {judgeJoke(judgement.name);}} class="transition-colors text-accent hover:text-primary focus:text-primary transition-opacity {judgementBusy === judgement.name ? 'opacity-50' : ''}">
                                <img src="/app/img/label/{iconGroup(joke.id)}/{judgement.name}.png" alt="" class="w-16 h-16"/>
                                <span class="block text-center mt-1 text-xl">{#if joke.attributes.judgements && joke.attributes.judgements[judgement.name]}{joke.attributes.judgements[judgement.name]}{:else}0{/if}</span>
                                <span class="block text-center text-sm">{judgement.label}</span>
                            </button>
                            {#if judgementBusy === judgement.name}
                                <div class="absolute left-1/2 top-1/2 transform -translate-x-1/2 -translate-y-1/2 z-10">
                                    <Busy message="Saving judgement..."/>
                                </div>
                            {/if}
                        </li>
                    {/each}
                </ul>
                <h2 class="font-blackriver-bold text-xl mb-4 lg:sr-only">Share this Joke</h2>
                <ul class="flex flex-row space-x-8 mb-8">
                    <li role="presentation">
                        <a href="https://twitter.com/intent/tweet?{joke.attributes.title ? 'text=' + encodeURIComponent(joke.attributes.title.substring()) : ''}&url={encodeURIComponent(window.location.href)}&via=oldjokearchive" target="_blank" class="transition-colors text-accent hover:text-primary focus:text-primary" rel="noopener" aria-label="Share on Twitter" title="Share on Twitter">
                            <svg aria-hidden="true" viewBox="0 0 24 24" class="w-16 h-16">
                                <path fill="currentColor" d="M22.46,6C21.69,6.35 20.86,6.58 20,6.69C20.88,6.16 21.56,5.32 21.88,4.31C21.05,4.81 20.13,5.16 19.16,5.36C18.37,4.5 17.26,4 16,4C13.65,4 11.73,5.92 11.73,8.29C11.73,8.63 11.77,8.96 11.84,9.27C8.28,9.09 5.11,7.38 3,4.79C2.63,5.42 2.42,6.16 2.42,6.94C2.42,8.43 3.17,9.75 4.33,10.5C3.62,10.5 2.96,10.3 2.38,10C2.38,10 2.38,10 2.38,10.03C2.38,12.11 3.86,13.85 5.82,14.24C5.46,14.34 5.08,14.39 4.69,14.39C4.42,14.39 4.15,14.36 3.89,14.31C4.43,16 6,17.26 7.89,17.29C6.43,18.45 4.58,19.13 2.56,19.13C2.22,19.13 1.88,19.11 1.54,19.07C3.44,20.29 5.7,21 8.12,21C16,21 20.33,14.46 20.33,8.79C20.33,8.6 20.33,8.42 20.32,8.23C21.16,7.63 21.88,6.87 22.46,6Z" />
                            </svg>
                        </a>
                    </li>
                    <li role="presentation">
                        <a href="https://www.facebook.com/sharer/sharer.php?u={encodeURIComponent(window.location.href)}" target="_blank" class="transition-colors text-accent hover:text-primary focus:text-primary" rel="noopener" aria-label="Share on Facebook" title="Share on Facebook">
                            <svg aria-hidden="true" viewBox="0 0 24 24" class="w-16 h-16">
                                <path fill="currentColor" d="M12 2.04C6.5 2.04 2 6.53 2 12.06C2 17.06 5.66 21.21 10.44 21.96V14.96H7.9V12.06H10.44V9.85C10.44 7.34 11.93 5.96 14.22 5.96C15.31 5.96 16.45 6.15 16.45 6.15V8.62H15.19C13.95 8.62 13.56 9.39 13.56 10.18V12.06H16.34L15.89 14.96H13.56V21.96A10 10 0 0 0 22 12.06C22 6.53 17.5 2.04 12 2.04Z" />
                            </svg>
                        </a>
                    </li>
                </ul>
                <h2 class="font-blackriver-bold text-xl mb-4">About this Joke</h2>
                <dl class="flex flex-row flex-wrap items-end">
                    <dt class="text-neutral-800 text-sm w-1/4 mb-2">Published in</dt>
                    <dd class="pl-2 w-3/4 mb-2">
                        <p class="mb-0"><Link to="/search?q=&publication={source.attributes.title}" class="transition-colors text-accent hover:text-primary focus:text-primary">{source.attributes.title}</Link></p>
                        {#if source.attributes.subtitle}
                            <p class="mt-2 mb-0"><Link to="/search?q=&section={source.attributes.subtitle}" class="transition-colors text-accent hover:text-primary focus:text-primary">{source.attributes.subtitle}</Link></p>
                        {/if}
                    </dd>
                    <dt class="text-neutral-800 text-sm w-1/4 mb-2">Publication type</dt>
                    <dd class="pl-2 w-3/4 mb-2">{titleCase(source.attributes.type)}</dd>
                    <dt class="text-neutral-800 text-sm w-1/4 mb-2">Publication date</dt>
                    <dd class="pl-2 w-3/4 mb-2">
                        {#if monthDayFromDate(source.attributes.date)}
                            {monthDayFromDate(source.attributes.date)}
                        {/if}
                        <Link to="/search?q=&year={yearFromDate(source.attributes.date)}" class="transition-colors text-accent hover:text-primary focus:text-primary">{yearFromDate(source.attributes.date)}</Link>
                    </dd>
                    {#if source.attributes.publisher}
                        <dt class="text-neutral-800 text-sm w-1/4 mb-2">Publisher</dt>
                        <dd class="pl-2 w-3/4 mb-2"><Link to="/search/?q=&publisher={source.attributes.publisher}" class="transition-colors text-accent hover:text-primary focus:text-primary">{titleCase(source.attributes.publisher)}</Link></dd>
                    {/if}
                    {#if source.attributes.location}
                        <dt class="text-neutral-800 text-sm w-1/4 mb-2">Location</dt>
                        <dd class="pl-2 w-3/4 mb-2">{titleCase(source.attributes.location)}</dd>
                    {/if}
                    {#if source.attributes.page_numbers}
                        <dt class="text-neutral-800 text-sm w-1/4 mb-2">Page</dt>
                        <dd class="pl-2 w-3/4 mb-2">{source.attributes.page_numbers}</dd>
                    {/if}
                </dl>
            </div>
        </div>
    {/if}
</div>
