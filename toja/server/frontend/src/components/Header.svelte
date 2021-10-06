<script lang="ts">
    import { Link } from 'svelte-navigator';

    import { breakpoint } from '../stores';
</script>

<header class="container mx-auto flex flex-col lg:flex-row mb-12">
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
                    <button class="block text-accent py-1">
                        <svg viewBox="0 0 24 24" class="w-6 h-6">
                            <path fill="currentColor" d="M3,6H21V8H3V6M3,11H21V13H3V11M3,16H21V18H3V16Z" />
                        </svg>
                    </button>
                </li>
            </ul>
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
