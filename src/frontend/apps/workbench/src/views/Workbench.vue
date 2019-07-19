<template>
  <div>
    <div>
      <nav>
        <ul role="menu" class="inline">
          <li><a>Move</a></li>
        </ul>
      </nav>
      <div>
        <img v-bind:src="sourceUrl"/>
      </div>
    </div>
    <div>List of extracted jokes</div>
    <div>Transcription and Annotation interface</div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import HelloWorld from '@/components/HelloWorld.vue'; // @ is an alias to /src

@Component({
    components: {
        HelloWorld,
    },
    computed: {
        sourceUrl() {
            if (this.$store.state.source.attributes) {
                return this.$store.state.source.attributes.img;
            } else {
                return '';
            }
        },
    },
    mounted() {
        this.$store.dispatch('loadSource', 1);
    },
})
export default class Workbench extends Vue {}
</script>
