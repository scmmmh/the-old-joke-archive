import { Mark, mergeAttributes } from '@tiptap/core';

export const QuestionMark = Mark.create({
    name: 'QuestionMark',

    renderHTML({ HTMLAttributes }) {
        return ['span', mergeAttributes(HTMLAttributes, { 'type': 'QuestionMark' }), 0]
    },

    parseHTML() {
        return [
            {
                tag: 'span',
                getAttrs: (node: HTMLElement) => { return node.getAttribute('type') === 'QuestionMark' && null; }
            },
        ]
    },
});
