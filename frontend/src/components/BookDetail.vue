<script setup lang="ts">
import { useFetch } from '@vueuse/core';
import { computed, ref, watch} from 'vue';
import { type BookAvailability, type Book } from './types';

import { Badge } from '@/components/ui/badge'
import Skeleton from './ui/skeleton/Skeleton.vue';
import Button from './ui/button/Button.vue';
import { ArrowUpRight, CircleQuestionMark, CircleQuestionMarkIcon, RotateCcw, Search } from 'lucide-vue-next';

import {
  HoverCard,
  HoverCardContent,
  HoverCardTrigger,
} from '@/components/ui/hover-card'
import { toast } from 'vue-sonner';
import Spinner from './ui/spinner/Spinner.vue';
import Card from './ui/card/Card.vue';
import CardHeader from './ui/card/CardHeader.vue';
import CardTitle from './ui/card/CardTitle.vue';
import CardDescription from './ui/card/CardDescription.vue';
import CardContent from './ui/card/CardContent.vue';
import CardAction from './ui/card/CardAction.vue';

const bookCoverAPILink = 'https://covers.openlibrary.org/b/id';

const url = import.meta.env.VITE_API_URL;

const props = defineProps<{
  bookid: number
}>()

const imgLoaded = ref(false);

const bookUrl = computed(() => {
  return `${url}/books/${props.bookid}`
})

const {isFetching, error, data} = 
  useFetch(bookUrl, {refetch: true})
  .get()
  .json<Book>();

watch(() => error.value, (newError) => {
  if (!!newError) {
    toast.error(newError);
  }
})

const bookCoverLink = computed(() => {
  return data.value ? `${bookCoverAPILink}/${data.value.coverid}-M.jpg?default=false` : ""
})


// getting the book availability
const nlbLoading = ref(false);
const nlbError = ref("");
const bookAvailability = ref<BookAvailability | null>(null);
const isSearched = ref(false);

async function getNlbAvailability() {
  nlbLoading.value = true;
  nlbError.value = "";
  bookAvailability.value = null;
  isSearched.value = true;

  const { error, data, statusCode } =
    await useFetch(`${url}/books/${props.bookid}/availability`)
    .get()
    .json<BookAvailability>()

  if (statusCode.value == 404) {
    nlbError.value = "Book currently unavailable at NLB.";
  } else if (statusCode.value == 429) {
    nlbError.value = "Ran out of NLB API requests. Please try again later."
  } else if (error.value) {
    nlbError.value = error.value;
  } else if (data.value?.libraries.length == 0) {
    nlbError.value = "Book fully loaned at NLB. Please try again later."
  }

  bookAvailability.value = data.value;
  
  nlbLoading.value = false;
}

</script>

<template>
  <div class="flex flex-col" v-if="isFetching || error">
    <div class="flex flex-col md:flex-row gap-8">
      <div class="flex-1 w-40 md:w-full">
        <Skeleton class="w-full h-full rounded aspect-2/3"/>
      </div>
    
      <div class="flex-2">
        <div class="grid gap-2 w-full">
          <Skeleton class="h-15" />
          <Skeleton class="h-5" />
          <Skeleton class="h-7 my-4" />
          <Skeleton class="h-5" />
          <Skeleton class="h-5" />
          <Skeleton class="h-5" />
          <Skeleton class="h-5" />
        </div>
      </div>

    </div>
    <Skeleton class="h-25 mt-4" />
  </div>  
  <div class="flex flex-col items-start" v-else-if="!error">
    <div class="flex flex-col md:flex-row gap-8">
      <div class="flex-1 w-40 md:w-full">
        <Skeleton class="w-full h-full rounded aspect-2/3" v-if="!imgLoaded"/>
        <img 
          :src="bookCoverLink"
          class="w-auto h-auto block rounded object-cover"
          v-show="imgLoaded"
          @load="imgLoaded = true"
          @error="imgLoaded = false">
      </div>
    
      <div class="flex-2">
        <div class="text-xl font-bold">{{ data?.title }}</div>
        <div>{{ data?.authors }}</div>
        <div class="flex flex-wrap gap-1 my-4">
          <Badge
            v-for="genre in data?.genres"
            :key="genre.genreid">
            {{ genre.name }}
          </Badge>
        </div>
        
        <div class="flex items-center gap-1">
          <span class="font-semibold">Average Rating </span>
          <span>{{ data?.averagerating }} / 5</span>
          <span class="text-muted-foreground">({{ data?.ratingscount }} ratings)</span>
          <HoverCard>
            <HoverCardTrigger>  
              <CircleQuestionMark class="ml-1"></CircleQuestionMark>
            </HoverCardTrigger>
            <HoverCardContent class="text-sm font-semibold">
              Average rating of the book on goodreads.com
            </HoverCardContent>
          </HoverCard>
        </div>

        <div class="my-1 md:my-0 flex items-start gap-1">
          <span class="font-semibold">Weighted Rating</span>
          <span>{{ data?.weightedscore.toFixed(2) }} / 5</span>
          <HoverCard>
            <HoverCardTrigger>  
              <CircleQuestionMark class="ml-1"></CircleQuestionMark>
            </HoverCardTrigger>
            <HoverCardContent class="w-fit">
              <p class="text-sm font-semibold">
                Re-centered average rating (center at 3)
              </p>
              <p class="mt-1 text-sm">
                Weighted Rating > 3 (better than average)
              </p>
              <p class="text-sm">
                Weighted Rating < 3 (worse than average)
              </p>
            </HoverCardContent>
          </HoverCard>
        </div>
        <p class="my-1 md:my-0">
          <span class="font-semibold">ISBN </span>
          <span>{{ data?.isbn }}</span>
        </p>
        <p>
          <span class="font-semibold">Goodreads ID </span>
          <Button variant="link" class="p-0 h-auto inline-flex align-baseline">
            <a
              :href="`https://goodreads.com/book/show/${data?.goodreadsbookid}`"
              target="_blank"
              rel="noopener noreferrer"
              class="inline-flex">
              {{ data?.goodreadsbookid }}
              <ArrowUpRight />
            </a>
          </Button>
        </p>
      </div>
    </div>

    <Card class="w-full mt-4">
      <CardHeader>
        <CardTitle>
          NLB Availability
        </CardTitle>
        <CardDescription>
          Availability may not be fully accurate as BookRank searches by title and author, instead of ISBN or BRN.
        </CardDescription>
        <CardAction>
          <Button @click="getNlbAvailability" variant="outline" size="icon" class="rounded-full">
            <Spinner v-if="nlbLoading" />
            <RotateCcw v-else-if="isSearched" />
            <Search v-else/>
          </Button>
        </CardAction>
      </CardHeader>
      <CardContent>
        <div>
          {{ nlbError }}
        </div>
        <div v-if="bookAvailability?.brn" class="grid">
          <div>
            <span class="font-semibold">BRN </span>
            <Button variant="link" class="p-0">
              <a :href="`https://catalogue.nlb.gov.sg/search/card?recordId=${bookAvailability?.brn}`" target="_blank">
                <span>{{ bookAvailability?.brn }}</span>
              </a>
            </Button>
          </div>
          
          <div class="flex flex-wrap gap-1 my-2">
            <Badge
              v-for="lib in bookAvailability?.libraries"
              :key="lib">
              {{ lib }}
            </Badge>
          </div>
        </div>
      </CardContent>
    </Card>
  </div>
  
</template>


<style>

</style>