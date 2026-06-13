<template>
    <div id="app-info" class="coordinates app-info">
      <button class="close-btn" @click="$emit('close')">&times;</button>
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
      <pre class="app-description">{{ conteudo.description }}</pre>
    </div>
  </template>
  
  <script setup>
    import { defineProps, defineEmits } from 'vue'
  
  defineProps({
    conteudo: {
      type: Object,
      required: true,
      default: () => ({
        img: 'https://i.ytimg.com/vi/lHKajh0XyUE/hq720.jpg?sqp=-oaymwE7CK4FEIIDSFryq4qpAy0IARUAAAAAGAElAADIQj0AgKJD8AEB-AH-CYAC0AWKAgwIABABGE4gZSgyMA8=&rs=AOn4CLApVXxQq5IVWY4hOw1zwHuDSYzTsg',
        build: '',
        description: ''
      })
    }
  })

  defineEmits(['close']);
  
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
   z-index: 1;
}

.slide-enter-active,
.slide-leave-active {
  transition: transform 0.3s ease;
}

.slide-enter-from,
.slide-leave-to {
  transform: translateX(-100%);
}

.close-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  background: white;
  border: 1px solid #ccc;
  border-radius: 50%;
  width: 30px;
  height: 30px;
  font-size: 20px;
  cursor: pointer;
  z-index: 1001;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 5px rgba(0,0,0,0.2);
}

.close-btn:hover {
  background: #f0f0f0;
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
   font-size: 1.375rem;
   font-weight: 400;
   letter-spacing: 0rem;
   line-height: 1.75rem;
   padding: 16px 24px 8px 24px;
   margin: 0;
}

.app-description {
   padding: 0 24px;
   white-space: pre-wrap;
   font-family: inherit;
   font-size: 1rem;
   color: #555;
}

</style>