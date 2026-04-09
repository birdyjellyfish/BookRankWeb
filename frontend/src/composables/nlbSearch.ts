import { ref } from "vue";

const availibilityUrl = "https://openweb.nlb.gov.sg/api/v2/Catalogue/GetAvailabilityInfo"

export function useNlbSearch() {
  // 2-stage book search
  // first directly check availibility via isbn
  // if not fall back to title search
  const loading = ref(false);
  const availbility = ref<string[]>([]);
  const error = ref("");

  async function getBookAvailibiity(isbn: string, authors: string, title: string) {
    loading.value = true;
    availbility.value = [];
    error.value = "";

    //left pad isbn with 0 to make it isbn10
    isbn = isbn.padStart(10, '0');

    // first directly check availibility via isbn
    try {
      const response = await fetch(`${availibilityUrl}?ISBN=${isbn}`, {
        method: "GET",
        headers: {
          "X-Api-Key":
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
  
}