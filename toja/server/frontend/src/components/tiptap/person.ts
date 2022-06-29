import { Mark, mergeAttributes } from '@tiptap/core';

export const PersonMark = Mark.create({
    name: 'PersonMark',

    addAttributes() {
        return {
            age: {
                default: null,
            },
            gender: {
                default: null,
            },
            class: {
                default: null,
            },
            role: {
                default: null,
            },
            nationality: {
                default: null,
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
