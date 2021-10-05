<script lang="ts">
	import { Router } from "svelte-navigator";

	import Header from './components/Header.svelte';
</script>

<div class="bg-gray-900 p-vw-2">
	<div class="bg-white p-vw-8">
		<main class="md:border-brand pt-8">
			<Router>
				<Header/>
			</Router>
		</main>
	</div>
</div>

<style global>
	@font-face {
    	font-family: 'blackriver-bold';
    	src: url('/app/fonts/blackriver-bold.woff2') format('woff2'),
			 url('/app/fonts/blackriver-bold.woff') format('woff'),
			 url('/app/fonts/blackriver-bold.ttf') format('ttf');
    	font-weight: normal;
    	font-style: normal;
    	font-display: swap;
	}

	@tailwind base;
	@tailwind components;
	@tailwind utilities;

	@layer utilities {
		@variants responsive {
			.border-brand {
			    border-image: url('/app/img/body-border-brand.svg') 5 75 75 fill stretch;
    			border-width: 5px 75px 75px;
    			border-style: solid;
			}
		}
	}

	body {
		@apply bg-gray-900;
	}
</style>
