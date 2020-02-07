<template>
    <div class="joke-transcriber">
        <nav>
            <ul role="menu" class="menu">
                <li role="presentation">
                    <a data-action="confirm" role="menuitem" @click="saveChanges">
                        <svg viewBox="0 0 24 24" class="icon mdi">
                            <path d="M21,7L9,19L3.5,13.5L4.91,12.09L9,16.17L19.59,5.59L21,7Z" />
                        </svg>
                    </a>
                </li>
                <li role="presentation">
                    <a data-action="cancel" role="menuitem" @click="discardChanges">
                        <svg viewBox="0 0 24 24" class="icon mdi">
                            <path d="M12,2A10,10 0 0,1 22,12A10,10 0 0,1 12,22A10,10 0 0,1 2,12A10,10 0 0,1 12,2M12,4A8,8 0 0,0 4,12C4,13.85 4.63,15.55 5.68,16.91L16.91,5.68C15.55,4.63 13.85,4 12,4M12,20A8,8 0 0,0 20,12C20,10.15 19.37,8.45 18.32,7.09L7.09,18.32C8.45,19.37 10.15,20 12,20Z" />
                        </svg>
                    </a>
                </li>
                <li role="separator"></li>
                <li role="presentation">
                    <a role="menuitem" :aria-checked="mode === 'transcribe' ? 'true': 'false'" @click="setMode('transcribe')">
                        <svg viewBox="0 0 24 24" class="icon mdi">
                            <path d="M8,12H16V14H8V12M10,20H6V4H13V9H18V12.1L20,10.1V8L14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H10V20M8,18H12.1L13,17.1V16H8V18M20.2,13C20.3,13 20.5,13.1 20.6,13.2L21.9,14.5C22.1,14.7 22.1,15.1 21.9,15.3L20.9,16.3L18.8,14.2L19.8,13.2C19.9,13.1 20,13 20.2,13M20.2,16.9L14.1,23H12V20.9L18.1,14.8L20.2,16.9Z" />
                        </svg>
                    </a>
                </li>
                <li role="presentation">
                    <a role="menuitem" :aria-checked="mode === 'attributes' ? 'true': 'false'" @click="setMode('attributes')">
                        <svg viewBox="0 0 24 24" class="icon mdi">
                            <path d="M21.7,13.35L20.7,14.35L18.65,12.3L19.65,11.3C19.86,11.08 20.21,11.08 20.42,11.3L21.7,12.58C21.92,12.79 21.92,13.14 21.7,13.35M12,18.94L18.07,12.88L20.12,14.93L14.06,21H12V18.94M4,2H18A2,2 0 0,1 20,4V8.17L16.17,12H12V16.17L10.17,18H4A2,2 0 0,1 2,16V4A2,2 0 0,1 4,2M4,6V10H10V6H4M12,6V10H18V6H12M4,12V16H10V12H4Z" />
                        </svg>
                    </a>
                </li>
            </ul>
            <editor-menu-bar v-if="mode === 'transcribe'" :editor="editor" v-slot="{ commands, isActive }">
                <ul role="menu" class="menu" style="flex-wrap:wrap;">
                    <li role="presentation">
                        <a role="menuitem" :aria-checked="isActive.annotation() ? 'true' : 'false'" @click="commands.annotation">Annotation</a>
                    </li>
                </ul>
            </editor-menu-bar>
        </nav>
        <div v-if="mode === 'transcribe'">
            <editor-content :editor="editor"></editor-content>
            <editor-menu-bar :editor="editor" v-slot="{ commands, isActive }">
                <div v-if="isActive.annotation()" class="padding-bottom">
                    <div class="margin-bottom">
                        <h2 class="font-size-default">Annotation Type</h2>
                        <select @change="setAnnotationAttributeValue('category', $event.target.value)">
                            <option value="">--- Please Select ---</option>
                            <template v-for="annotation in annotations">
                                <option v-if="annotation.separate" disabled="disabled" style="font-size: 1pt; background-color: #000000;"></option>
                                <option :value="annotation.name" v-html="annotation.label" :selected="hasAnnotationAttributeValue('category', annotation.name) ? 'selected' : null"></option>
                            </template>
                        </select>
                    </div>
                    <div v-for="annotation in annotations">
                        <div v-if="hasAnnotationAttributeValue('category', annotation.name)" v-for="attr in annotation.attrs" class="margin-bottom">
                            <h2 class="font-size-default">{{ attr.label }}</h2>
                            <select v-if="attr.type === 'select'" @change="setAnnotationAttributeValue('settings', {name: attr.name, value: $event.target.value})">
                                <option v-for="value in attr.values" :value="value[0]" v-html="value[1]" :selected="getAnnotationAttributeValue('settings')[attr.name] === value[0] ? 'selected' : null"></option>
                            </select>
                            <div v-else-if="attr.type === 'singletext'">
                                <auto-suggest :url="attr.autosuggest" v-slot="{ suggestions, keyboardNav, mouseNav, isSelected, searchPrefix }" @select="setAnnotationAttributeValue('settings', {name: attr.name, value: $event})">
                                    <div class="autosuggest">
                                        <input type="text" :value="searchPrefix !== null ? searchPrefix : getAnnotationAttributeValue('settings')[attr.name]" @keyup="keyboardNav"/>
                                        <ul v-if="suggestions.length > 0" class="no-bullet">
                                            <li v-for="suggest, idx in suggestions">
                                                <a role="menuitem" @click="mouseNav(idx, $event)" @mouseover="mouseNav(idx, $event)" :aria-selected="isSelected(idx) ? 'true' : 'false'">{{ suggest }}</a>
                                            </li>
                                        </ul>
                                    </div>
                                </auto-suggest>
                            </div>
                            <div v-else-if="attr.type === 'multitext'">
                                <ul>
                                    <li v-for="value in getAnnotationAttributeValue('settings')[attr.name]" class="value-and-action">
                                        <span>{{ value }}</span>
                                        <a @click="removeAnnotationAttributeValue('settings', {name: attr.name, value: value})" aria-label="Delete">
                                            <svg viewBox="0 0 24 24" class="icon mdi">
                                                <path d="M6,19A2,2 0 0,0 8,21H16A2,2 0 0,0 18,19V7H6V19M8,9H16V19H8V9M15.5,4L14.5,3H9.5L8.5,4H5V6H19V4H15.5Z" />
                                            </svg>
                                        </a>
                                    </li>
                                </ul>
                                <auto-suggest :url="attr.autosuggest" v-slot="{ suggestions, keyboardNav, mouseNav, isSelected }" @select="addAnnotationAttributeValue('settings', {name: attr.name, value: $event})">
                                    <div class="autosuggest">
                                        <div class="position-relative">
                                            <a @click="mouseNav(idx, $event)" class="form-element-nested-action">
                                                <svg viewBox="0 0 24 24" class="icon mdi">
                                                    <path d="M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z" />
                                                </svg>
                                            </a>
                                            <input type="text" @keyup="keyboardNav"/>
                                        </div>
                                        <ul v-if="suggestions.length > 0" class="no-bullet">
                                            <li v-for="suggest, idx in suggestions">
                                                <a role="menuitem" @click="mouseNav(idx, $event)" @mouseover="mouseNav(idx, $event)" :aria-selected="isSelected(idx) ? 'true' : 'false'">{{ suggest }}</a>
                                            </li>
                                        </ul>
                                    </div>
                                </auto-suggest>
                            </div>
                        </div>
                    </div>
                </div>
            </editor-menu-bar>
        </div>
        <div v-else-if="mode === 'attributes'">
            <div v-for="entry in metadata" class="margin-bottom">
                <h2 class="font-size-default">{{ entry.label }}</h2>
                <div v-if="entry.type === 'multichoice'">
                    <label v-for="value in entry.values">
                        <input type="checkbox" :value="value[0]" :checked="hasAttributeValue(entry.name, value[0], true) ? 'checked' : null" @change="$event.target.checked ? addAttributeValue(entry.name, value[0]) : removeAttributeValue(entry.name, value[0])"> <span v-html="value[1]"></span>
                    </label>
                </div>
                <select v-else-if="entry.type === 'select'" @change="setAttributeValue(entry.name, $event.target.value)">
                    <option v-for="value in entry.values" :value="value[0]" :selected="hasAttributeValue(entry.name, value[0]) ? 'selected' : null" v-html="value[1]"></option>
                </select>
                <div v-if="entry.type === 'multitext'">
                    <ul>
                        <li v-for="value in getAttributeValue(entry.name)" class="value-and-action">
                            <span>{{ value }}</span>
                            <a @click="removeAttributeValue(entry.name, value)" aria-label="Delete">
                                <svg viewBox="0 0 24 24" class="icon mdi">
                                    <path d="M6,19A2,2 0 0,0 8,21H16A2,2 0 0,0 18,19V7H6V19M8,9H16V19H8V9M15.5,4L14.5,3H9.5L8.5,4H5V6H19V4H15.5Z" />
                                </svg>
                            </a>
                        </li>
                    </ul>
                    <auto-suggest :url="entry.autosuggest" v-slot="{ suggestions, keyboardNav, mouseNav, isSelected }" @select="addAttributeValue(entry.name, $event)">
                        <div class="autosuggest">
                            <div class="position-relative">
                                <a @click="mouseNav(idx, $event)" class="form-element-nested-action">
                                    <svg viewBox="0 0 24 24" class="icon mdi">
                                        <path d="M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z" />
                                    </svg>
                                </a>
                                <input type="text" @keyup="keyboardNav"/>
                            </div>
                            <ul v-if="suggestions.length > 0" class="no-bullet">
                                <li v-for="suggest, idx in suggestions">
                                    <a role="menuitem" @click="mouseNav(idx, $event)" @mouseover="mouseNav(idx, $event)" :aria-selected="isSelected(idx) ? 'true' : 'false'">{{ suggest }}</a>
                                </li>
                            </ul>
                        </div>
                    </auto-suggest>
                </div>
            </div>
        </div>
        <div class="overlay" v-if="noTranscription">
            <p>Please select a joke from the list to transcribe and annotate it.</p>
        </div>
    </div>
