import { onBeforeRouteUpdate, onBeforeRouteLeave, useRoute } from 'vue-router';
import { ref, shallowRef } from "vue";

export function useFetcher(initialize){
  const status = ref(), data = ref(), loader = async (route) => {
    return (await initialize(route)).json();
  }

  function update(route){
    status.value = { done: false };
    loader(route)
      .then((outcome) => {
        status.value = { done: true };
        data.value = outcome;
      })
      .catch((error) => status.value = { done: true, error });
  }

  update(useRoute());
  onBeforeRouteUpdate((route) => update(route));

  return { status, data };
}

export function useSocket(initialize){
  const status = ref(), socket = shallowRef(null);

  function update(route){
    let websocket = initialize(route);
    status.value = { done: false };

    websocket.addEventListener('open', () => {
      status.value = { done: true }
    });
    websocket.addEventListener('error', (error) => {
      status.value = { done: true, error }
    });

    socket.value = websocket;
  }

  onBeforeRouteUpdate((route) => {
    socket.value.close();
    socket.value = null;

    update(route);
  });
  onBeforeRouteLeave(() => {
    socket.value.close();
  });
  update(useRoute());

  return { status, socket }
}