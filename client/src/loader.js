import { watch, ref } from "vue";

export default function(pointer, loader){
  const status = ref('loading');
  const data = ref(null);

  function reset(){
    status.value = 'loading';
    data.value = null;
  }
  function load(param){
    loader(param)
      .then((fetched) => {
        status.value = 'done';
        data.value = fetched;
      })
      .catch(() => status.value = 'error');
  }

  load(pointer())

  watch(pointer, (value) => {
    reset();
    load(value);
  });

  return { status, data }
}