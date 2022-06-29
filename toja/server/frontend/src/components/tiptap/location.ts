import { Mark, mergeAttributes } from '@tiptap/core';

export const LocationMark = Mark.create({
    name: 'LocationMark',

    renderHTML({ HTMLAttributes }) {
        return ['span', mergeAttributes(HTMLAttributes, { 'type': 'LocationMark' }), 0]
    },

    parseHTML() {
        return [
            {
                tag: 'span',
                getAttrs: (node: HTMLElement) => { return node.getAttribute('type') === 'LocationMark' && null; }
            },
        ]
    },
});
