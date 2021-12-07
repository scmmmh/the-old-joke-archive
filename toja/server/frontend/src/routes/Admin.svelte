<script lang="ts">
    import { Route, Link, useLocation } from 'svelte-navigator';

    import { isGroupAdminUsers } from '../stores';
    import AdminUsers from './admin/AdminUsers.svelte';

    const location = useLocation();
</script>

<h1 class="font-blackriver-bold text-4xl mb-8">Administrative Functions</h1>

<div class="flex flex-row">
    <nav class="flex-none w-full lg:w-auto">
        <ul>
            {#if $isGroupAdminUsers}
                <li role="presentation"><Link to="/admin/users" class="block px-3 py-2 text-accent hover:text-primary transition-colours {$location.pathname === '/admin/users' ? 'font-bold' : ''}">User Administration</Link></li>
            {/if}
        </ul>
    </nav>
    <div class="flex-auto lg:ml-8">
        <Route path="/users"><AdminUsers/></Route>
    </div>
</div>
