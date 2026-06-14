<template>
   <div class="map-time-control">
      <div class="control-row">
         <select v-model="selectedDay" class="day-select">
            <option :value="1">Segunda-feira</option>
            <option :value="2">Terça-feira</option>
            <option :value="3">Quarta-feira</option>
            <option :value="4">Quinta-feira</option>
            <option :value="5">Sexta-feira</option>
         </select>
         <button @click="$emit('change-floor')" class="floor-button">
            Andar
         </button>
      </div>

      <div class="slider-wrapper">
         <div class="time-display">
            <span class="time-label">Horário</span>
            <span class="time-value">{{ formatTime(selectedTimeMinutes) }}</span>
         </div>
         
         <input 
            type="range" 
            min="420" 
            max="1145"
            step="15" 
            v-model.number="selectedTimeMinutes" 
            class="time-slider" 
            :style="{ '--val': `${((selectedTimeMinutes - 420) / (1145-420)) * 100}%` }"
         />
         <div class="slider-marks">
            <span>07:10</span>
            <span>12:00</span>
            <span>19:00</span>
         </div>
      </div>
   </div>
</template>

<script setup>
import { ref, watch, defineEmits } from 'vue';

const emit = defineEmits(['change', 'change-floor']);

const nowInitial = new Date();
const selectedDay = ref(nowInitial.getDay());
const selectedTimeMinutes = ref(nowInitial.getHours() * 60 + nowInitial.getMinutes());

function formatTime(minutes) {
   const h = Math.floor(minutes / 60).toString().padStart(2, '0');
   const m = (minutes % 60).toString().padStart(2, '0');
   return `${h}:${m}`;
}

watch([selectedDay, selectedTimeMinutes], () => {
   const newDate = new Date();
   
   // Ajusta o dia da semana relativo à semana atual
   const currentDay = newDate.getDay();
   const diff = selectedDay.value - currentDay;
   newDate.setDate(newDate.getDate() + diff);

   // Ajusta a hora baseada no slider
   const hours = Math.floor(selectedTimeMinutes.value / 60);
   const mins = selectedTimeMinutes.value % 60;
   newDate.setHours(hours, mins, 0, 0);

   emit('change', newDate);
}, { immediate: true });
</script>

<style scoped>
/* Container flutuante sobre o mapa */
.map-time-control {
    position: absolute;
    bottom: 0px; 
    left: 50%;
    transform: translateX(-50%); 
    z-index: 1000; 
    
    width: 90%;
    max-width: 380px;
    background: rgba(255, 255, 255, 0.85); 
    backdrop-filter: blur(12px); 
    -webkit-backdrop-filter: blur(12px);
    
    padding: 20px 24px;
    border-radius: 16px 16px 0px 0px;
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
    border: 1px solid rgba(255, 255, 255, 0.4);
    font-family: 'Inter', 'Segoe UI', sans-serif;
    display: flex;
    flex-direction: column;
    gap: 16px;
}

/* Seletor de Dias */
.control-row {
    display: flex;
    gap: 8px;
}

.day-select {
    flex: 1;
    padding: 10px 12px;
    border-radius: 8px;
    border: 1px solid #cbd5e1;
    background-color: #ffffff;
    font-size: 15px;
    color: #334155;
    outline: none;
    cursor: pointer;
    box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    transition: border-color 0.2s;
    appearance: none;
    background-image: url("data:image/svg+xml;charset=US-ASCII,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22292.4%22%20height%3D%22292.4%22%3E%3Cpath%20fill%3D%22%23475569%22%20d%3D%22M287%2069.4a17.6%2017.6%200%200%200-13-5.4H18.4c-5%200-9.3%201.8-12.9%205.4A17.6%2017.6%200%200%200%200%2082.2c0%205%201.8%209.3%205.4%2012.9l128%20127.9c3.6%203.6%207.8%205.4%2012.8%205.4s9.2-1.8%2012.8-5.4L287%2095c3.5-3.5%205.4-7.8%205.4-12.8%200-5-1.9-9.2-5.5-12.8z%22%2F%3E%3C%2Fsvg%3E");
    background-repeat: no-repeat;
    background-position: right 12px top 50%;
    background-size: 10px auto;
}

.floor-button {
    padding: 10px 16px;
    border-radius: 8px;
    border: 1px solid #cbd5e1;
    background-color: #ffffff;
    font-size: 15px;
    color: #334155;
    cursor: pointer;
    transition: all 0.2s;
    font-weight: 500;
}

.floor-button:hover {
    background-color: #f1f5f9;
    border-color: #94a3b8;
}

.day-select:focus {
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
}

/* Área do Slider */
.time-display {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
}

.time-label {
    font-size: 15px;
    color: #475569;
    font-weight: 500;
}

.time-value {
    font-size: 20px;
    font-weight: 700;
    color: #0f172a;
    background: #f1f5f9;
    padding: 4px 12px;
    border-radius: 8px;
    letter-spacing: 0.5px;
}

.slider-wrapper {
    width: 100%;
}

/* Slider Bar */
.time-slider {
    -webkit-appearance: none;
    appearance: none;
    width: 100%;
    height: 8px;
    border-radius: 4px;
    outline: none;
    margin: 10px 0;
    background: linear-gradient(to right, #3b82f6 var(--val), #cbd5e1 var(--val));
}

/* Bolinha do Slider - Webkit */
.time-slider::-webkit-slider-thumb {
    -webkit-appearance: none;
    appearance: none;
    width: 22px;
    height: 22px;
    border-radius: 50%;
    background: #ffffff;
    border: 4px solid #3b82f6;
    cursor: pointer;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
    transition: transform 0.1s ease;
}

.time-slider::-webkit-slider-thumb:hover {
    transform: scale(1.15);
}

/* Bolinha do Slider - Firefox */
.time-slider::-moz-range-thumb {
    width: 16px;
    height: 16px;
    border-radius: 50%;
    background: #ffffff;
    border: 4px solid #3b82f6;
    cursor: pointer;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
    transition: transform 0.1s ease;
}

.time-slider::-moz-range-thumb:hover {
    transform: scale(1.15);
}

/* Marcações abaixo da barra */
.slider-marks {
    display: flex;
    justify-content: space-between;
    margin-top: 4px;
    font-size: 12px;
    font-weight: 500;
    color: #64748b;
}
</style>
