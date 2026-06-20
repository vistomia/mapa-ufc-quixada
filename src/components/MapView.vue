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
         <MapInfoPanel v-if="showInfo" :conteudo="conteudo" :simulatedDate="simulatedDate" @close="showInfo = false"></MapInfoPanel>
      </Transition>
      <AppSearch 
         class="t"
         :search-results="searchResults"
         :simulated-date="simulatedDate"
         @search-change="handleSearchChange"
         @select-result="handleSelectResult"
      />
   </div>

   <MapControls :simulated-date="simulatedDate" @change="handleTimeChange" @change-floor="handleChangeFloor" />
</template>

<script setup>
import { ref } from 'vue';

import MapInfoPanel from './MapInfoPanel.vue'
import MapManager from './MapManager.vue';
import MapControls from './MapControls.vue';
import AppSearch from './AppSearch.vue'

const simulatedDate = ref(new Date());
const showInfo = ref(false);
const mapManager = ref(null);
const searchResults = ref([]);
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

function handleMouseMove() {
   // console.log(point);
}

function handleChangeFloor() {
   mapManager.value?.changeFloor();
}

function handleSearchChange({ query, onlyNow }) {
   if (!query.trim()) {
      searchResults.value = [];
      return;
   }
   searchResults.value = mapManager.value?.search(query, onlyNow) || [];
}

function handleSelectResult(result) {
   if (result.type === 'class') {
      const newDate = new Date();
      const currentDay = newDate.getDay();
      const diff = result.dayIndex - currentDay;
      newDate.setDate(newDate.getDate() + diff);

      const [startStr] = result.horario.split(' - ');
      if (startStr) {
         const [hours, mins] = startStr.split(':').map(Number);
         newDate.setHours(hours, mins, 0, 0);
      }
      simulatedDate.value = newDate;
   }

   mapManager.value?.goToRoom(result.label);
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

.t {
   position: absolute;
   top: 0;
   left: 0;
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