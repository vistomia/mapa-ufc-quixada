<template>
    <div class="table" v-if="alocacaoInfo && alocacaoInfo.grade_horaria">
        <div class="schedule-controls">
        <button class="btn-controls" @click="prevDay">❬</button>
        <button class="btn-controls">{{ dayNames[currentDayIndex] }}</button>
        <button class="btn-controls" @click="nextDay">❭</button>
        </div>
        <table class="schedule">
        <tbody>
            <template v-for="(slot, index) in alocacaoInfo.grade_horaria" :key="index">
                <tr v-if="slot.semana[currentDayIndex]">
                    <td>{{ slot.horario }}</td>
                    <td>{{ slot.semana[currentDayIndex].disciplina }}</td>
                    <td>{{ slot.semana[currentDayIndex].professor }}</td>
                </tr>
            </template>
            <tr v-if="!hasClasses">
                <td colspan="3" style="text-align: center; padding: 20px;">Livre este dia</td>
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
  margin:auto;
  border-collapse: collapse;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #ffffff;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.schedule td {
  padding: 10px;
  color: #333;
}

.schedule tr {
  border-bottom: 2px solid #dadcf0;
}

.schedule tr:nth-last-child(1) {
  padding: 8px;
  border: none;
  color: #333;
}

.schedule td:nth-child(1) {
  font-weight: bold;
  color: #032633;
  width: 30%;
}

.schedule td:nth-child(2) {
  font-size: 1.1em;
  text-align: left;
  font-weight: 600;
}

.schedule td:nth-child(3) {
  color: #666;
}

.schedule-controls {
  width: 90%;
  margin: 0em auto -1em auto;
  text-align: center;
  height: 3em;
  padding: 10px 0px;
  background-color: #dadcf0;
  border-radius: 16px 16px 0px 0px;
}

.schedule-controls button {
  padding: 0px 10px;
  font-size: 1.5em;
  font-style: none;
  border-style: none;
  background: none;
}
</style>