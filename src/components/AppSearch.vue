<template>
  <div class="search-container" ref="searchContainerRef">
    <div class="search-bar">
      <div class="search-icon">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 640" style="width: 1em; height: 1em;">
          <path fill="#64748b" d="M480 272C480 317.9 465.1 360.3 440 394.7L566.6 521.4C579.1 533.9 579.1 554.2 566.6 566.7C554.1 579.2 533.8 579.2 521.3 566.7L394.7 440C360.3 465.1 317.9 480 272 480C157.1 480 64 386.9 64 272C64 157.1 157.1 64 272 64C386.9 64 480 157.1 480 272zM272 416C351.5 416 416 351.5 416 272C416 192.5 351.5 128 272 128C192.5 128 128 192.5 128 272C128 351.5 192.5 416 272 416z"/>
        </svg>
      </div>
      <input 
        type="text" 
        v-model="searchQuery" 
        placeholder="Pesquise por matéria ou sala..." 
        class="search-input"
        @focus="showDropdown = true"
        @input="handleInput"
      />
      <button 
        @click="toggleOnlyNow" 
        :class="['now-toggle', { active: onlyNow }]"
        title="Filtrar por aulas acontecendo agora"
      >
        <span class="pulse-dot" v-if="onlyNow"></span>
        🕒 Agora
      </button>
    </div>

    <!-- Dropdown results -->
    <div v-if="showDropdown && searchQuery.trim()" class="results-dropdown">
      <div v-if="searchResults.length === 0" class="no-results">
        Nenhuma aula ou sala encontrada.
      </div>
      <div 
        v-else 
        v-for="(result, index) in searchResults" 
        :key="index" 
        class="result-item"
        @click="selectResult(result)"
      >
        <div class="result-title">
          <template v-if="result.type === 'class'">
            {{ result.disciplina }} ({{ result.sigla }})
          </template>
          <template v-else>
            {{ result.roomName }}
          </template>
        </div>
        <div class="result-details">
          <span class="result-badge type">{{ result.type === 'class' ? 'Aula' : 'Sala' }}</span>
          <span v-if="result.type === 'class'" class="result-badge room">📍 {{ result.roomName }}</span>
          <span v-if="result.type === 'class'" class="result-badge professor">👤 {{ result.professor }}</span>
          <span v-if="result.type === 'class'" class="result-badge time">🕒 {{ result.dayName }}, {{ result.horario }}</span>
          <span v-if="result.isNow" class="result-badge now">● acontecendo agora</span>
          <span v-if="result.type === 'room' && result.description" class="result-description">{{ result.description }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps, defineEmits, watch, onMounted, onUnmounted } from 'vue';

const props = defineProps({
  searchResults: {
    type: Array,
    default: () => []
  },
  simulatedDate: {
    type: Date,
    default: () => new Date()
  }
});

const emit = defineEmits(['search-change', 'select-result']);

const searchQuery = ref('');
const onlyNow = ref(false);
const showDropdown = ref(false);
const searchContainerRef = ref(null);

function handleInput() {
  showDropdown.value = true;
  emitSearch();
}

function toggleOnlyNow() {
  onlyNow.value = !onlyNow.value;
  emitSearch();
}

function emitSearch() {
  emit('search-change', {
    query: searchQuery.value,
    onlyNow: onlyNow.value
  });
}

function selectResult(result) {
  emit('select-result', result);
  showDropdown.value = false;
}

function handleClickOutside(event) {
  if (searchContainerRef.value && !searchContainerRef.value.contains(event.target)) {
    showDropdown.value = false;
  }
}

// Watch simulatedDate to update search results dynamically if they depend on simulated "now"
watch(() => props.simulatedDate, () => {
  if (searchQuery.value) {
    emitSearch();
  }
});

onMounted(() => {
  document.addEventListener('click', handleClickOutside);
});

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
});
</script>

<style scoped>
.search-container {
    position: relative;
    width: 380px;
    font-family: 'Inter', 'Segoe UI', Roboto, sans-serif;
    z-index: 1002;
    margin-top: 1.5rem;
    margin-left: 1.5rem;
}

