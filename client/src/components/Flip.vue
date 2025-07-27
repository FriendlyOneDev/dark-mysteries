<template>
  <div class="flip-container">
    <div class="flip-card" :class="{ 'flipped': flipped }">
      <slot v-if="!flipped" name="front"></slot>
      <div v-else class="back-side">
        <slot name="back"></slot>
      </div>
    </div>
  </div>
</template>

<script setup>
  defineProps({
    flipped: {
      type: Boolean,
      default: false
    }
  })
</script>

<style scoped>
.flip-container {
  perspective: 1000px;
  width: 100%;
  height: 100%;
}

.flip-card {
  position: relative;
  width: 100%;
  height: 100%;
  transform-style: preserve-3d;
  transition: transform 0.6s cubic-bezier(0.4, 0.0, 0.2, 1);
  
  /* Glass-like card styling with white borders */
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  border: 2px solid rgba(255, 255, 255, 0.8);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  padding: 24px;
  box-sizing: border-box;
}

.flip-card.flipped {
  transform: rotateY(180deg);
}

/* Hover effect */
.flip-card:hover {
  border-color: rgba(255, 255, 255, 1);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

.flip-card.flipped:hover {
  transform: rotateY(180deg) translateY(-2px);
}

.back-side{
  transform: rotateY(180deg);
}
</style>