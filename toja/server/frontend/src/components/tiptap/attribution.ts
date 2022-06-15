import { Mark, mergeAttributes } from '@tiptap/core';

export const AttributionMark = Mark.create({
    name: 'AttributionMark',

    renderHTML({ HTMLAttributes }) {
        return ['span', mergeAttributes(HTMLAttributes, { 'type': 'AttributionMark' }), 0]
    },

    parseHTML() {
        return [
            {
                tag: 'span',
                getAttrs: (node: HTMLElement) => { return node.getAttribute('type') === 'AttributionMark' && null; }
            },
        ]
    },
});
