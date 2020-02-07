<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';
import axios from 'axios';

@Component({
})
export default class AutoSuggest extends Vue {
    @Prop({type: String})
    public readonly url!: string;
    public suggestions: string[] = [];
    public selected: number = -1;
    public searchPrefix: string | null = null;

    public render() {
        if (this.$scopedSlots.default) {
            return this.$scopedSlots.default({
                suggestions: this.suggestions,
                keyboardNav: this.keyboardNav,
                mouseNav: this.mouseNav,
                isSelected: this.isSelected,
                searchPrefix: this.searchPrefix,
            });
        }
    }

    public keyboardNav(event: KeyboardEvent) {
        if (event.keyCode === 13) {
            if (this.selected >= 0 && this.selected < this.suggestions.length) {
                this.$emit('select', this.suggestions[this.selected]);
                this.suggestions = [];
                this.selected = -1;
                (event.target as HTMLInputElement).value = '';
                this.searchPrefix = null;
            } else if (this.suggestions.length === 0 && (event.target as HTMLInputElement).value !== '') {
                this.$emit('select', (event.target as HTMLInputElement).value);
                this.suggestions = [];
                this.selected = -1;
                (event.target as HTMLInputElement).value = '';
                this.searchPrefix = null;
            }
        } else if (event.keyCode === 38) {
            this.selected = Math.max(-1, Math.min(this.selected - 1, this.suggestions.length - 1));
        } else if (event.keyCode === 40) {
            this.selected = Math.max(-1, Math.min(this.selected + 1, this.suggestions.length - 1));
        } else {
            this.searchPrefix = (event.target as HTMLInputElement).value;
            axios.get(this.$props.url, {
                params: {
                    value: this.searchPrefix,
                },
            }).then((response) => {
                this.suggestions = response.data;
                this.selected = response.data.length > 0 ? 0 : -1;
            });
        }
    }

    public mouseNav(idx: number, event: MouseEvent) {
        if (event.type === 'mouseover') {
            this.selected = idx;
        } else if (event.type === 'click') {
            if (idx >= 0 && idx < this.suggestions.length) {
                this.$emit('select', this.suggestions[idx]);
                this.suggestions = [];
                this.selected = -1;
                const autosuggest = this.getRootAutosuggest(event.target as HTMLElement);
                if (autosuggest !== null) {
                    const input = autosuggest.querySelector('input[type="text"]');
                    if (input !== null) {
                        (input as HTMLInputElement).value = '';
                    }
                }
                this.searchPrefix = null;
            } else {
                const autosuggest = this.getRootAutosuggest(event.target as HTMLElement);
                if (autosuggest !== null) {
                    const input = autosuggest.querySelector('input[type="text"]');
                    if (input !== null && (input as HTMLInputElement).value !== '') {
                        this.$emit('select', (input as HTMLInputElement).value);
                        (input as HTMLInputElement).value = '';
                        this.suggestions = [];
                        this.selected = -1;
                        this.searchPrefix = null;
                    }
                }
            }
        }
    }

    public isSelected(idx: number) {
        return this.selected === idx;
    }

    private getRootAutosuggest(element: HTMLElement): HTMLElement | null {
        if (element.classList.contains('autosuggest')) {
            return element;
        } else {
            if (element.parentElement) {
                return this.getRootAutosuggest(element.parentElement);
            } else {
                return null;
            }
        }
    }
}
</script>
