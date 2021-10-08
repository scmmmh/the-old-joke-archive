import { derived } from 'svelte/store';

import { authUser } from './auth';

export const isGroupAdmin = derived(authUser, (authUser) => {
    if (authUser && (authUser.attributes.groups as string[]).indexOf('admin') >= 0) {
        return true;
    }
    return false;
});

export const isGroupAdminUsers = derived([authUser, isGroupAdmin], ([authUser, isGroupAdmin]) => {
    if (isGroupAdmin) {
        return true;
    }
    if (authUser && (authUser.attributes.groups as string[]).indexOf('admin:users') >= 0) {
        return true;
    }
    return false;
});
