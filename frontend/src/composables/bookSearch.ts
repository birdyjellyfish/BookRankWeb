import { computed, watch, type Ref } from "vue"
import { refDebounced, useFetch } from "@vueuse/core";
import type { BookSearch } from "@/components/types";

const url = import.meta.env.VITE_API_URL;

export function useBookSearch(title: Ref<string>) {
  const debouncedSearch = refDebounced(title, 300);

  const searchUrl = computed(() => `${url}/books?search=${debouncedSearch.value}`)

  watch(searchUrl, (value) => {
    console.log(value);
  })



  const { isFetching, error, data } = 
    useFetch(searchUrl, { refetch: true })
      .get()
      .json<BookSearch>();

  // unpack data
  const bookResults = computed(() => data.value?.results ?? []);

  return { bookResults, error, loading: isFetching }
}