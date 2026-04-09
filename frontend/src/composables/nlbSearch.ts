import { ref } from "vue";

const availibilityUrl = "https://openweb.nlb.gov.sg/api/v2/Catalogue/GetAvailabilityInfo";
const searchUrl = "https://openweb.nlb.gov.sg/api/v2/Catalogue/SearchTitles";
const NLB_APIKEY = import.meta.env.VITE_NLB_APIKEY;
const NLB_APPCODE = import.meta.env.VITE_NLB_APPCODE;

export function useNlbSearch() {
  // 2-stage book search
  // first directly check availibility via isbn
  // if not fall back to title search
  const loading = ref(false);
  const availibility = ref<string[]>([]);
  const error = ref("");

  async function getBookAvailibiity(isbn: string, authors: string, title: string) {
    loading.value = true;
    availibility.value = [];
    error.value = "";

    //left pad isbn with 0 to make it isbn10
    isbn = isbn.padStart(10, '0');

    // first directly check availibility via isbn
    try {
      const response = await fetch(`${availibilityUrl}?ISBN=${isbn}`, {
        method: "GET",
        headers: {
          "X-Api-Key": NLB_APIKEY,
          "X-App-Code": NLB_APPCODE
        }
      })

      if (response.ok) {
        const data = await response.json();

        // unpack data
        for (var item of data['items']) {
          if (item['transactionStatus']['code'] == 'S') {
            availibility.value.push(item['location']['name'])
          }
        }
      }
    } catch (err) {
      error.value = (err as Error).message;
    }

    // if cannot find by isbn try title and author search
    if (availibility.value.length != 0) {
      loading.value = false;
      return;
    }

    // clean title remove brackets and text within
    title = title.replace(/\(.*?\)/g, '');
    var brn = "";

    try {
      const response = await fetch(`${searchUrl}?Keywords=${title.concat(' ', authors)}&MaterialTypes=bks`, {
        method: "GET",
        headers: {
          "X-Api-Key": NLB_APIKEY,
          "X-App-Code": NLB_APPCODE
        }
      })

      if (response.ok) {
        const data = await response.json();

        // unpack data
        for (var book of data['titles']) {
          if (title === book['title']) {
            brn = book['records'][0]['brn'];
            break;
          }
        }
      } else {
        throw new Error(`Response status: ${response.status}`)
      }
    } catch (err) {
      error.value = (err as Error).message;
    }

    // find availibility by brn
    if (error.value != "" || brn == "") {
      loading.value = false;
      return;
    }

    try {
      const response = await fetch(`${availibilityUrl}?BRN=${brn}`, {
        method: "GET",
        headers: {
          "X-Api-Key": NLB_APIKEY,
          "X-App-Code": NLB_APPCODE
        }
      })

      if (response.ok) {
        const data = await response.json();

        // unpack data
        for (var item of data['items']) {
          if (item['transactionStatus']['code'] == 'S') {
            availibility.value.push(item['location']['name'])
          }
        }
      } else {
        throw new Error(`Response status: ${response.status}`);
      }

    } catch (err) {
      error.value = (err as Error).message;
    } finally {
      loading.value = false;
    }
  } 

  return { loading, availibility, error, getBookAvailibiity }
  
}