</template>

<script lang="ts">
import { Component, Vue, Watch } from 'vue-property-decorator';
// @ts-ignore
import { Editor, EditorContent, EditorMenuBar } from 'tiptap';
// @ts-ignore
import { removeMark, updateMark } from 'tiptap-commands';
import AnnotationMark from '@/markup/AnnotationMark';
// @ts-ignore
import deepcopy from 'deepcopy';
import axios from 'axios';

import { Joke, Transcription } from '@/interfaces';
import AutoSuggest from './AutoSuggest.vue';

@Component({
    components: {
        EditorContent,
        EditorMenuBar,
        AutoSuggest,
    },
})
export default class JokeTranscriber extends Vue {
    public mode = 'transcribe';
    public editor: Editor | null = null;
    public attributes: any = {};
    public autosuggests: any = {};

    // ****************
    // Lifecycle events
    // ****************

    public mounted() {
        this.editor = new Editor({
            extensions: [
                new AnnotationMark(),
            ],
        });
    }

    public beforeDestroy() {
        if (this.editor) {
            this.editor.destroy();
        }
    }

    // **************
    // Event handlers
    // **************

    public saveChanges() {
        this.attributes = { ... this.attributes, ... { text: this.editor.getJSON() }};
        this.$store.dispatch('updateTranscription', this.attributes);
    }

