<script lang="ts">
	import { Router } from "svelte-navigator";

	import { busy } from "./stores";
	import Content from "./Content.svelte";
</script>

<div class="bg-gray-900 p-vw-2 font-merriweather-regular">
	<div class="bg-white p-vw-8">
		<main class="md:border-brand pt-8">
			<Router basepath="/app">
				<Content />
			</Router>
		</main>
	</div>
	{#if $busy}
		<div class="fixed top-0 left-0 w-screen h-screen cursor-wait z-50" />
	{/if}
</div>
