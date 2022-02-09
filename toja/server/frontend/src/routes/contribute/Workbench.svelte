<script lang="ts">
    import ImageEditor from '../../components/ImageEditor.svelte';
</script>

<div class="h-9/10-screen flex flex-col">
    <h1 class="flex-0 font-blackriver-bold text-2xl md:text-3xl lg:text-4xl mb-8">Joke Workbench</h1>
    <div class="flex-1 flex flex-row overflow-hidden">
        <div class="w-1/3 h-full"><ImageEditor/></div>
        <div class="w-1/3"></div>
        <div class="w-1/3"></div>
    </div>
</div>
