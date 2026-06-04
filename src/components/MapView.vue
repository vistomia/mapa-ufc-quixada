<template>
   <div class="map-container">
      <svg :viewBox="viewBoxString" @wheel.prevent="handleWheel" @mousemove="handleMouseMove"
         @mousedown="handleMouseDown" class="map-svg" ref="svgElement">
         <LayerDefinitions />
         <LayerDetails />
         <LayerBlocos />
         <LayerVista />
         <LayerSalasAC />
         <LayerSalasB1 />
         <LayerSalasRU />
         <LayerSalasGuarita />
          <LayerInfo style="pointer-events: none;" />
      </svg>

      <CardInfo :conteudo="conteudo"></CardInfo>
   </div>
   <div class="map-time-control">

   
   <div class="control-row">
      <select v-model="selectedDay" class="day-select">
         <option :value="0">Domingo</option>
         <option :value="1">Segunda-feira</option>
         <option :value="2">Terça-feira</option>
         <option :value="3">Quarta-feira</option>
         <option :value="4">Quinta-feira</option>
         <option :value="5">Sexta-feira</option>
         <option :value="6">Sábado</option>
      </select>
   </div>

   <div class="slider-wrapper">
      <div class="time-display">
         <span class="time-label">Horário</span>
         <span class="time-value">{{ formatTime(selectedTimeMinutes) }}</span>
      </div>
      
      <input 
         type="range" 
         min="0" 
         max="1439" 
         step="15" 
         v-model.number="selectedTimeMinutes" 
         class="time-slider" 
         :style="{ '--val': `${(selectedTimeMinutes / 1439) * 100}%` }"
      />
      <div class="slider-marks">
         <span>00:00</span>
         <span>12:00</span>
         <span>23:59</span>
      </div>
   </div>
</div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch} from 'vue';
import LayerDetails from './map_parsed/LayerDetails.vue';
import LayerDefinitions from './map_parsed/LayerDefinitions.vue';
import LayerSalasAC from './map_parsed/LayerSalasAC.vue';
import LayerSalasB1 from './map_parsed/LayerSalasB1.vue';
import LayerSalasRU from './map_parsed/LayerSalasRU.vue';
import LayerBlocos from './map_parsed/LayerBlocos.vue';
import LayerVista from './map_parsed/LayerVista.vue';
import LayerInfo from './map_parsed/LayerInfo.vue';
import LayerSalasGuarita from './map_parsed/LayerSalasGuarita.vue';

import map from './map.json'
import alocacao from './alocacao.json'
import CardInfo from './CardInfo.vue'

// Elemento SVG para obter suas dimensões na tela
const svgElement = ref(null);

// É uma câmera virtual sobre o SVG.
// [x, y, largura, altura]
const viewBox = reactive({
   x: -250,
   y: 0,
   width: 1000,
   height: 1000,
});

// String computada para usar no atributo :viewBox do SVG
const viewBoxString = computed(() => {
   return `${viewBox.x} ${viewBox.y} ${viewBox.width} ${viewBox.height}`;
});

// Coordenadas do mouse dentro do sistema do SVG
const mouseCoords = reactive({ x: 0, y: 0 });
const conteudo = reactive({ build: '', description: ''});

// Estado do dragging
const isDragging = ref(false);
const lastMousePosition = reactive({ x: 0, y: 0 });

// Função para lidar com o evento da roda do mouse (zoom)
function handleWheel(event) {
   const zoomFactor = 0.1; // Fator de zoom reduzido para movimento mais suave
   const { deltaY } = event;

   if (!svgElement.value) return;
   const svgPoint = getSvgCoordinates(event);

   // Calcula o fator de zoom (aumenta ou diminui)
   const zoomDirection = deltaY < 0 ? 1 - zoomFactor : 1 + zoomFactor;

   // Calcula o novo tamanho do viewBox
   const newWidth = viewBox.width * zoomDirection;
   const newHeight = viewBox.height * zoomDirection;

   // Limita o zoom para evitar valores extremos
   const minZoom = 30; // Tamanho mínimo do viewBox
   const maxZoom = 1000; // Tamanho máximo do viewBox
   console.log(newWidth)
   if (newWidth < minZoom || newWidth > maxZoom) return;

   // Ajusta a posição (x, y) do viewBox para que o zoom seja centrado no mouse
   viewBox.x = svgPoint.x - (svgPoint.x - viewBox.x) * zoomDirection;
   viewBox.y = svgPoint.y - (svgPoint.y - viewBox.y) * zoomDirection;

   // Atualiza a largura e altura
   viewBox.width = newWidth;
   viewBox.height = newHeight;
}

