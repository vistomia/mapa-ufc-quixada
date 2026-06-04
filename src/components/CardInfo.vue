<template>
    <div id="app-info" class="coordinates app-info">
      <AppSearch></AppSearch>
      <div class="app-img">
        <img 
          decoding="async" 
          :src="conteudo.img" 
          style="position: absolute; top: 50%; left: 50%; width: 508px; height: 644px; transform: translateY(-50%) translateX(-50%);"
        >
      </div>
      <h1 class="app-title">
        {{ conteudo.build }}
      </h1>
      <p>{{ conteudo.description }}</p>
    </div>
  </template>
  
  <script setup>
    import { defineProps} from 'vue'  
  import AppSearch from './AppSearch.vue' // Lembre-se de importar o componente AppSearch se ele for local
  
  defineProps({
    conteudo: {
      type: Object,
      required: true,
      default: () => ({
        img: 'https://',
        build: '',
        description: ''
      })
    }
  })
  
  </script>


<style>
.app-info {
   position: absolute;
   top: 0;
   left: 0;
   width: 480px;
   height: 100%;
   background-color: white;
   box-shadow: 0 1px 3px rgba(60,64,67,0.3),0 2px 8px 2px rgba(60,64,67,0.15);
   display:none;
}


.app-img {
   position: relative;
   min-width: 100%;
   height: 270px;
   display: block; 
   overflow: hidden;
}

.app-title {
   font-family: Roboto,Arial,sans-serif;
   font-size: 13px;
   font-size: 1.375rem;
   font-weight: 400;
   letter-spacing: 0rem;
   line-height: 1.75rem;
   padding: 16px 24px;
}

</style>