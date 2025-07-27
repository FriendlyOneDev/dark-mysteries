<template>
  <div class="wrapper">
    <MessageHistory :messages="history"/>
    <MessageInput @message="message"/>
  </div>
</template>
<style scoped>
  .wrapper{
    max-width: 720px;
    margin: auto;

    display: flex;
    flex-direction: column;
    height: 100vh;

    padding: 20px 0;
    box-sizing: border-box;
  }
  .history{
    flex: 1;
  }
  .message-box{
    flex-shrink: 0;
  }
</style>
<script setup>
  import { reactive } from 'vue';
  
  import MessageHistory from '../components/MessageHistory.vue';
  import MessageInput from '../components/MessageInput.vue';

  const history = reactive([]);

  function message(text){
    history.push({ text, type: true });
  }
</script>