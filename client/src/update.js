import { useRoute, onBeforeRouteUpdate } from 'vue-router'
import { markRaw, ref } from 'vue'

export default function(loader){
  const status = ref(), data = ref();

  function load(route){
    status.value = { done: false };
    data.value = undefined;

    loader(route)
      .then((outcome) => {
        status.value = { done: true };
        data.value = outcome;
      })
      .catch((error) => status.value = { done: true, error: markRaw(error) })
  }

  load(useRoute());
  onBeforeRouteUpdate((route) => load(route));

  return { status, data, redo: load }
}