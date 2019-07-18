<template>
  <div>
    <div>This is the menu bar</div>
    <div>Image goes here</div>
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
})
export default class Home extends Vue {}
</script>
