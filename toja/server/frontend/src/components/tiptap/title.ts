import { Mark, mergeAttributes } from '@tiptap/core';

export const TitleMark = Mark.create({
    name: 'TitleMark',

    renderHTML({ HTMLAttributes }) {
        return ['span', mergeAttributes(HTMLAttributes, { 'type': 'TitleMark' }), 0]
    },

    parseHTML() {
        return [
            {
                tag: 'span',
                getAttrs: (node: HTMLElement) => { return node.getAttribute('type') === 'TitleMark' && null; }
            },
        ]
    },
});
