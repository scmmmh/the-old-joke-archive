import { writable, derived } from "svelte/store";

export const authUser = writable(null as JsonApiObject);

export const authToken = writable('');

export const isAuthenticated = derived(authUser, (user) => {
    return user !== null;
});
