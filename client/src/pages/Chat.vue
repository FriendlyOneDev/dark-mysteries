<template>
  <Curtain :status="status">
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
  import { reactive, ref } from 'vue';
  import { onBeforeRouteLeave, onBeforeRouteUpdate, useRoute } from 'vue-router';
  
  import Curtain from '../components/Curtain.vue';
  import MessageHistory from '../components/MessageHistory.vue';
  import MessageInput from '../components/MessageInput.vue';

  const status = ref('loading');
  const ignore = ref(true);
  const history = reactive([]);

  let websocket = connect(useRoute().params.id);

  function connect(id){
    let socket = new WebSocket(`/ws/${id}`);
    status.value = 'loading';
  
    socket.addEventListener('open', () => {
      status.value = 'done';
    });
    socket.addEventListener('error', () => {
      status.value = 'error';
    });
    socket.addEventListener('close', (event) => {
      status.value = 'error';
    });
    
    socket.addEventListener('message', (event) => {
      if(!ignore.value){
        history.push({ text: JSON.parse(event.data).answer, type: false });
      }
    });

    return socket;
  }

  function message(text){
    ignore.value = false;
    history.push({ text, type: true });

    websocket.send(text);
  }

  onBeforeRouteUpdate((to) => {
    websocket.close();

    ignore.value = true;
    history.length = 0;

    websocket = connect(to.params.id);
  });
  onBeforeRouteLeave(() => {
    websocket.close();
  });
</script>