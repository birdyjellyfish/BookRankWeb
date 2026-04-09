import { ref } from "vue";

export function useNlbSearch(isbn: string, title: string, authors: string) {
  // 2-stage book search
  // first directly check availbility via isbn
  // if not fall back to title search
  const loading = ref(false);
  const availbility = ref<string[]>([]);
  const error = ref("");
  
}