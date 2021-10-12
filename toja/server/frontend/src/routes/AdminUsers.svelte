<script lang="ts">
    import { getJsonApiObjects } from '../stores';

    let users = [];

    getJsonApiObjects('users').then((new_users) => {
        users = new_users;
        console.log(users);
    });
</script>

<h2 class="sr-only">User Administration</h2>

<table class="w-full">
    <thead>
        <tr>
            <th class="italic text-left border-t-2 border-b-2 border-gray-400 py-2">E-Mail</th>
            <th class="italic text-left border-t-2 border-b-2 border-gray-400 py-2">Name</th>
            <th class="italic text-left border-t-2 border-b-2 border-gray-400 py-2">Groups</th>
            <th class="italic text-left border-t-2 border-b-2 border-gray-400 py-2">Status</th>
            <th class="italic text-left border-t-2 border-b-2 border-gray-400 py-2">Actions</th>
        </tr>
    </thead>
    <tbody>
        {#each users as user}
            <tr>
                <td class="text-left border-b border-accent py-4">{user.attributes.email}</td>
                <td class="text-left border-b border-accent py-4">{user.attributes.name}</td>
                <td class="text-left border-b border-accent py-4">{user.attributes.groups.join(', ')}</td>
                <td class="text-left border-b border-accent py-4"></td>
                <td class="text-left border-b border-accent py-4"></td>
            </tr>
        {/each}
    </tbody>
</table>
