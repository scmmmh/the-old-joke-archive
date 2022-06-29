import { Mark, mergeAttributes } from '@tiptap/core';

export const AnswerMark = Mark.create({
    name: 'AnswerMark',

    renderHTML({ HTMLAttributes }) {
        return ['span', mergeAttributes(HTMLAttributes, { 'type': 'AnswerMark' }), 0]
    },

    parseHTML() {
        return [
            {
                tag: 'span',
                getAttrs: (node: HTMLElement) => { return node.getAttribute('type') === 'AnswerMark' && null; }
            },
        ]
    },
});