    public discardChanges() {
        this.$store.dispatch('loadTranscription');
    }

    public setMode(mode: string) {
        this.mode = mode;
    }

    public attributeAutosuggest(entry: any, event: KeyboardEvent) {
        if (event !== null && event !== undefined) {
            if (entry.type === 'multitext') {
                if (event.keyCode === 13) {
                    this.addAttributeValue(entry.name, (event.target as HTMLInputElement).value);
                    (event.target as HTMLInputElement).value = '';
                } else {
                    axios.get(entry.autosuggest, {
                        params: {
                            value: (event.target as HTMLInputElement).value,
                        },
                    }).then((response) => {
                        this.autosuggests = {[entry.name]: response.data};
                    });
                }
            }
        }
    }

    public annotationAttributeAutosuggest(section: string, entry: any, event: KeyboardEvent) {
        if (event !== null && event !== undefined) {
            if (event.keyCode === 13) {
                if (entry.type === 'multitext') {
                    this.addAnnotationAttributeValue(section, {
                        name: entry.name,
                        value: (event.target as HTMLInputElement).value,
                    });
                    (event.target as HTMLInputElement).value = '';
                } else if (entry.type === 'singletext') {
                    this.setAnnotationAttributeValue(section, {
                        name: entry.name,
                        value: (event.target as HTMLInputElement).value,
                    });
                }
            } else {
                axios.get(entry.autosuggest, {
                    params: {
                        value: (event.target as HTMLInputElement).value,
                    },
                }).then((response) => {
                    this.autosuggests = {[entry.name]: response.data};
                });
            }
        }
    }

    // ************
    // Dynamic data
    // ************

    public get annotations() {
        return this.$store.state.annotations;
    }

    public get metadata() {
        return this.$store.state.metadata;
    }

    public get noTranscription() {
        return this.$store.state.transcription === null;
    }

    /**
     * Computed property of all selected nodes.
     */
    private get selectedNodes() {
        if (this.editor) {
            const { from, to } = this.editor.state.selection;
            const selectedNodes = [] as any;
            this.editor.state.doc.nodesBetween(from, to, (node: any) => {
                selectedNodes.push(node);
            });
            return selectedNodes;
        } else {
            return [];
        }
    }

