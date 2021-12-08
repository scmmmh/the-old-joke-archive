<script lang="ts">
    import { Link } from 'svelte-navigator';

    import { isAuthenticated, authUser, isGroupEditor, isGroupDataProvider } from '../../stores';
</script>

<h1 class="font-blackriver-bold text-2xl md:text-3xl lg:text-4xl mb-8">Contribute to <span class="text-primary">The Old Joke Archive</span></h1>

<div class="max-w-5xl mb-8">
    <p>The archive's content relies on your contributions and its full scale cannot be achieved without you.</p>
    <p>We have a number of different ways in which you can contribute. Whether you just want to do something simple quickly, or if you want to
        get really involved in a difficult task, there is something for you.</p>
</div>

<div class="flex flex-col lg:flex-row">
    <div class="flex-auto lg:pr-4">
        <h2 class="font-merriweather-bold-italic text-xl md:text-2xl lg:text-3xl mb-4">Available Tasks</h2>
        <ul class="flex flex-col md:flex-row md:flex-wrap">
            {#if $isGroupEditor}
                <li class="md:w-1/2 xl:w-1/3 md:pr-8 md:pb-8">
                    <h2 class="font-merriweather-bold text-lg"><Link to="/contribute/workbench" class="text-accent">Workbench</Link></h2>
                    <p>The workbench allows you to undertake the complete find, transcribe, annotate workflow in a single, integrated interface.</p>
                    <div class="flex flex-row">
                        <span class="inline-block px-3 py-1 border border-primary rounded-lg text-sm">Medium - Long</span>
                        <span class="flex-auto"></span>
                        <Link to="/contribute/workbench" class="inline-block px-3 py-1 text-accent">Start &rarr;</Link>
                    </div>
                </li>
            {/if}
            {#if $isGroupDataProvider}
                <li class="md:w-1/2 xl:w-1/3 md:pr-8 md:pb-8">
                    <h2 class="font-merriweather-bold text-lg"><Link to="/contribute/data" class="text-accent">Provide Data</Link></h2>
                    <p>Provide source data for the archive. This involves uploading the source image data and providing appropriate metadata.</p>
                    <div class="flex flex-row">
                        <span class="inline-block px-3 py-1 border border-primary rounded-lg text-sm">Medium</span>
                        <span class="flex-auto"></span>
                        <Link to="/contribute/workbench" class="inline-block px-3 py-1 text-accent">Start &rarr;</Link>
                    </div>
                </li>
            {/if}
            <li class="md:w-1/2 xl:w-1/3 md:pr-8 md:pb-8">
                <h2 class="font-merriweather-bold text-lg">Find Jokes</h2>
                <p>Our source data often mixes jokes with other text or contains multiple jokes in a single image. In this task you will find jokes and mark
                    them out using a simple graphical tool.</p>
                <div>
                    <span class="inline-block px-3 py-1 border border-primary rounded-lg text-sm">Short</span>
                </div>
            </li>
            <li class="md:w-1/2 xl:w-1/3 md:pr-8 md:pb-8">
                <h2 class="font-merriweather-bold text-lg">Verify Jokes</h2>
                <p>The extraction of the jokes from the source data needs to be verified. In this task we will provide you with a simple tool to quickly
                    check that individual jokes have been extracted correctly.</p>
                <div>
                    <span class="inline-block px-3 py-1 border border-primary rounded-lg text-sm">Short</span>
                </div>
            </li>
            <li class="md:w-1/2 xl:w-1/3 md:pr-8 md:pb-8">
                <h2 class="font-merriweather-bold text-lg">Transcribe Jokes</h2>
                <p>The verified jokes are automatically processed and the text extracted and are then made available in this task for error correction or
                    manual transcription. How much work is needed depends on the quality of the source data and ranges from fixing a typo here or there to
                    manual transcription of the whole text.</p>
                <div>
                    <span class="inline-block px-3 py-1 border border-primary rounded-lg text-sm">Short - Medium</span>
                </div>
            </li>
            <li class="md:w-1/2 xl:w-1/3 md:pr-8 md:pb-8">
                <h2 class="font-merriweather-bold text-lg">Check Joke Categorisation</h2>
                <p>The transcribed jokes are automatically categorised, but this needs to be verified. In this task you are provided with a simple tool to
                    verify the automatic categorisation and add additional categorisations.</p>
                <div>
                    <span class="inline-block px-3 py-1 border border-primary rounded-lg text-sm">Short</span>
                </div>
            </li>
            <li class="md:w-1/2 xl:w-1/3 md:pr-8 md:pb-8">
                <h2 class="font-merriweather-bold text-lg">Annotate Jokes</h2>
                <p>To power the advanced functionality of the Old Joke Archive, we need to identify elements of the text such as speakers, people, places,
                    objects, and so on. In this task you are provided with a powerful tool to quickly annotate the joke text.</p>
                <div>
                    <span class="inline-block px-3 py-1 border border-primary rounded-lg text-sm">Short - Long</span>
                </div>
            </li>
        </ul>
    </div>
    <div class="flex-none lg:w-1/3 lg:pl-4">
        <h2 class="font-merriweather-bold-italic text-xl md:text-2xl lg:text-3xl mb-4">Attribution & Licensing</h2>
        {#if $isAuthenticated}
            <p>All the work you do for the project is attributed to {$authUser.attributes.name} ({$authUser.attributes.email}).</p>
        {:else}
            <p>All the work you do for the project is fully attributed to you. As a result, we require that you <Link to="/user/sign-up" class="text-accent">register</Link> or
                <Link to="/user/log-in" class="text-accent">log in</Link>.</p>
        {/if}
        <p>All the data you provide when undertaking tasks for the project are licensed under the
            <a href="https://creativecommons.org/licenses/by/4.0" class="text-accent">Creative Commons Attribution 4.0 license</a>. This basically
            means that the project and anybody else is free to use the data you provide however they see fit, as long as they abide by the license by
            attributing your contributions.</p>
    </div>
</div>
