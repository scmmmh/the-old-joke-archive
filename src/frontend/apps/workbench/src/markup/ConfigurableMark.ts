// @ts-ignore
import { Mark } from 'tiptap';
// @ts-ignore
import { toggleMark } from 'tiptap-commands';

export default class ConfigurableMark extends Mark {

    private markName: string;

    constructor(name: string) {
        super();
        this.markName = name;
    }

    public get name() {
        return this.markName;
    }

    public get schema() {
        return {
            parseDOM: [
                {
                    tag: 'span.mark-' + this.markName,
                },
            ],
            toDOM: () => ['span', { class: 'mark-' + this.markName }, 0],
        };
    }

    public commands({ type }: any) {
        return () => toggleMark(type);
    }
}
