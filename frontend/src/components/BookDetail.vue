<script setup lang="ts">
import { useFetch } from '@vueuse/core';
import { computed, ref, watch} from 'vue';
import type { Book } from './types';

import { Badge } from '@/components/ui/badge'
import Skeleton from './ui/skeleton/Skeleton.vue';
import Button from './ui/button/Button.vue';
import { ArrowUpRight, CircleQuestionMark, CircleQuestionMarkIcon } from 'lucide-vue-next';

import {
  HoverCard,
  HoverCardContent,
  HoverCardTrigger,
} from '@/components/ui/hover-card'
import { toast } from 'vue-sonner';
import { useNlbSearch } from '@/composables/nlbSearch';

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
const {
  loading: nlbLoading,
  availability,
  error: nlbError,
  getBookAvailability
} = useNlbSearch();

watch(() => data.value, (newData) => {
  if (!newData) {
    availability.value = [];
    return;
  }

  getBookAvailability(newData.isbn, newData.authors, newData.title);
})

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
    
  <div>
    <p>
      Book Availability
    </p>
    <div v-if="nlbError">
      {{ nlbError }}
    </div>
    <Skeleton v-else-if="nlbLoading" />
    <div v-else-if="availability.length == 0">
      Book currently unavailable at NLB.
    </div>
    <div v-else class="flex flex-wrap gap-1 my-4">
      <Badge
        v-for="lib in availability"
        :key="lib">
        {{ lib }}
      </Badge>
    </div>

  </div>

  </div>
  
</template>


<style>

</style>