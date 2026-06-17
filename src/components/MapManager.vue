<template>
  <MapNavigator ref="mapNavigator" @element-click="handleElementClick" @empty-click="$emit('empty-click', $event)"
    @mouse-move="$emit('mouse-move', $event)" @change-floor="changeFloor"/>
</template>

<script setup>
import { ref, defineProps, defineEmits, defineExpose, watch, onMounted } from 'vue';
import MapNavigator from './MapNavigator.vue';
import mapDataRaw from './static/map.json';
import alocacaoData from './static/alocacao.json';

const props = defineProps({
  simulatedDate: {
    type: Date,
    default: () => new Date()
  }
});

const emit = defineEmits(['update-info', 'empty-click', 'mouse-move']);

watch(() => props.simulatedDate, changeInfosByDate)

const mapData = ref(mapDataRaw);
const alocacao = ref(alocacaoData);

function getCurrentSlot(alocacaoInfo) {
  const date = props.simulatedDate;
  const dayIndex = date.getDay();
  const currentTime = date.getHours() * 60 + date.getMinutes();

  const slot = alocacaoInfo.grade_horaria?.find(slot => {
    const [startStr, endStr] = slot.horario.split(' - ');
    if (!startStr || !endStr) return false;
    const [startH, startM] = startStr.split(':').map(Number);
    const [endH, endM] = endStr.split(':').map(Number);
    const startTime = startH * 60 + startM;
    const endTime = endH * 60 + endM;
    
    return currentTime >= startTime && currentTime < endTime;
  });

  return slot ? slot.semana[dayIndex] : null;
}

function handleElementClick({ label }) {
  const basicInfo = mapData.value[0][label] || mapData.value[1][label] || label;
  const displayName = mapData.value[1][label] || label;

  let description = typeof basicInfo === 'string' ? basicInfo : (basicInfo.description || '');
  const alocacaoInfo = alocacao.value[label];

  if (alocacaoInfo) {
    if (alocacaoInfo.informacoes_adicionais) {
      description += `\n${alocacaoInfo.informacoes_adicionais}`;
    }

    const currentSlot = getCurrentSlot(alocacaoInfo)

    if (currentSlot) {
      const classInfo = currentSlot;
      description += `\n\nAgora: ${classInfo.disciplina} (${classInfo.professor})`;
    } else {
      description += `\n\nLivre agora`;
    }
  }

  emit('update-info', {
    build: displayName,
    description: description,
    alocacaoInfo: alocacaoInfo,
    img: mapData.value[0][label]?.photo || 'https://i.ytimg.com/vi/lHKajh0XyUE/hq720.jpg?sqp=-oaymwE7CK4FEIIDSFryq4qpAy0IARUAAAAAGAElAADIQj0AgKJD8AEB-AH-CYAC0AWKAgwIABABGE4gZSgyMA8=&rs=AOn4CLApVXxQq5IVWY4hOw1zwHuDSYzTsg'
  });
}

function changeInfosByDate(newDate) {
  const dayIndex = newDate.getDay();
  const currentTime = newDate.getHours() * 60 + newDate.getMinutes();

  const aloc = alocacao.value
  const teste = new Map()
  for (let sala in aloc) {
    aloc[sala].grade_horaria?.forEach(slot => {
      const [startStr, endStr] = slot.horario.split(' - ');
      if (!startStr || !endStr) return false;

      const [startH, startM] = startStr.split(':').map(Number);
      const [endH, endM] = endStr.split(':').map(Number);
      const startTime = startH * 60 + startM;
      const endTime = endH * 60 + endM;
      
      if (currentTime >= startTime && currentTime < endTime && slot.semana[dayIndex]) {
        teste.set(sala, slot.semana[dayIndex].sigla)
      }
    });
  }

  let group = document.getElementById("layer11")
  for (let child of group.childNodes) {
    let id = child.getAttribute("inkscape:label")
    child.firstElementChild.textContent = teste.get(id)
  }
  group = document.getElementById("g41")
  for (let child of group.childNodes) {
    let id = child.getAttribute("inkscape:label")
    child.firstElementChild.textContent = teste.get(id)
  }
}

const isFloorC = ref(false);

function updateLayers() {
  changeInfosByDate(props.simulatedDate)
  const layers = document.querySelectorAll('g[inkscape\\:groupmode="layer"]');
  layers.forEach(layer => {
    const label = layer.getAttribute('inkscape:label') || '';
    if (label.endsWith('T')) {
      layer.style.display = isFloorC.value ? 'none' : 'inline';
    } else if (label.endsWith('C')) {
      layer.style.display = isFloorC.value ? 'inline' : 'none';
    }
  });
}

function changeFloor() {
  isFloorC.value = !isFloorC.value;
  updateLayers();
}

onMounted(() => {
  updateLayers();
});

defineExpose({
  changeFloor
});

</script>
