<template>
   <div class="map-container">
      <svg :viewBox="viewBoxString" @wheel.prevent="handleWheel" @mousemove="handleMouseMove"
         @mousedown="handleMouseDown" class="map-svg" ref="svgElement">
         <LayerDefinitions />
         <LayerDetails />
         <LayerBuild />
         <LayerServiceBuildings />
         <LayerAcademicBuildings />
         <LayerRoomsB1 />
      </svg>

      <div id="app-info" class="coordinates app-info">
         <h1>
            {{ conteudo.build }}
         </h1>
         <p>{{ conteudo.description }}</p>
         X: {{ mouseCoords.x.toFixed(2) }},
         Y: {{ mouseCoords.y.toFixed(2) }}
      </div>
   </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue';
import LayerDetails from './map/LayerDetails.vue';
import LayerDefinitions from './map/LayerDefinitions.vue';
import LayerAcademicBuildings from './map/LayerAcademicBuildings.vue';
import LayerServiceBuildings from './map/LayerServiceBuildings.vue';
import LayerRoomsB1 from './map/LayerRoomsB1.vue';

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
   const minZoom = 100; // Tamanho mínimo do viewBox
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
   if (event.key == 'a') {
      viewBox.x -= 10;
      console.log('left')
   }
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

const data = {
   'ADM': 'Térreo: Restaurante Universitário\n Pavimento Superior: ADM',
   'B1': 'Descrição do bloco 1',
   'B2': 'Descrição do bloco 2',
   'B3': 'Descrição do bloco 3',
   'B4': 'Descrição do bloco 4',
   'PETSI': 'O PET-SI é um Programa de Educação Tutorial (PET), um dos programas especiais do Ministério da Educação (MEC), realizado na Universidade Federal do Ceará campus de Quixadá. O programa visa auxiliar na melhoria do ensino de graduação, realizando atividades extracurriculares que envolvam pesquisa, ensino e extensão.',
   'PET': 'Grupo PET TI Conexões de Saberes. Desde 2010 desenvolvendo atividades de ensino, pesquisa e extensão na UFC Campus Quixadá.',
   'NULL': 'Local desconhecido e restrito',
   'SECRETARIA_ACADEMICA': 'Descrição da Secretaria Acadêmica\nHorarios1,Horarios2,Horarios3',
   'B1SALA1': 'Sala de aula 1',
   'B1SALA2': 'Sala de aula 2',
   'B1SALA3': 'Sala de aula 3',
   'B1SALA4': 'Sala de aula 4',
}
function get_description(label) {
   return data[label] || 'Description not found';
}
// Função para finalizar o dragging
function handleMouseUp(event) {
   let label = event.target.attributes.getNamedItem('inkscape:label')

   console.log(x, y)
   console.log(event.clientX, event.clientY)
   isClick = (Math.abs(x - event.clientX) <= 10 && Math.abs(y - event.clientY) <= 10) 
   isDragging.value = false;

   if (label && isClick) {
      document.getElementById('app-info').style.display = 'block';
      conteudo.build = label.value;
      conteudo.description = get_description(label.value);
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
   /* O tamanho da fonte é relativo ao viewBox */
   font-family: sans-serif;
   fill: white;
   text-anchor: middle;
   /* Centraliza o texto */
   dominant-baseline: middle;
   pointer-events: none;
   /* Impede que o texto intercepte eventos do mouse */
}

.app-info {
   position: absolute;
   top: 0;
   left: 0;
   width: 25%;
   height: 100%;
   background-color: white;
   padding: 20px;
   border-radius: 8px;
   box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

body {
   margin: 0;
   padding: 0;
}
</style>