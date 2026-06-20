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
const mapNavigator = ref(null);

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

function goToRoom(label) {
  const element = document.querySelector(`[inkscape\\:label="${label}"]`);
  if (element) {
    let parent = element.parentElement;
    let layerLabel = '';
    while (parent) {
      if (parent.tagName === 'g' && parent.getAttribute('inkscape:groupmode') === 'layer') {
        layerLabel = parent.getAttribute('inkscape:label') || '';
        break;
      }
      parent = parent.parentElement;
    }

    if (layerLabel.endsWith('C') && !isFloorC.value) {
      changeFloor();
    } else if (layerLabel.endsWith('T') && isFloorC.value) {
      changeFloor();
    }
  }

  setTimeout(() => {
    mapNavigator.value?.goToRoom(label);
    handleElementClick({ label });
  }, 50);
}

function search(query, onlyNow) {
  const q = query.toLowerCase().trim();
  if (!q) return [];

  const results = [];
  const dayNames = ['domingo', 'segunda', 'terça', 'quarta', 'quinta', 'sexta', 'sábado'];

  const date = props.simulatedDate;
  const dayIndex = date.getDay();
  const currentTime = date.getHours() * 60 + date.getMinutes();

  // 1. Search for classes in alocacao
  for (let label in alocacao.value) {
    const salaInfo = alocacao.value[label];
    const displayName = mapData.value[1][label] || label;
    
    // Check if the room name/description itself matches the query
    const basicInfo = mapData.value[0][label] || '';
    const description = typeof basicInfo === 'string' ? basicInfo : (basicInfo.description || '');
    
    const labelMatch = label.toLowerCase().includes(q) || 
                       displayName.toLowerCase().includes(q) || 
                       description.toLowerCase().includes(q);

    if (salaInfo.grade_horaria) {
      salaInfo.grade_horaria.forEach(slot => {
        const [startStr, endStr] = slot.horario.split(' - ');
        if (!startStr || !endStr) return;
        const [startH, startM] = startStr.split(':').map(Number);
        const [endH, endM] = endStr.split(':').map(Number);
        const startTime = startH * 60 + startM;
        const endTime = endH * 60 + endM;

        const isTimeNow = currentTime >= startTime && currentTime < endTime;

        slot.semana.forEach((classInfo, index) => {
          if (!classInfo) return;

          const isDayNow = index === dayIndex;
          const isHappeningNow = isTimeNow && isDayNow;

          if (onlyNow && !isHappeningNow) return;

          const matchDisciplina = classInfo.disciplina.toLowerCase().includes(q);
          const matchSigla = classInfo.sigla?.toLowerCase().includes(q);
          const matchProfessor = classInfo.professor?.toLowerCase().includes(q);

          if (matchDisciplina || matchSigla || matchProfessor || labelMatch) {
            results.push({
              type: 'class',
              label: label,
              roomName: displayName,
              disciplina: classInfo.disciplina,
              sigla: classInfo.sigla,
              professor: classInfo.professor,
              horario: slot.horario,
              dayIndex: index,
              dayName: dayNames[index],
              isNow: isHappeningNow
            });
          }
        });
      });
    }
  }

  // 2. Search for rooms/buildings in mapData.value[1] (from map.json)
  if (!onlyNow) {
    for (let label in mapData.value[1]) {
      const displayName = mapData.value[1][label];
      const basicInfo = mapData.value[0][label] || '';
      const description = typeof basicInfo === 'string' ? basicInfo : (basicInfo.description || '');

      const labelMatch = label.toLowerCase().includes(q) || 
                         displayName.toLowerCase().includes(q) || 
                         description.toLowerCase().includes(q);

      if (labelMatch) {
        results.push({
          type: 'room',
          label: label,
          roomName: displayName,
          description: description,
          isNow: false
        });
      }
    }
  }

  return results;
}

onMounted(() => {
  updateLayers();
});

defineExpose({
  changeFloor,
  goToRoom,
  search
});

</script>
