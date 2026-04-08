<script setup lang="ts">
import { useReadlist } from '@/composables/readlistRecord';
import BookSearch from './BookSearch.vue';
import { ref, watch, type Ref } from 'vue';
import type { BookLite } from './types';

import DialogTitle from './ui/dialog/DialogTitle.vue';
import DialogHeader from './ui/dialog/DialogHeader.vue';

import type { DateValue } from '@internationalized/date'
import { DateFormatter, getLocalTimeZone, today } from '@internationalized/date'
import { ArrowDown, CalendarIcon, Check, ChevronDown } from 'lucide-vue-next'
import { cn } from '@/lib/utils'
import { Button } from '@/components/ui/button'
import { Calendar } from '@/components/ui/calendar'
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover'
import DialogDescription from './ui/dialog/DialogDescription.vue';
import Spinner from './ui/spinner/Spinner.vue';

const defaultPlaceholder = today(getLocalTimeZone())
const date = ref() as Ref<DateValue>
const df = new DateFormatter('en-US', {
  dateStyle: 'long',
})

const {error, loading, success, data, fetchRecords, addRecord} = useReadlist();

const selectedBook = ref<BookLite | null>(null);
const datefinished = ref<string | null>(null);

const emit = defineEmits(['refresh', 'close']);

watch([selectedBook, datefinished], () => {
  error.value = "";
  loading.value = false;
  success.value = ""
})

async function handleSubmit() {
  if (!selectedBook.value) {
    error.value = "Book title must be provided."
    return;
  }

  await fetchRecords();

  // check if book already in read list
  if (data.value.find(record => record.bookid === selectedBook.value?.bookid)) {
    error.value = 'Book already in read list.'
    return;
  }

  if (!date.value) {
    datefinished.value = null;
  } else {
    datefinished.value = date.value.toString();
  }

  await addRecord(selectedBook.value.bookid, datefinished.value);
  emit('refresh');
  setTimeout(() => {
    emit('close')
  }, 500)
}

</script>

<template>
  <DialogHeader>
    <DialogTitle>
      Add to read list
    </DialogTitle>
    <DialogDescription class="min-h-10">
      <p v-if="error">{{ error }}</p>
      <p v-else-if="success">
        Successully added to read list.
      </p>
    </DialogDescription>
  </DialogHeader>

  <form @submit.prevent="handleSubmit" class="grid gap-2">
    <BookSearch
      v-model="selectedBook"
      required
      :prompt="'Search books/authors'" />
    <Popover v-slot="{ close }">
      <PopoverTrigger as-child>
        <Button
          variant="outline"
          :class="cn('w-100 justify-between font-normal', !date && 'text-muted-foreground')"
        >
          <CalendarIcon />
          {{ date ? df.format(date.toDate(getLocalTimeZone())) : "Date finished" }}
          <ChevronDown class="ml-2 h-4 w-4 shrink-0"></ChevronDown>
        </Button>
      </PopoverTrigger>
      <PopoverContent class="w-100 p-0" align="start">
        <Calendar
          v-model="date"
          :default-placeholder="defaultPlaceholder"
          layout="month-and-year"
          initial-focus
          @update:model-value="close"
        />
      </PopoverContent>
    </Popover>
    
    <div class="mt-8">
      <Button disabled class="w-full" v-if="success"><Check /></Button>
      <Button
        class="w-full"
        type="submit"
        v-else-if="!loading">
        Add to read list
      </Button>
      <Button disabled class="w-full" v-if="loading"><Spinner /></Button>
    </div>
    
  </form>

  
</template>

