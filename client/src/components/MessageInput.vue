<template>
  <form @submit.prevent="send" class="message-send">
    <input v-model="message" class="message-input" placeholder="type" />
    <button type="submit" class="btn-icon">
      <SendIcon class="icon"/>
    </button>
  </form>
</template>
<style scoped>
  .message-send{
    display: flex;
    gap: 10px;
  }
  .message-input{
    flex: 1;
    background-color: var(--primary-color);
    border-radius: 3px;
    padding: 10px;
  }
</style>
<script setup>
  import { ref } from 'vue';
  import SendIcon from '../assets/send.svg';

  const message = ref('');
  const emit = defineEmits(['message']);

  function send(){
    if(!message.value) return;
    
    emit('message', message.value);
    message.value = '';
  }
</script>