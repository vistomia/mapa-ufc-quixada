<template>
  <MapSVG
    ref="svgComponent"
    :viewBox="viewBoxString"
    @wheel.prevent="handleWheel"
    @mousemove="handleMouseMove"
    @mousedown="handleMouseDown"
    class="map-navigator-svg"
  />
</template>

<script setup>
import { ref, reactive, computed, defineEmits, defineExpose } from 'vue';
import MapSVG from './MapSVG.vue';

const emit = defineEmits(['element-click', 'empty-click', 'mouse-move']);

const svgComponent = ref(null);

const viewBox = reactive({
  x: -250,
  y: 0,
  width: 1000,
  height: 1000,
});

const viewBoxString = computed(() => {
  return `${viewBox.x} ${viewBox.y} ${viewBox.width} ${viewBox.height}`;
});

const isDragging = ref(false);
const lastMousePosition = reactive({ x: 0, y: 0 });
let startMousePosition = { x: 0, y: 0 };

function handleWheel(event) {
  const zoomFactor = 0.1;
  const { deltaY } = event;

  if (!svgComponent.value) return;
  const svgPoint = getSvgCoordinates(event);

  const zoomDirection = deltaY < 0 ? 1 - zoomFactor : 1 + zoomFactor;

  const newWidth = viewBox.width * zoomDirection;
  const newHeight = viewBox.height * zoomDirection;

  const minZoom = 30; 
  const maxZoom = 1000; 

  if (newWidth < minZoom || newWidth > maxZoom) return;

  viewBox.x = svgPoint.x - (svgPoint.x - viewBox.x) * zoomDirection;
  viewBox.y = svgPoint.y - (svgPoint.y - viewBox.y) * zoomDirection;

  viewBox.width = newWidth;
  viewBox.height = newHeight;
}

function handleMouseDown(event) {
  isDragging.value = true;
  lastMousePosition.x = event.clientX;
  lastMousePosition.y = event.clientY;
  startMousePosition.x = event.clientX;
  startMousePosition.y = event.clientY;

  document.addEventListener('mousemove', handleDocumentMouseMove);
  document.addEventListener('mouseup', handleMouseUp);
}

function handleMouseUp(event) {
  const isClick = (Math.abs(startMousePosition.x - event.clientX) <= 10 && 
                   Math.abs(startMousePosition.y - event.clientY) <= 10);
  
  isDragging.value = false;

  if (isClick) {
    const label = event.target.attributes.getNamedItem('inkscape:label');
    if (label) {
      emit('element-click', { label: label.value, event });
    } else {
      emit('empty-click', event);
    }
  }

  document.removeEventListener('mousemove', handleDocumentMouseMove);
  document.removeEventListener('mouseup', handleMouseUp);
}

function handleDocumentMouseMove(event) {
  if (!isDragging.value || !svgComponent.value) return;

  const deltaX = event.clientX - lastMousePosition.x;
  const deltaY = event.clientY - lastMousePosition.y;

  const svg = svgComponent.value.$el;
  const rect = svg.getBoundingClientRect();
  const viewBoxDeltaX = (deltaX / rect.width) * viewBox.width;
  const viewBoxDeltaY = (deltaY / rect.height) * viewBox.height;

  viewBox.x -= viewBoxDeltaX;
  viewBox.y -= viewBoxDeltaY;

  lastMousePosition.x = event.clientX;
  lastMousePosition.y = event.clientY;
}

function handleMouseMove(event) {
  if (event.target.attributes.getNamedItem('inkscape:label')) {
    event.target.style.cursor = 'pointer';
  }
  
  if (!svgComponent.value) return;
  const point = getSvgCoordinates(event);
  emit('mouse-move', point);
}

function getSvgCoordinates(event) {
  const svg = svgComponent.value.$el;
  const rect = svg.getBoundingClientRect();

  const screenX = event.clientX - rect.left;
  const screenY = event.clientY - rect.top;

  const svgX = (screenX / rect.width) * viewBox.width + viewBox.x;
  const svgY = (screenY / rect.height) * viewBox.height + viewBox.y;

  return { x: svgX, y: svgY };
}

defineExpose({
  svgComponent,
  viewBox
});
</script>

<style scoped>
.map-navigator-svg {
  width: 100%;
  height: 100%;
  background-color: #f0f0f0;
}
</style>
