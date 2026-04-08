import { ref } from "vue"
import type { BookLite } from "../components/types"
import { getCSRFToken } from "@/stores/auth";

const url = import.meta.env.VITE_API_URL;

export function useRecommender() {
  const bookResults = ref<BookLite[]>([]) // just the books
  const loading = ref(false);
  const error = ref<string | null>(null);

  async function fetchRecs(lastread: number, genre: number | null = null, n: number = 10, k: number = 100) {
    loading.value = true;
    error.value = null;
    
    try {
      const response = await fetch(`${url}/recommender/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCSRFToken()
        },
        credentials: 'include',
        body: JSON.stringify({
          lastread,
          genre,
          n,
          k
        })

      })

      if (!response.ok) {
        throw new Error(`Response status: ${response.status}`);
      }
      
      bookResults.value = await response.json(); // may be empty list if no recs

    } catch (err) {
      error.value = (err as Error).message;
    } finally {
      loading.value = false;
    }
  }

  return { bookResults, loading, error, fetchRecs }
}