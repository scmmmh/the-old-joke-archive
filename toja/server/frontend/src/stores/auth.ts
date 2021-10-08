import { writable, derived } from "svelte/store";

import { localLoadValue, sessionLoadValue, localDeleteValue, sessionDeleteValue, NestedStorage } from '../local-persistence';
import { getJsonApiObject } from './jsonapi';

export const authUser = writable(null as JsonApiObject);

export const authToken = writable('');

export const isAuthenticated = derived(authUser, (user) => {
    return user !== null;
});

export async function attemptAuthentication() {
    let auth = sessionLoadValue('auth', null) as NestedStorage;
    if (!auth) {
        auth = sessionLoadValue('auth', null) as NestedStorage;
    }
    if (auth) {
        authToken.set(auth.id + '$$' + auth.token);
        try {
            const user = await getJsonApiObject('users', auth.id as string);
            authUser.set(user);
        } catch {
            authToken.set('');
            authUser.set(null);
            localDeleteValue('auth');
            sessionDeleteValue('auth');
        }
    }
}

attemptAuthentication();
