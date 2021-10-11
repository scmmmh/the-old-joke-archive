<script lang="ts">
	import { Route, useLocation } from "svelte-navigator";
    import { onDestroy } from "svelte";

    import Header from './components/Header.svelte';
    import Footer from './components/Footer.svelte';
    import Home from './routes/Home.svelte';
    import Signup from './routes/Signup.svelte';
    import Login from './routes/Login.svelte';

    let Admin;
    const location = useLocation();
    const unsubscribeLocation = location.subscribe((location) => {
        if (location.pathname === '/admin') {
            import('./routes/Admin.svelte').then((mod) => {
                Admin = mod.default;
            })
        }
    });

    onDestroy(unsubscribeLocation);
</script>

<Header/>
<Route path="/"><Home/></Route>
<Route path="/user/sign-up"><Signup/></Route>
<Route path="/user/log-in"><Login/></Route>
<Route path="/admin"><svelte:component this={Admin}/></Route>
<Footer/>
