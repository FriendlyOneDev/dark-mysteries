<template>
  <Curtain v-bind="status">
    <div class="wrapper">
      <MessageHistory :messages="history"/>
      <MessageInput @message="message"/>
    </div>
  </Curtain>
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
  import { reactive, ref, watch } from 'vue';
  import { useSocket } from '../loader.js';
  
  import Curtain from '../components/Curtain.vue';
  import MessageHistory from '../components/MessageHistory.vue';
  import MessageInput from '../components/MessageInput.vue';

  const ignore = ref(true);
  const history = reactive([]);

  const { status, socket } = useSocket((route) => new WebSocket(`/ws/${route.params.id}`));

  watch(status, (websocket) => {
    if(!status.value.done) return;

    socket.value.addEventListener('message', (event) => {
      if(ignore.value) return;

      history.push({ text: JSON.parse(event.data).answer, type: false });
    })
  })

  function message(text){
    ignore.value = false;
    history.push({ text, type: true });

    socket.value.send(text);
  }
</script>