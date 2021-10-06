<script lang="ts">
	import { Router, Route } from "svelte-navigator";

	import Header from './components/Header.svelte';
	import Footer from './components/Footer.svelte';
	import Home from './routes/Home.svelte';
</script>

<div class="bg-gray-900 p-vw-2 font-merriweather-regular">
	<div class="bg-white p-vw-8">
		<main class="md:border-brand pt-8">
			<Router basepath="/app">
				<Header/>
				<Route path="/"><Home/></Route>
				<Footer/>
			</Router>
		</main>
	</div>
</div>

<style global>
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

			.flex-basis-full {
				flex-basis: 100%;
			}
		}
	}

	html {
		@apply font-merriweather-regular;
		font-size: 11pt;
	}

	body {
		@apply bg-gray-900;
	}
</style>