let isClick = false
let x = 0
let y = 0

// Função para iniciar o dragging
function handleMouseDown(event) {
   // Adiciona cor vibrante por 2 segundos
   isDragging.value = true;
   // Usa coordenadas de tela em vez de coordenadas SVG
   lastMousePosition.x = event.clientX;
   lastMousePosition.y = event.clientY;

   x = event.clientX
   y = event.clientY
   console.log(`Mouse down at: (${x}, ${y})`);
   // Adiciona event listeners para o documento para capturar movimentos fora do SVG
   document.addEventListener('mousemove', handleDocumentMouseMove);
   document.addEventListener('mouseup', handleMouseUp);
}

let color = 'red'
let labela = ''

const data = map[0]
const title = map[1]
const cronograma = map[2]

console.log(data)

function get_description(label) {
   return data[label] || 'Descrição não encontrada';
}

function get_cronograma(label) {
   const sala = cronograma.salas[label];
   if (!sala) return null;
   
   const disciplinas = cronograma.disciplinas;
   const mapaTempo = cronograma.mapa_recorrencia;
   
   let resultado = `<strong>${sala.nome}</strong>\n`;
   resultado += `Lugares: ${sala.lugares}\n`;
   resultado += `Projetor: ${sala.tem_projetor ? 'Sim' : 'Não'}\n`;
   resultado += `Ar-condicionado: ${sala['ar-condicionado-estado']}\n\n`;
   resultado += '<strong>Horários:</strong>\n';
   
   const dias = ['segunda', 'terça', 'quarta', 'quinta', 'sexta'];
   
   dias.forEach(dia => {
      if (sala.horarios_indexados[dia]) {
         resultado += `\n<strong>${dia.charAt(0).toUpperCase() + dia.slice(1)}:</strong>\n`;
         Object.entries(sala.horarios_indexados[dia]).forEach(([inicio, info]) => {
            const disciplina = disciplinas[info.d_id];
            const horaInicio = mapaTempo[inicio] || inicio;
            const horaFim = mapaTempo[info.fim] || info.fim;
            resultado += `${horaInicio} - ${horaFim}: ${disciplina.nome} (${disciplina.professor})\n`;
         });
      }
   });
   
   return resultado;
}



function get_title(label) {
   return title[label] || 'ID: '+label;
}

// Função para atualizar o texto dos elementos SVG com seus nomes
function updateSvgLabels() {
   if (!svgElement.value) return;

   function getCurrentClass(salaId) {
      const sala = alocacao[salaId];
      if (!sala) return null;

      const now = simulatedDate.value;

      const currentHour = now.getHours();
      const currentMinutes = now.getMinutes();
      const currentTime = currentHour + currentMinutes / 60;
      const dayOfWeek = now.getDay(); // 0 = Sunday, 1 = Monday, ..., 6 = Saturday
      const dayIndex = dayOfWeek
      
      if (!sala.grade_horaria) return null;
      
      for (const timeSlot of sala.grade_horaria) {
         const [startStr, endStr] = timeSlot.horario.split(' - ');
         const [startHour, startMin] = startStr.split(':').map(Number);
         const [endHour, endMin] = endStr.split(':').map(Number);
         
         const startTime = startHour + startMin / 60;
         const endTime = endHour + endMin / 60;
         
         if (currentTime >= startTime && currentTime < endTime) {
            const classInfo = timeSlot.semana[dayIndex];
            if (classInfo) return classInfo.sigla;
         }
      }
      return "";
   }


   const salaNames = {
      'B1S1': 'B1-01\n' + getCurrentClass('B1SALA1'),
      'B1S2': 'B1-02\n' + getCurrentClass('B1SALA2'),
      'B1S3': 'B1-03\n' + getCurrentClass('B1SALA3'),
      'B1S4': 'B1-04\n' + getCurrentClass('B1SALA4'),
   };
   
   const textElements = svgElement.value.querySelectorAll('text[inkscape\\:label]');
   textElements.forEach(element => {
      const label = element.getAttribute('inkscape:label');
      if (label && salaNames[label]) {
         const tspan = element.querySelector('tspan');
         if (tspan) {
            tspan.textContent = salaNames[label];
         }
      }
   });
}