    // ************
    // Data watches
    // ************

    @Watch('$store.state.selected')
    public watchSelectedJoke(newValue: Joke, oldValue: Joke) {
        this.$store.dispatch('loadTranscription');
    }

    @Watch('$store.state.transcription')
    public watchTranscription(newValue: Transcription) {
        if (newValue) {
            this.editor.setContent(newValue.attributes.text);
            this.attributes = deepcopy(newValue.attributes);
        } else {
            this.editor.setContent('');
            this.attributes = {};
        }
    }

    // *******************
    // Annotation handling
    // *******************

    /**
     * Gets a mark attribute value.
     */
    public getAnnotationAttributeValue(attrName: string) {
        for (const node of this.selectedNodes) {
            if (node.marks) {
                for (const mark of node.marks) {
                    if (mark.type.name === 'annotation') {
                        return mark.attrs[attrName];
                    }
                }
            }
        }
        return '';
    }

    /**
     * Checks whether a mark has a given attribute value.
     */
    public hasAnnotationAttributeValue(attrName: string, value: string) {
        return this.getAnnotationAttributeValue(attrName) === value;
    }

    /**
     * Sets the mark's attribute value.
     */
    public setAnnotationAttributeValue(attrName: string, value: any) {
        if (value) {
            const { from, to } = this.editor.state.selection;
            let attributes = {} as any;
            this.editor.state.doc.nodesBetween(from, to, (node: any) => {
                if (node.marks) {
                    node.marks.forEach((mark: any) => {
                        if (mark.type.name === 'annotation') {
                            attributes = {...attributes, ...mark.attrs};
                        }
                    });
                }
            });
            if (attrName === 'settings') {
                if (!attributes.settings) {
                    attributes.settings = {};
                }
                attributes.settings[value.name] = value.value;
            } else if (attrName === 'category') {
                attributes[attrName] = value;
            }
            updateMark(this.editor.schema.marks.annotation, attributes)(this.editor.state,
                this.editor.dispatchTransaction.bind(this.editor));
        } else {
            removeMark(this.editor.schema.marks.annotation)(this.editor.state,
                this.editor.dispatchTransaction.bind(this.editor));
        }
    }

    public addAnnotationAttributeValue(attrName: string, value: any) {
        const attr = this.getAnnotationAttributeValue(attrName);
        if (attr[value.name]) {
            const newAttrValues = deepcopy(attr[value.name]);
            if (newAttrValues.indexOf(value.value) < 0) {
                newAttrValues.push(value.value);
                this.setAnnotationAttributeValue(attrName, {name: value.name, value: newAttrValues});
            }
        } else {
            this.setAnnotationAttributeValue(attrName, {name: value.name, value: [value.value]});
        }
        if (this.autosuggests[value.name]) {
            this.autosuggests = {};
        }
    }

    public removeAnnotationAttributeValue(attrName: string, value: any) {
        const attr = this.getAnnotationAttributeValue(attrName);
        if (attr[value.name]) {
            const newAttrValues = deepcopy(attr[value.name]);
            if (newAttrValues.indexOf(value.value) >= 0) {
                newAttrValues.splice(newAttrValues.indexOf(value.value), 1);
                this.setAnnotationAttributeValue(attrName, {name: value.name, value: newAttrValues});
            }
        }
    }

    // ******************
    // Attribute handling
    // ******************

    public hasAttributeValue(name: string, value: string, multiple?: boolean) {
        const values = this.attributes[name];
        if (multiple) {
            if (values) {
                return values.indexOf(value) >= 0;
            } else {
                return false;
            }
        } else {
            return values === value;
        }
    }

    public getAttributeValue(name: string) {
        return this.attributes[name];
    }

    public addAttributeValue(name: string, value: string) {
        let values = this.attributes[name];
        if (!values) {
            values = [];
        }
        if (values.indexOf(value) < 0 && value) {
            values.push(value);
        }
        this.attributes = { ... this.attributes, ... { [name]: values} };
        if (this.autosuggests[name]) {
            this.autosuggests = {};
        }
    }

    public removeAttributeValue(name: string, value: string) {
        const values = this.attributes[name];
        if (values) {
            if (values.indexOf(value) >= 0) {
                values.splice(values.indexOf(value), 1);
            }
            this.attributes = { ... this.attributes, ... { [name]: values} };
        } else {
            this.attributes = { ... this.attributes, ... { [name]: []} };
        }
    }

    public setAttributeValue(name: string, value: string) {
        this.attributes = { ... this.attributes, ... { [name]: value} };
    }
}
</script>
