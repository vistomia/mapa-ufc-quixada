<template>
   <div class="map-container">
      <MapManager 
         ref="mapManager"
         :simulated-date="simulatedDate"
         @update-info="handleUpdateInfo"
         @empty-click="handleEmptyClick"
         @mouse-move="handleMouseMove"
      />
      <Transition name="slide">
         <MapInfoPanel v-if="showInfo" :conteudo="conteudo" @close="showInfo = false"></MapInfoPanel>
      </Transition>
   </div>

   <MapControls @change="handleTimeChange" />
</template>

<script setup>
import { ref } from 'vue';

import MapInfoPanel from './MapInfoPanel.vue'
import MapManager from './MapManager.vue';
import MapControls from './MapControls.vue';

const simulatedDate = ref(new Date());
const showInfo = ref(false);
const conteudo = ref({
   img: '',
   build: '',
   description: ''
});

function handleTimeChange(newDate) {
   simulatedDate.value = newDate;
}

function handleUpdateInfo(info) {
   conteudo.value = info;
   showInfo.value = true;
}

function handleEmptyClick() {
   showInfo.value = false;
}

</script>

<style scoped>
body {
   overflow: hidden;
}

.map-container {
   width: 100%;
}

.map-svg {
   width: 100%;
   height: 100%;
   background-color: #f0f0f0;
}

.map-label {
   font-size: 50px;
   font-family: sans-serif;
   fill: white;
   text-anchor: middle;
   dominant-baseline: middle;
   pointer-events: none;
}

.coords {
   position: fixed;
   bottom: 10px;
   right: 10px;
   margin: 0;
   padding: 5px 10px;
   background-color: rgba(0, 0, 0, 0.7);
   color: white;
   border-radius: 5px;
   font-size: 12px;
}

p {
   padding: 0px 24px;
}

body {
   margin: 0;
   padding: 0;
   overflow: hidden;
}
</style>