// Chama a função após o componente ser montado
onMounted(() => {
   updateSvgLabels();
});

// Função para finalizar o dragging
function handleMouseUp(event) {
   let label = event.target.attributes.getNamedItem('inkscape:label')

   console.log(x, y)
   console.log(event.clientX, event.clientY)
   isClick = (Math.abs(x - event.clientX) <= 10 && Math.abs(y - event.clientY) <= 10) 
   isDragging.value = false;

   if (label && isClick) {
      document.getElementById('app-info').style.display = 'block';
      conteudo.build = get_title(label.value);
      const cronogramaData = get_cronograma(label.value);
      conteudo.description = cronogramaData || get_description(label.value);
      if (event.target.tagName !== 'svg') {
         if (labela) {
            labela.style.fill = color
         }
         color = event.target.style.fill
         // Make the current color brighter
         const currentColor = getComputedStyle(event.target).fill;
         event.target.style.fill = saturateColor(currentColor, 540);
         labela = event.target
      }
   } else if (isClick) {
      document.getElementById('app-info').style.display = 'none';
      if (labela) labela.style.fill = color
   }

   // Remove event listeners do documento
   document.removeEventListener('mousemove', handleDocumentMouseMove);
   document.removeEventListener('mouseup', handleMouseUp);
}

// Função para lidar com movimento do mouse durante dragging (no documento)
function handleDocumentMouseMove(event) {
   if (!isDragging.value || !svgElement.value) return;

   // Calcula a diferença de movimento em pixels da tela
   const deltaX = event.clientX - lastMousePosition.x;
   const deltaY = event.clientY - lastMousePosition.y;

   // Converte o movimento de pixels para unidades do viewBox
   const rect = svgElement.value.getBoundingClientRect();
   const viewBoxDeltaX = (deltaX / rect.width) * viewBox.width;
   const viewBoxDeltaY = (deltaY / rect.height) * viewBox.height;

   // Move o viewBox na direção oposta ao movimento do mouse
   viewBox.x -= viewBoxDeltaX;
   viewBox.y -= viewBoxDeltaY;

   // Atualiza a última posição (em coordenadas de tela)
   lastMousePosition.x = event.clientX;
   lastMousePosition.y = event.clientY;
}

// Função para atualizar as coordenadas do mouse
function handleMouseMove(event) {
   if (event.target.attributes.getNamedItem('inkscape:label')) {
      event.target.style.cursor = 'pointer';
   }
   if (!svgElement.value) return;
   const point = getSvgCoordinates(event);
   mouseCoords.x = point.x;
   mouseCoords.y = point.y;
}

// Função auxiliar para converter as coordenadas do evento (pixels da tela)
// para as coordenadas do sistema interno do SVG.
function getSvgCoordinates(event) {
   const svg = svgElement.value;
   const rect = svg.getBoundingClientRect();

   // Posição do mouse em pixels, relativa ao canto superior esquerdo do SVG
   const screenX = event.clientX - rect.left;
   const screenY = event.clientY - rect.top;

   // Converte de pixels para as unidades do viewBox
   const svgX = (screenX / rect.width) * viewBox.width + viewBox.x;
   const svgY = (screenY / rect.height) * viewBox.height + viewBox.y;

   return { x: svgX, y: svgY };
}

function saturateColor(color, amount) {
   // Extrai os componentes RGB da cor
   const rgb = color.match(/\d+/g);

   if (rgb && rgb.length >= 3) {
         const r = parseInt(rgb[0]);
         const g = parseInt(rgb[1]);
         const b = parseInt(rgb[2]);
         
         // Convert to HSL for saturation manipulation
         const max = Math.max(r, g, b) / 255;
         const min = Math.min(r, g, b) / 255;
         const diff = max - min;
         
         let h, s, l = (max + min) / 2;
         
         if (diff === 0) {
         h = s = 0;
         } else {
         s = l > 0.5 ? diff / (2 - max - min) : diff / (max + min);
         switch (max) {
            case r / 255: h = (g / 255 - b / 255) / diff + (g < b ? 6 : 0); break;
            case g / 255: h = (b / 255 - r / 255) / diff + 2; break;
            case b / 255: h = (r / 255 - g / 255) / diff + 4; break;
         }
         h /= 6;
         }
         
         // Increase saturation
         s = Math.min(1, s * amount);
         
         // Convert back to RGB
         const hue2rgb = (p, q, t) => {
         if (t < 0) t += 1;
         if (t > 1) t -= 1;
         if (t < 1/6) return p + (q - p) * 6 * t;
         if (t < 1/2) return q;
         if (t < 2/3) return p + (q - p) * (2/3 - t) * 6;
         return p;
         };
         
         let newR, newG, newB;
         if (s === 0) {
         newR = newG = newB = l;
         } else {
         const q = l < 0.5 ? l * (1 + s) : l + s - l * s;
         const p = 2 * l - q;
         newR = hue2rgb(p, q, h + 1/3);
         newG = hue2rgb(p, q, h);
         newB = hue2rgb(p, q, h - 1/3);
         }
         
         return `rgb(${Math.round(newR * 255)}, ${Math.round(newG * 255)}, ${Math.round(newB * 255)})`;
      }
   return color; // Return original color if parsing fails
}


