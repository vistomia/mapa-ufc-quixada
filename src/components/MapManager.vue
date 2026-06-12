<template>
  <MapNavigator
    ref="mapNavigator"
    @element-click="handleElementClick"
    @empty-click="$emit('empty-click', $event)"
    @mouse-move="$emit('mouse-move', $event)"
  />
</template>

<script setup>
import { ref, computed } from 'vue';
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

const mapData = ref(mapDataRaw);
const alocacao = ref(alocacaoData);

function handleElementClick({ label, event }) {
  const basicInfo = mapData.value[0][label] || mapData.value[1][label] || label;
  const displayName = mapData.value[1][label] || label;
  
  let description = typeof basicInfo === 'string' ? basicInfo : (basicInfo.description || '');
  const alocacaoInfo = alocacao.value[label];

  if (alocacaoInfo) {
    description += `\n\nLocal: ${alocacaoInfo.local}`;
    if (alocacaoInfo.informacoes_adicionais) {
      description += `\nInfo: ${alocacaoInfo.informacoes_adicionais}`;
    }
    
    // Find current class
    const date = props.simulatedDate;
    const dayIndex = date.getDay();
    const currentTime = date.getHours() * 60 + date.getMinutes();
    
    const currentSlot = alocacaoInfo.grade_horaria?.find(slot => {
      const [startStr, endStr] = slot.horario.split(' - ');
      if (!startStr || !endStr) return false;
      const [startH, startM] = startStr.split(':').map(Number);
      const [endH, endM] = endStr.split(':').map(Number);
      const startTime = startH * 60 + startM;
      const endTime = endH * 60 + endM;
      return currentTime >= startTime && currentTime < endTime && slot.semana[dayIndex];
    });

    if (currentSlot) {
      const classInfo = currentSlot.semana[dayIndex];
      description += `\n\nAgora: ${classInfo.disciplina} (${classInfo.professor})`;
    } else {
      description += `\n\nLivre agora`;
    }
  }

  emit('update-info', {
    build: displayName,
    description: description,
    img: mapData.value[0][label]?.photo || 'https://via.placeholder.com/500x600?text=' + label
  });
}
</script>
