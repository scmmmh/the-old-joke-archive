import { writable } from "svelte/store";

function createBusy() {
	const { subscribe, set } = writable(false);
    let counter = 0;

	return {
		subscribe,
        startBusy: () => { counter++; set(true); },
        endBusy: () => { counter = Math.max(counter - 1, 0); set(counter > 0); },
	};
}

export const busy = createBusy();
