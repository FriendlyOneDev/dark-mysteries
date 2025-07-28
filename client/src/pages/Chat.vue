<template>
  <Curtain v-bind="status">
    <div class="wrapper">
      <div class="preview">
        <span class="emoji">{{ data.emoji }}</span>
        <div class="description">{{ data.puzzle }}</div>
      </div>
      <div class="chat">
        <MessageHistory :messages="history"/>
        <MessageInput :disable="!turn" @message="message"/>
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

  .preview{
    display: flex;
    flex-direction: column;
    justify-content: center;

    gap: 10px;
  }
  .emoji{
    font-size: 128px;
    align-self: center;
  }
  .description{
    text-align: center;
  }

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

  @media (max-width: 540px){
    .wrapper{
      flex-direction: column;
    }
    .preview{
      flex-direction: row;
      flex: initial;
    }
    .emoji{
      font-size: 64px;
    }
  }
</style>
<script setup>
  import { computed, reactive, ref, watch } from 'vue';
  import { useSocket, useFetcher } from '../loader.js';
  
  import Curtain from '../components/Curtain.vue';
  import MessageHistory from '../components/MessageHistory.vue';
  import MessageInput from '../components/MessageInput.vue';

  const ANSWERS = {
    'bad': "I don't understand you. Try rephrasing your question",
    'yes': 'Yes',
    'no': 'No'
  }

  const ignore = ref(true);
  const turn = ref(true);
  const history = reactive([]);

  const {
    status: socketStatus, socket
  } = useSocket((route) => {
    if(import.meta.env.DEV){
      return new WebSocket(`/ws/${route.params.id}`);
    } else{
      return new WebSocket(`wss://dark-mysteries.onrender.com/ws/${route.params.id}`);
    }
  });
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
      turn.value = true;
    })
  }, { immediate: true })

  function message(text){
    ignore.value = false;
    turn.value = false;
    history.push({ text, type: true });

    if(WebSocket.OPEN == socket.value.readyState){
      socket.value.send(text)
    } else{
      status.value = { done: true, error: new Error() }
    }
  }
</script>