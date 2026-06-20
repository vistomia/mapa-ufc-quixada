<template>
    <div class="table" v-if="alocacaoInfo && alocacaoInfo.grade_horaria">
        <div class="schedule-controls">
        <button class="btn-controls nav-arrow" @click="prevDay">❬</button>
        <button class="btn-controls day-name">{{ dayNames[currentDayIndex] }}</button>
        <button class="btn-controls nav-arrow" @click="nextDay">❭</button>
        </div>
        <table class="schedule">
        <tbody>
            <template v-for="(slot, index) in alocacaoInfo.grade_horaria" :key="index">
                <tr 
                  v-if="slot.semana[currentDayIndex]"
                  :class="{ 'current-class': isSlotNow(slot) }"
                >
                    <td class="col-time">
                      <span class="pulse-dot-indicator" v-if="isSlotNow(slot)"></span>
                      {{ slot.horario }}
                    </td>
                    <td>{{ slot.semana[currentDayIndex].disciplina }}</td>
                    <td>{{ slot.semana[currentDayIndex].professor }}</td>
                </tr>
            </template>
            <tr v-if="!hasClasses">
                <td colspan="3" style="text-align: center; padding: 25px; color: #64748b; font-weight: 500;">Livre este dia</td>
            </tr>
        </tbody>
        </table>
    </div>
</template>

<script setup>
import { ref, computed, defineProps, watch } from 'vue';

const props = defineProps({
    alocacaoInfo: {
        type: Object,
        default: null
    },
    initialDayIndex: {
        type: Number,
        default: new Date().getDay()
    },
    simulatedDate: {
        type: Date,
        default: () => new Date()
    }
});

const dayNames = ['domingo', 'segunda', 'terça', 'quarta', 'quinta', 'sexta', 'sábado'];
const currentDayIndex = ref(props.initialDayIndex);

watch(() => props.initialDayIndex, (newVal) => {
    currentDayIndex.value = newVal;
});

const hasClasses = computed(() => {
    if (!props.alocacaoInfo || !props.alocacaoInfo.grade_horaria) return false;
    return props.alocacaoInfo.grade_horaria.some(slot => slot.semana[currentDayIndex.value]);
});

function isSlotNow(slot) {
  if (currentDayIndex.value !== props.simulatedDate.getDay()) return false;

  const [startStr, endStr] = slot.horario.split(' - ');
  if (!startStr || !endStr) return false;
  
  const [startH, startM] = startStr.split(':').map(Number);
  const [endH, endM] = endStr.split(':').map(Number);
  
  const startTime = startH * 60 + startM;
  const endTime = endH * 60 + endM;
  
  const currentTime = props.simulatedDate.getHours() * 60 + props.simulatedDate.getMinutes();
  
  return currentTime >= startTime && currentTime < endTime;
}

function nextDay() {
    currentDayIndex.value = (currentDayIndex.value + 1) % 7;
}

function prevDay() {
    currentDayIndex.value = (currentDayIndex.value - 1 + 7) % 7;
}
</script>

<style>
.schedule {
  width: 90%;
  margin: auto;
  border-collapse: collapse;
  font-family: 'Inter', 'Segoe UI', Roboto, sans-serif;
  background-color: #ffffff;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  border: 1px solid #dadcf0;
}

.schedule td {
  padding: 14px 16px;
  color: #334155;
  font-size: 0.95em;
  border-bottom: 1px solid #e2e8f0;
}

.schedule tr:last-child td {
  border-bottom: none;
}

.schedule td.col-time {
  font-weight: 700;
  color: #032633;
  width: 30%;
  display: flex;
  align-items: center;
  gap: 8px;
}

.schedule td:nth-child(2) {
  font-size: 1em;
  text-align: left;
  font-weight: 600;
  color: #0f172a;
}

.schedule td:nth-child(3) {
  color: #64748b;
  font-size: 0.9em;
}

.schedule-controls {
  width: 90%;
  margin: 0em auto 0em auto;
  text-align: center;
  height: 3.5em;
  padding: 0 16px;
  background-color: #dadcf0;
  border-radius: 16px 16px 0px 0px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-sizing: border-box;
  border: 1px solid #cbd5e1;
  border-bottom: none;
}

.schedule-controls button {
  background: none;
  border: none;
  color: #032633;
  font-family: inherit;
}

.schedule-controls .nav-arrow {
  padding: 0px 16px;
  font-size: 1.7em;
  cursor: pointer;
  transition: transform 0.1s ease, color 0.2s ease;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
}

.schedule-controls .nav-arrow:hover {
  color: #1a73e8;
  transform: scale(1.2);
}

.schedule-controls .nav-arrow:active {
  transform: scale(0.9);
}

.schedule-controls .day-name {
  font-size: 1.3em;
  font-weight: bold;
  text-transform: capitalize;
  pointer-events: none;
  color: #0f172a;
}

/* Highlight styling for current class, staying completely faithful but refined */
.schedule tr.current-class td {
  background-color: #f0f5ff; /* Extremely soft blue/indigo highlight */
  border-bottom-color: #d0e0ff;
  border-top: 1px solid #d0e0ff;
}

.schedule tr.current-class td.col-time {
  border-left: 5px solid #1a73e8; /* Accent border on the left side of the row */
  color: #1a73e8;
  font-weight: 800;
}

.schedule tr.current-class td:nth-child(2) {
  color: #1a73e8;
}

/* Pulse indicator dot next to time in highlighted row */
.pulse-dot-indicator {
  width: 8px;
  height: 8px;
  background-color: #1a73e8;
  border-radius: 50%;
  display: inline-block;
  position: relative;
  flex-shrink: 0;
  animation: pulse-active 1.6s infinite;
}

@keyframes pulse-active {
  0% {
    transform: scale(0.9);
    box-shadow: 0 0 0 0 rgba(26, 115, 232, 0.7);
  }
  70% {
    transform: scale(1.15);
    box-shadow: 0 0 0 6px rgba(26, 115, 232, 0);
  }
  100% {
    transform: scale(0.9);
    box-shadow: 0 0 0 0 rgba(26, 115, 232, 0);
  }
}
</style>