import type { BookUser } from "@/components/types";
import { getCSRFToken } from "@/stores/auth";
import { useFetch } from "@vueuse/core";
import { ref } from "vue"

const url = `${import.meta.env.VITE_API_URL}/readlist`;

export function useReadlist() {
  const loading = ref<boolean>(false);
  const error = ref<string>("");
  const success = ref<string>("");
  const data = ref<BookUser[]>([]);
  
  async function fetchRecords() {
    loading.value = true;
    error.value = "";
    success.value = "";
    data.value = [];

    try {
      const response = await fetch(`${url}/`, {
        method: "GET",
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCSRFToken()
        },
        credentials: 'include'
      })

      if (!response.ok) {
        throw new Error(`Response status: ${response.status}`)
      } else {
        success.value = "Successfully retrieved book records.";
        data.value = await response.json();
      }
    } catch (err) {
      error.value = (err as Error).message;
    } finally {
      loading.value = false;
    }
  }

  async function addRecord(bookid: number, datefinished: string | null = null) {
    loading.value = true;
    error.value = "";
    success.value = "";
    data.value = [];

    try {
      const response = await fetch(`${url}/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCSRFToken()
        },
        credentials: 'include',
        body: JSON.stringify({
          bookid,
          datefinished
        })
      })

      if (!response.ok) {
        throw new Error(`Response status: ${response.status}`)
      } else {
        success.value = "Successfully added book record.";
      }
    } catch (err) {
      error.value = (err as Error).message;
      console.log(error.value)
    } finally {
      loading.value = false;
    }
  }
  

  async function editRecord(bookid: number, datefinished: string | null = null) {
    loading.value = true;
    error.value = "";
    success.value = "";
    data.value = [];

    try {
      const response = await fetch(`${url}/${bookid}/`, {
        method: "PATCH",
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCSRFToken()
        },
        credentials: 'include',
        body: JSON.stringify({
          datefinished
        })
      })

      if (!response.ok) {
        throw new Error(`Response status: ${response.status}`)
      } else {
        success.value = "Successfully edited book record.";
      }
    } catch (err) {
      error.value = (err as Error).message;
    } finally {
      loading.value = false;
    }
  }

  async function deleteRecord(bookid: number) {
    loading.value = true;
    error.value = "";
    success.value = "";
    data.value = [];

    try {
      const response = await fetch(`${url}/${bookid}/`, {
        method: "DELETE",
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCSRFToken()
        },
        credentials: 'include'
      })

      if (!response.ok) {
        throw new Error(`Response status: ${response.status}`)
      } else {
        success.value = "Successfully deleted book record.";
      }
    } catch (err) {
      error.value = (err as Error).message;
    } finally {
      loading.value = false;
    }
  }

  return {loading, error, success, data, addRecord, editRecord, deleteRecord, fetchRecords};
}