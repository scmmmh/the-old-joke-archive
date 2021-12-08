<script lang="ts">
	import { Route, useLocation } from "svelte-navigator";
    import { tick, onDestroy } from "svelte";

    import { isGroupAdminUsers } from './stores';
    import Header from './components/Header.svelte';
    import Footer from './components/Footer.svelte';
    import Home from './routes/Home.svelte';
    import Signup from './routes/user/Signup.svelte';
    import Login from './routes/user/Login.svelte';
    import ResetPassword from './routes/user/ResetPassword.svelte';
    import Confirm from './routes/user/Confirm.svelte';
    import Contribute from "./routes/contribute/Contribute.svelte";

    let Admin = null;
    const location = useLocation();
    const unsubscribeLocation = location.subscribe((location) => {
        if (location.pathname.startsWith('/admin')) {
            if (Admin === null) {
                import('./routes/Admin.svelte').then((mod) => {
                    Admin = mod.default;
                    tick().then(() => {
                        const elem = document.querySelector('h1');
                        if (elem) {
                            elem.focus();
                        }
                    });
                });
            }
        }
    });

    onDestroy(unsubscribeLocation);
</script>

<Header/>
<article class="container mx-auto mb-12">
    <Route path="/"><Home/></Route>
    <Route path="/user/sign-up"><Signup/></Route>
    <Route path="/user/confirm"><Confirm/></Route>
    <Route path="/user/log-in"><Login/></Route>
    <Route path="/user/reset-password"><ResetPassword/></Route>
    {#if $isGroupAdminUsers}
        <Route path="/admin/*"><svelte:component this={Admin}/></Route>
    {/if}
    <Route path="/contribute"><Contribute/></Route>
</article>
<Footer/>
