<script lang="ts">
    import { tick } from 'svelte';
    import { Link } from 'svelte-navigator';

    import { breakpoint } from '../stores';

    let menuVisible = false;
    let popupList = null;
    let showMenuButton = null;

    async function showMenu() {
        menuVisible = true;
        await tick();
        if (popupList) {
            popupList.querySelector('a').focus();
        }
    }

    async function hideMenu() {
        menuVisible = false;
        await tick();
        if (showMenuButton) {
            showMenuButton.focus();
        }
    }

    function popupKeyUp(ev: KeyboardEvent) {
        if (ev.key === 'Escape') {
            hideMenu();
        }
    }
</script>

<header class="container mx-auto flex flex-col lg:flex-row mb-8">
    <div class="flex-none pb-6 lg:pb-0">
        <Link to="/" class="block font-blackriver-bold font-bold text-primary text-4xl whitespace-nowrap text-center md:text-left">The Old Joke Archive</Link>
        <span class="block font-blackriver-bold font-bold text-gray-500 text-2xl text-center md:text-left md:pl-8">Are we amused?</span>
    </div>
    <div class="flex-none lg:flex-1"></div>
    <nav class="relative">
        {#if $breakpoint <= 1}
            <ul class="flex flex-row">
                <li class="flex-none" role="presentation"><Link to="/search" class="block px-8 py-1 font-blackriver-bold text-accent text-center">Search</Link></li>
                <li class="flex-none" role="presentation"><Link to="/contribute" class="block px-8 py-1 font-blackriver-bold text-accent text-center">Contribute</Link></li>
                <li class="flex-1" role="presentation"></li>
                <li class="flex-none" role="presentation">
                    <button bind:this={showMenuButton} on:click={showMenu} class="block text-accent py-1 rounded focus:outline-primary" aria-label="Show the full menu">
                        <svg viewBox="0 0 24 24" class="w-6 h-6">
                            <path fill="currentColor" d="M3,6H21V8H3V6M3,11H21V13H3V11M3,16H21V18H3V16Z" />
                        </svg>
                    </button>
                </li>
            </ul>
            {#if menuVisible}
                <div on:keyup={popupKeyUp} class="absolute left-0 top-0 w-full flex flex-row bg-white z-1 shadow-md">
                    <ul bind:this={popupList} class="flex-auto">
                        <li role="presentation"><Link to="/search" class="block px-8 py-2 font-blackriver-bold text-accent">Search</Link></li>
                        <li role="presentation"><Link to="/contribute" class="block px-8 py-2 font-blackriver-bold text-accent">Contribute</Link></li>
                        <li role="presentation"><Link to="/about" class="block px-8 py-2 font-blackriver-bold text-accent">About</Link></li>
                        <li role="presentation"><Link to="/user/sign-up" class="block px-8 py-2 font-blackriver-bold text-accent">Sign Up</Link></li>
                        <li role="presentation"><Link to="/user/log-in" class="block px-8 py-2 font-blackriver-bold text-accent">Log in</Link></li>
                    </ul>
                    <div>
                        <button on:click={hideMenu} class="block text-accent py-1 rounded focus:outline-primary" aria-label="Hide the full menu">
                            <svg viewBox="0 0 24 24" class="w-6 h-6">
                                <path fill="currentColor" d="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z" />
                            </svg>
                        </button>
                    </div>
                </div>
            {/if}
        {:else if $breakpoint <= 3}
            <ul class="flex flex-row">
                <li class="flex-none" role="presentation"><Link to="/search" class="block px-8 py-1 font-blackriver-bold text-accent text-center">Search</Link></li>
                <li class="flex-none" role="presentation"><Link to="/contribute" class="block px-8 py-1 font-blackriver-bold text-accent text-center">Contribute</Link></li>
                <li class="flex-none" role="presentation"><Link to="/about" class="block px-8 py-1 font-blackriver-bold text-accent text-center">About</Link></li>
                <li class="flex-1" role="presentation"></li>
                <li class="flex-none" role="presentation"><Link to="/user/sign-up" class="block px-8 py-1 font-blackriver-bold text-accent text-center">Sign Up</Link></li>
                <li class="flex-none" role="presentation"><Link to="/user/log-in" class="block px-8 py-1 font-blackriver-bold text-accent text-center">Log in</Link></li>
            </ul>
        {:else if $breakpoint === 4}
            <ul class="flex flex-row flex-wrap">
                <li class="flex-auto" role="presentation"></li>
                <li class="flex-none" role="presentation"><Link to="/user/sign-up" class="block px-8 py-1 font-blackriver-bold text-accent text-center">Sign Up</Link></li>
                <li class="flex-none" role="presentation"><Link to="/user/log-in" class="block px-8 py-1 font-blackriver-bold text-accent text-center">Log in</Link></li>
                <li class="flex-1 flex-basis-full" role="presentation"></li>
                <li class="flex-auto w-px" role="presentation"></li>
                <li class="flex-none" role="presentation"><Link to="/search" class="block px-8 py-1 font-blackriver-bold text-accent text-center">Search</Link></li>
                <li class="flex-none" role="presentation"><Link to="/contribute" class="block px-8 py-1 font-blackriver-bold text-accent text-center">Contribute</Link></li>
                <li class="flex-none" role="presentation"><Link to="/about" class="block px-8 py-1 font-blackriver-bold text-accent text-center">About</Link></li>
            </ul>
        {:else}
            <ul class="flex flex-row flex-wrap">
                <li class="flex-none" role="presentation"><Link to="/search" class="block px-8 py-1 font-blackriver-bold text-accent text-center">Search</Link></li>
                <li class="flex-none" role="presentation"><Link to="/contribute" class="block px-8 py-1 font-blackriver-bold text-accent text-center">Contribute</Link></li>
                <li class="flex-none" role="presentation"><Link to="/about" class="block px-8 py-1 font-blackriver-bold text-accent text-center">About</Link></li>
                <li class="flex-1 w-20" role="presentation"></li>
                <li class="flex-none" role="presentation"><Link to="/user/sign-up" class="block px-8 py-1 font-blackriver-bold text-accent text-center">Sign Up</Link></li>
                <li class="flex-none" role="presentation"><Link to="/user/log-in" class="block px-8 py-1 font-blackriver-bold text-accent text-center">Log in</Link></li>
            </ul>
        {/if}
        <div role="presentation">
            <img src="/app/img/element-hr.svg" alt="" class="w-full"/>
        </div>
    </nav>
</header>
