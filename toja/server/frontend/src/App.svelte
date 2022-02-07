<script lang="ts">
	import { Router } from "svelte-navigator";

	import { busy } from './stores';
	import Content from './Content.svelte';
</script>

<div class="bg-gray-900 p-vw-2 font-merriweather-regular">
	<div class="bg-white p-vw-8">
		<main class="md:border-brand pt-8">
			<Router basepath="/app">
				<Content/>
			</Router>
		</main>
	</div>
	{#if $busy}
		<div class="fixed top-0 left-0 w-screen h-screen cursor-wait z-50"></div>
	{/if}
</div>

<style global>
	@tailwind base;
	@tailwind components;
	@tailwind utilities;

	@layer utilities {
		.border-brand {
			border-image: url('/app/img/body-border-brand.svg') 5 75 75 fill stretch;
			border-width: 5px 75px 75px;
    		border-style: solid;
		}

		.flex-basis-full {
			flex-basis: 100%;
		}
	}

	html {
		@apply font-merriweather-regular;
		font-size: 11pt;
	}

	body {
		@apply bg-gray-900;
	}

	a {
		@apply rounded focus:outline-primary;
	}

	p {
		@apply mb-2;
	}
</style>
