import { Mark, mergeAttributes } from '@tiptap/core';

export const SpokenTextMark = Mark.create({
    name: 'SpokenTextMark',

    renderHTML({ HTMLAttributes }) {
        return ['span', mergeAttributes(HTMLAttributes, { 'type': 'SpokenTextMark' }), 0]
    },

    parseHTML() {
        return [
            {
                tag: 'span',
                getAttrs: (node: HTMLElement) => { return node.getAttribute('type') === 'SpokenTextMark' && null; }
            },
        ]
    },
});
