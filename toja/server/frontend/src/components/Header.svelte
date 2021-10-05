<script lang="ts">
    import { Link } from 'svelte-navigator';
</script>

<header class="container mx-auto flex flex-col lg:flex-row">
    <div class="flex-0 pb-6 lg:pb-0">
        <span class="block font-blackriver-bold font-bold text-primary text-4xl whitespace-nowrap text-center md:text-left">The Old Joke Archive</span>
        <span class="block font-blackriver-bold font-bold text-gray-500 text-2xl lg:text-right pl-16 md:pl-8 lg:pl-0 lg:pr-8">Are we amused?</span>
    </div>
    <div class="flex-0 lg:flex-1"></div>
    <nav>
        <ul class="flex flex-row flex-wrap lg:flex-no-wrap">
            <li class="flex-0 lg:w-1/3 xl:w-auto md:border-solid md:border-r-px md:border-gray-400" role="presentation"><Link to="/search" class="block px-8 py-1 font-blackriver-bold text-accent text-center">Search</Link></li>
            <li class="flex-0 lg:w-1/3 xl:w-auto md:border-solid md:border-r-px md:border-gray-400" role="presentation"><Link to="/contribute" class="block px-8 py-1 font-blackriver-bold text-accent text-center">Contribute</Link></li>
            <li class="flex-0 lg:w-1/3 xl:w-auto" role="presentation"><Link to="/about" class="block px-8 py-1 font-blackriver-bold text-accent text-center">About</Link></li>
            <li class="flex-1 lg:w-1/3 xl:w-auto" role="presentation"></li>
            <li class="flex-0 lg:w-1/3 xl:w-auto md:border-solid md:border-r-px md:border-gray-400" role="presentation"><Link to="/contribute" class="block px-8 py-1 font-blackriver-bold text-accent text-center">Sign Up</Link></li>
            <li class="flex-0 lg:w-1/3 xl:w-auto" role="presentation"><Link to="/about" class="block px-8 py-1 font-blackriver-bold text-accent text-center">Log in</Link></li>
        </ul>
        <div role="presentation">
            <img src="/app/img/element-hr.svg" alt="" class="w-full"/>
        </div>
    </nav>
</header>
