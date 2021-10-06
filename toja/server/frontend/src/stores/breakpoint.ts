import { readable } from "svelte/store";

export const breakpoint = readable(0, (set) => {
    function resize() {
        const width = window.innerWidth;
        if (width < 640) {
            set(1);
        } else if (width < 768) {
            set(2);
        } else if (width < 1024) {
            set(3);
        } else if (width < 1280) {
            set(4);
        } else if (width < 1536) {
            set(5);
        } else {
            set(6);
        }
    }

    window.addEventListener('resize', resize);
    resize();

    return function() {
        window.removeEventListener('resize', resize);
    }
});
