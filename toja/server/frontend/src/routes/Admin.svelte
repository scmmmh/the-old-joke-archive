<script lang="ts">
    import { Route, Link, useLocation } from 'svelte-navigator';

    import { isGroupAdminUsers, isGroupAdmin } from '../stores';
    import AdminUsers from './admin/AdminUsers.svelte';
    import AdminSearch from './admin/AdminSearch.svelte';

    const location = useLocation();
</script>

<h1 class="font-blackriver-bold text-2xl md:text-3xl lg:text-4xl mb-8">Administrative Functions</h1>

<div class="flex flex-row">
    <nav class="flex-none w-full lg:w-auto">
        <ul>
            {#if $isGroupAdminUsers}
                <li role="presentation"><Link to="/admin/users" class="block px-3 py-2 hover:text-primary transition-colours {$location.pathname === '/admin/users' ? 'font-bold text-primary' : 'text-accent'}">User Administration</Link></li>
            {/if}
            {#if $isGroupAdmin}
                <li role="presentation"><Link to="/admin/search" class="block px-3 py-2 hover:text-primary transition-colours {$location.pathname === '/admin/search' ? 'font-bold text-primary' : 'text-accent'}">Search Administration</Link></li>
            {/if}
        </ul>
    </nav>
    <div class="flex-auto lg:ml-8">
        <Route path="/users"><AdminUsers/></Route>
        <Route path="/search"><AdminSearch/></Route>
    </div>
</div>
