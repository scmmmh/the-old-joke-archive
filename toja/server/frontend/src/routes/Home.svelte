<script lang="ts">
    import { Link } from 'svelte-navigator';
</script>

<article class="container mx-auto mb-12">
    <h1 class="sr-only">Welcome to The Old Joke Archive</h1>
    <div class="flex flex-row items-center md:px-8 mb-12">
        <div class="flex-none" role="presentation">
            <img src="/app/img/img-character-m.png" alt="" class="w-16 md:w-24 lg:w-40 xl:w-60"/>
        </div>
        <div class="md:flex-1"></div>
        <div class="flex-auto px-8 md:px-16 lg:px-24 xl:px-32 lg:text-lg xl:text-2xl">
            <p class="font-merriweather-bold">A Roundabout Role</p>
            <p>— A rigmarole.</p>
            <p class="text-right text-sm">— Funny Folks.</p>
        </div>
        <div class="md:flex-1"></div>
        <div class="flex-none" role="presentation">
            <img src="/app/img/img-character-f.png" alt="" class="w-16 md:w-24 lg:w-40 xl:w-60"/>
        </div>
    </div>
    <form class="mb-12 md:mx-20 lg:mx-28 xl:mx-auto xl:max-w-3xl">
        <h2 class="font-blackriver-bold text-lg lg:text-xl xl:text-2xl mb-4">Find Something Funny</h2>
        <label class="block relative w-full bg-gray-200 rounded-lg flex">
            <span class="sr-only">Search for jokes</span>
            <input type="search" name="q" class="flex-auto bg-gray-200 px-3 py-3 rounded-lg focus:outline-primary"/>
            <button aria-label="Search" class="px-3 text-accent rounded-lg focus:outline-primary">
                <svg viewBox="0 0 24 24" class="w-6 h-6">
                    <path fill="currentColor" d="M9.5,3A6.5,6.5 0 0,1 16,9.5C16,11.11 15.41,12.59 14.44,13.73L14.71,14H15.5L20.5,19L19,20.5L14,15.5V14.71L13.73,14.44C12.59,15.41 11.11,16 9.5,16A6.5,6.5 0 0,1 3,9.5A6.5,6.5 0 0,1 9.5,3M9.5,5C7,5 5,7 5,9.5C5,12 7,14 9.5,14C12,14 14,12 14,9.5C14,7 12,5 9.5,5Z" />
                </svg>
            </button>
        </label>
    </form>
    <div class="flex flex-row flex-wrap mb-12 lg:items-center">
        <div class="flex-auto w-full lg:w-1/2 mb-12 lg:mb-0 lg:pr-4">
            <h2 class="font-blackriver-bold text-lg lg:text-xl xl:text-2xl mb-2">The Old Joke Archive</h2>
            <p class="mb-2">When the 18-year-old Victoria came to the throne in 1837, victories over Revolutionary and Napoleonic France had increased Britain’s influence abroad. Queen Victoria ruled Britain for over 60 years. During this long reign, the country acquired unprecedented power and wealth.</p>
            <ul class="flex flex-row text-sm">
                <li role="presentation" class="flex-none pr-2 mr-2 border-solid border-r-px border-gray-400"><Link to="/about" class="text-accent hover:text-primary transition-colors hover:underline">Find out more</Link></li>
                <li role="presentation" class="flex-none"><Link to="/contribute" class="text-accent hover:text-primary transition-colors hover:underline">Contribute</Link></li>
            </ul>
        </div>
        <div class="flex-auto w-1/2 lg:w-1/4 px-2 text-center">
            <div class="text-primary text-6xl font-blackriver-bold">29</div>
            <div class="font-blackriver-bold md:text-lg">Jokes Archived</div>
        </div>
        <div class="flex-auto w-1/2 lg:w-1/4 pl-2 text-center">
            <div class="text-primary text-6xl font-blackriver-bold">10</div>
            <div class="font-blackriver-bold md:text-lg">Jokes Transcribed</div>
        </div>
    </div>
</article>
