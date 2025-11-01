<template>
  <main>
    <MapaSimples />
  </main>
</template>

<script setup>
import MapaSimples from './components/MapView.vue';
</script>

<style>
/* Estilos globais se necessário */
body {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin: 0;
  overflow: hidden;
}

main {
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>