<script lang="ts">
	import { Router, Route } from "svelte-navigator";

	import { busy } from './stores';
	import Header from './components/Header.svelte';
	import Footer from './components/Footer.svelte';
	import Home from './routes/Home.svelte';
	import Signup from './routes/Signup.svelte';
	import Login from './routes/Login.svelte';
</script>

<div class="bg-gray-900 p-vw-2 font-merriweather-regular">
	<div class="bg-white p-vw-8">
		<main class="md:border-brand pt-8">
			<Router basepath="/app">
				<Header/>
				<Route path="/"><Home/></Route>
				<Route path="/user/sign-up"><Signup/></Route>
				<Route path="/user/log-in"><Login/></Route>
				<Footer/>
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

	a {
		@apply rounded focus:outline-primary;
	}
</style>