.search-bar {
    display: flex;
    align-items: center;
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(226, 232, 240, 0.8);
    border-radius: 50px;
    padding: 6px 12px 6px 16px;
    box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.1), 0 2px 8px -1px rgba(15, 23, 42, 0.05);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.search-bar:focus-within {
    border-color: #3b82f6;
    background: #ffffff;
    box-shadow: 0 10px 25px -5px rgba(59, 130, 246, 0.25), 0 8px 10px -6px rgba(59, 130, 246, 0.15);
}

.search-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    margin-right: 8px;
}

.search-input {
    flex: 1;
    border: none;
    outline: none;
    background: transparent;
    font-size: 15px;
    padding: 8px 0;
    color: #0f172a;
    font-weight: 500;
}

.search-input::placeholder {
    color: #94a3b8;
}

/* Toggle switch for simulated "Now" */
.now-toggle {
    display: flex;
    align-items: center;
    gap: 6px;
    border: 1px solid #e2e8f0;
    background: #f8fafc;
    color: #64748b;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    user-select: none;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02);
}

.now-toggle:hover {
    background: #f1f5f9;
    border-color: #cbd5e1;
    color: #334155;
}

.now-toggle.active {
    background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
    border-color: #2563eb;
    color: #ffffff;
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.35);
}

.pulse-dot {
    width: 7px;
    height: 7px;
    background-color: #4ade80;
    border-radius: 50%;
    display: inline-block;
    animation: pulse 1.6s infinite;
}

@keyframes pulse {
    0% {
        transform: scale(0.95);
        box-shadow: 0 0 0 0 rgba(74, 222, 128, 0.7);
    }
    70% {
        transform: scale(1);
        box-shadow: 0 0 0 5px rgba(74, 222, 128, 0);
    }
    100% {
        transform: scale(0.95);
        box-shadow: 0 0 0 0 rgba(74, 222, 128, 0);
    }
}

/* Results dropdown panel */
.results-dropdown {
    position: absolute;
    top: calc(100% + 10px);
    left: 0;
    right: 0;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(226, 232, 240, 0.8);
    border-radius: 16px;
    box-shadow: 0 20px 25px -5px rgba(15, 23, 42, 0.12), 0 10px 10px -5px rgba(15, 23, 42, 0.06);
    max-height: 350px;
    overflow-y: auto;
    padding: 8px;
    display: flex;
    flex-direction: column;
    gap: 4px;
}

/* Scrollbar styling */
.results-dropdown::-webkit-scrollbar {
    width: 6px;
}
.results-dropdown::-webkit-scrollbar-track {
    background: transparent;
}
.results-dropdown::-webkit-scrollbar-thumb {
    background: #cbd5e1;
    border-radius: 10px;
}
.results-dropdown::-webkit-scrollbar-thumb:hover {
    background: #94a3b8;
}

.result-item {
    display: flex;
    flex-direction: column;
    padding: 12px 14px;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.2s ease;
    border-left: 3px solid transparent;
}

.result-item:hover {
    background: rgba(59, 130, 246, 0.06);
    border-left-color: #3b82f6;
    transform: translateX(2px);
}

.result-title {
    font-size: 14px;
    font-weight: 600;
    color: #1e293b;
    margin-bottom: 4px;
    line-height: 1.4;
}

.result-details {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    align-items: center;
}

.result-badge {
    padding: 2px 8px;
    border-radius: 6px;
    font-size: 11px;
    font-weight: 500;
    line-height: 1.2;
}

.result-badge.type {
    background: #f1f5f9;
    color: #475569;
}

.result-badge.room {
    background: #eff6ff;
    color: #1e40af;
}

.result-badge.professor {
    background: #fdf2f8;
    color: #9d174d;
}

.result-badge.time {
    background: #faf5ff;
    color: #6b21a8;
}

.result-badge.now {
    background: #dcfce7;
    color: #166534;
    font-weight: 600;
    display: inline-flex;
    align-items: center;
    gap: 3px;
}

.result-description {
    font-size: 11px;
    color: #64748b;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 100%;
}

.no-results {
    padding: 20px;
    text-align: center;
    color: #64748b;
    font-size: 14px;
    font-weight: 500;
}
</style>