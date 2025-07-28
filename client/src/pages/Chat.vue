<template>
  <Curtain v-bind="status">
    <div class="wrapper">
      <Card class="preview" 
        :puzzle="data.puzzle"
        :emoji="data.emoji"
        :title="data.title"
      />
      <div class="chat">
        <MessageHistory :messages="history"/>
        <MessageInput @message="message"/>
      </div>
    </div>
  </Curtain>
</template>
<style scoped>
  .wrapper{
    height: 100vh;
    padding: 20px;
    box-sizing: border-box;

    display: flex;
    gap: 10px;
  }
  .chat { flex: 3; }
  .preview { flex: 1; }

  .chat{
    display: flex;
    flex-direction: column;
  }
  .history{
    flex: 1;
  }
  .message-box{
    flex-shrink: 0;
  }
</style>
<script setup>
  import { computed, reactive, ref, watch } from 'vue';
  import { useSocket, useFetcher } from '../loader.js';
  
  import Curtain from '../components/Curtain.vue';
  import Card from '../components/Card.vue';
  import MessageHistory from '../components/MessageHistory.vue';
  import MessageInput from '../components/MessageInput.vue';

  const ANSWERS = {
    'bad': "I don't understand you. Try rephrasing your question",
    'yes': 'Yes',
    'no': 'No'
  }

  const ignore = ref(true);
  const history = reactive([]);

  const { 
    status: socketStatus, socket
  } = useSocket((route) => new WebSocket(`/ws/${route.params.id}`));
  const { 
    status: fetchStatus, data
  } = useFetcher((route) => fetch(`/api/story/${route.params.id}`));

  const status = computed(() => ({
    done: socketStatus.value.done && fetchStatus.value.done,
    error: socketStatus.value.error ?? fetchStatus.value.error,
  }));

  watch(socket, (websocket) => {
    if(!websocket) return;

    websocket.addEventListener('message', (event) => {
      if(ignore.value) return;

      let { answer, solved } = JSON.parse(event.data);
      history.push({
        text: solved ? 'Congrats! You have solved it' : ANSWERS[answer],
        type: false
      });
    })
  }, { immediate: true })

  function message(text){
    ignore.value = false;
    history.push({ text, type: true });

    if(WebSocket.OPEN == socket.value.readyState){
      socket.value.send(text)
    } else{
      status.value = { done: true, error: new Error() }
    }
  }
</script>