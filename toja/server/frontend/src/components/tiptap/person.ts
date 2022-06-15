import { Mark, mergeAttributes } from '@tiptap/core';

export const PersonMark = Mark.create({
    name: 'PersonMark',

    addAttributes() {
        return {
            gender: {
                default: 'unknown'
            }
        }
    },

    renderHTML({ HTMLAttributes }) {
        return ['span', mergeAttributes(HTMLAttributes, { 'type': 'PersonMark' }), 0]
    },

    parseHTML() {
        return [
            {
                tag: 'span',
                getAttrs: (node: HTMLElement) => { return node.getAttribute('type') === 'PersonMark' && null; }
            },
        ]
    },
});
