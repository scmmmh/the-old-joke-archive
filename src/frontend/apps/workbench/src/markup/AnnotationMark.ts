// @ts-ignore
import { Mark } from 'tiptap';
// @ts-ignore
import { toggleMark } from 'tiptap-commands';

export default class AnnotationMark extends Mark {

    public get name() {
        return 'annotation';
    }

    public get schema() {
        return {
            attrs: {
                category: {
                    default: '',
                },
                settings: {
                    default: {},
                },
            },
            parseDOM: [
                {
                    tag: 'span.mark-annotation',
                },
            ],
            toDOM: () => ['span', { class: 'mark-annotation' }, 0],
        };
    }

    public commands({ type }: any) {
        return () => toggleMark(type);
    }
}
