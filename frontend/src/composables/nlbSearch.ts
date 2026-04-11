import { ref } from "vue";

const availabilityUrl = "https://openweb.nlb.gov.sg/api/v2/Catalogue/GetAvailabilityInfo";
const searchUrl = "https://openweb.nlb.gov.sg/api/v2/Catalogue/SearchTitles";
const NLB_APIKEY = import.meta.env.VITE_NLB_APIKEY;
const NLB_APPCODE = import.meta.env.VITE_NLB_APPCODE;

export function useNlbSearch() {
  // 2-stage book search
  // first directly check availability via isbn
  // if not fall back to title search
  const loading = ref(false);
  const availability = ref<string[]>([]);
  const error = ref("");

  async function getBookAvailability(isbn: string, authors: string, title: string) {
    loading.value = true;
    availability.value = [];
    error.value = "";

    // //left pad isbn with 0 to make it isbn10
    // isbn = isbn.padStart(10, '0');

    // // first directly check availability via isbn
    // try {
    //   const response = await fetch(`${availabilityUrl}?ISBN=${isbn}`, {
    //     method: "GET",
    //     headers: {
    //       "X-Api-Key": NLB_APIKEY,
    //       "X-App-Code": NLB_APPCODE
    //     }
    //   })

    //   if (response.ok) {
    //     const data = await response.json();

    //     // unpack data
    //     for (var item of data['items']) {
    //       if (item['transactionStatus']['code'] == 'S') {
    //         availability.value.push(item['location']['name'])
    //       }
    //     }
    //   }
    // } catch (err) {
    //   error.value = (err as Error).message;
    // }

    // // check if availability found
    // // otherwise if cannot find by isbn try title and author search
    // if (availability.value.length != 0) {
    //   loading.value = false;
    //   return;
    // }

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

    // find availability by brn
    if (error.value != "" || brn == "") {
      loading.value = false;
      return;
    }

    try {
      const response = await fetch(`${availabilityUrl}?BRN=${brn}`, {
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
            availability.value.push(item['location']['name'])
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

  return { loading, availability, error, getBookAvailability }
  
}