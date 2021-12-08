<script lang="ts">
    import Input from '../../components/Input.svelte';
    import Button from '../../components/Button.svelte';
</script>

<h1 class="font-blackriver-bold text-2xl md:text-3xl lg:text-4xl mb-8">Sources</h1>

<div class="flex flex-row space-x-16">
    <ul class="flex-auto">
        <li class="flex flex-row space-x-8">
            <div class="flex-none">
                <div class="w-60 h-32 border border-black rounded-lg"></div>
            </div>
            <div class="flex-auto">
                <h2 class="font-merriweather-bold text-2xl md:text-3xl italic uppercase mb-2">The Big Book of Bad Jokes</h2>
                <p>Nothing as bad as a bad laugh</p>
                <p>Groan Publishing. London, UK</p>
            </div>
            <div class="flex-none">
                <p class="font-blackriver-bold text-2xl md:text-4xl text-center">1860</p>
                <p class="text-center">June</p>
            </div>
            <ul class="flex-none flex flex-row self-end">
                <li role="presentation" class="px-4 mr-4 border-r border-solid border-gray-300">
                    <button aria-label="Edit this source">
                        <svg viewBox="0 0 24 24" class="w-6 h-6 text-accent hover:text-primary transition-colors">
                            <path fill="currentColor" d="M20.71,7.04C21.1,6.65 21.1,6 20.71,5.63L18.37,3.29C18,2.9 17.35,2.9 16.96,3.29L15.12,5.12L18.87,8.87M3,17.25V21H6.75L17.81,9.93L14.06,6.18L3,17.25Z" />
                        </svg>
                    </button>
                </li>
                <li role="presentation">
                    <button aria-label="Delete this source">
                        <svg viewBox="0 0 24 24" class="w-6 h-6 text-accent hover:text-primary transition-colors">
                            <path fill="currentColor" d="M19,4H15.5L14.5,3H9.5L8.5,4H5V6H19M6,19A2,2 0 0,0 8,21H16A2,2 0 0,0 18,19V7H6V19Z" />
                        </svg>
                    </button>
                </li>
            </ul>
    </li>
    </ul>
    <form class="flex-none w-1/3">
        <h2 class="font-blackriver-bold text-2xl md:text-3xl mb-2">Contribute a source</h2>
        <Input type="select" value="" values={[['book', 'Book'], ['newspaper', 'Newspaper']]}>Publication Type</Input>
        <Input value="">Publication Title</Input>
        <Input value="">Column / Chapter Title</Input>
        <Input value="">Publication Date (YYYY, YYYY-MM, YYYY-MM-DD)</Input>
        <Input value="">Publisher</Input>
        <Input value="">Publication Location</Input>
        <Input value="">Page Numbers</Input>
        <Input type="file" value="">Source Image</Input>
        <Input type="checkbox" value="">Please confirm that you are permitted to upload this source image under a CC-BY-4.0
            license. For more details on the license, please use the Copyright questions link in the page's footer.</Input>
        <div class="text-right">
            <Button>Add source</Button>
        </div>
    </form>
</div>
