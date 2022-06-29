import { Mark, mergeAttributes } from '@tiptap/core';

export const ObjectMark = Mark.create({
    name: 'ObjectMark',

    renderHTML({ HTMLAttributes }) {
        return ['span', mergeAttributes(HTMLAttributes, { 'type': 'ObjectMark' }), 0]
    },

    parseHTML() {
        return [
            {
                tag: 'span',
                getAttrs: (node: HTMLElement) => { return node.getAttribute('type') === 'ObjectMark' && null; }
            },
        ]
    },
});
