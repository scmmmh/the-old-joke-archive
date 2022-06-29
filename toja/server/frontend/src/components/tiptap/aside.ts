import { Mark, mergeAttributes } from '@tiptap/core';

export const AsideMark = Mark.create({
    name: 'AsideMark',

    renderHTML({ HTMLAttributes }) {
        return ['span', mergeAttributes(HTMLAttributes, { 'type': 'AsideMark' }), 0]
    },

    parseHTML() {
        return [
            {
                tag: 'span',
                getAttrs: (node: HTMLElement) => { return node.getAttribute('type') === 'AsideMark' && null; }
            },
        ]
    },
});