// --- NOVO: Lógica de Controle de Tempo ---
const nowInitial = new Date();
const selectedDay = ref(nowInitial.getDay());
// Converte a hora atual para minutos totais do dia (ex: 14:30 = 14 * 60 + 30 = 870)
const selectedTimeMinutes = ref(nowInitial.getHours() * 60 + nowInitial.getMinutes());
const simulatedDate = ref(new Date());

// Atualiza a simulatedDate sempre que o slider ou o select mudarem
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

   simulatedDate.value = newDate;
   
   // Refaz os labels do mapa com o novo horário!
   updateSvgLabels();
});

// Formata os minutos de volta para HH:MM para exibição na tela
function formatTime(minutes) {
   const h = Math.floor(minutes / 60).toString().padStart(2, '0');
   const m = (minutes % 60).toString().padStart(2, '0');
   return `${h}:${m}`;
}

/* Reseta para o relógio real do computador do usuário
function resetToRealTime() {
   const now = new Date();
   selectedDay.value = now.getDay();
   selectedTimeMinutes.value = now.getHours() * 60 + now.getMinutes();
}
*/
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

/* Container flutuante sobre o mapa */
.map-time-control {
    position: absolute;
    bottom: 40px; 
    left: 50%;
    transform: translateX(-50%); 
    z-index: 1000; 
    
    width: 90%;
    max-width: 380px;
    background: rgba(255, 255, 255, 0.85); 
    backdrop-filter: blur(12px); 
    -webkit-backdrop-filter: blur(12px);
    
    padding: 20px 24px;
    border-radius: 16px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
    border: 1px solid rgba(255, 255, 255, 0.4);
    font-family: 'Inter', 'Segoe UI', sans-serif;
    display: flex;
    flex-direction: column;
    gap: 16px; /* Espaçamento uniforme entre as linhas */
}

/* Cabeçalho */
.time-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(0, 0, 0, 0.1);
    padding-bottom: 12px;
}

.time-title {
    margin: 0;
    font-size: 18px;
    font-weight: 600;
    color: #1e293b;
}

.reset-btn {
    background: #f1f5f9;
    border: none;
    border-radius: 8px;
    padding: 6px 10px;
    cursor: pointer;
    font-size: 16px;
    transition: background 0.2s, transform 0.1s;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.reset-btn:hover {
    background: #e2e8f0;
}

.reset-btn:active {
    transform: scale(0.95);
}

/* Seletor de Dias */
.day-select {
    width: 100%;
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
    appearance: none; /* Remove a seta padrão em alguns navegadores */
    background-image: url("data:image/svg+xml;charset=US-ASCII,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22292.4%22%20height%3D%22292.4%22%3E%3Cpath%20fill%3D%22%23475569%22%20d%3D%22M287%2069.4a17.6%2017.6%200%200%200-13-5.4H18.4c-5%200-9.3%201.8-12.9%205.4A17.6%2017.6%200%200%200%200%2082.2c0%205%201.8%209.3%205.4%2012.9l128%20127.9c3.6%203.6%207.8%205.4%2012.8%205.4s9.2-1.8%2012.8-5.4L287%2095c3.5-3.5%205.4-7.8%205.4-12.8%200-5-1.9-9.2-5.5-12.8z%22%2F%3E%3C%2Fsvg%3E");
    background-repeat: no-repeat;
    background-position: right 12px top 50%;
    background-size: 10px auto;
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