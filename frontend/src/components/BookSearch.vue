<script setup lang="ts">
import { computed, ref, watch } from "vue"
import { useBookSearch } from "../composables/bookSearch"
import type { BookLite } from "./types"

import { BookOpen, CheckIcon, ChevronsUpDownIcon } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from '@/components/ui/command'
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover'
import { cn } from "@/lib/utils"

const open = ref(false);
const value = ref('');

const { prompt } = defineProps(['prompt'])

const cleanedTitle = computed(() => value.value.trim());
// useBookSearch handles debouncing of title
const { bookResults, loading, error } = useBookSearch(cleanedTitle)
const selectedBook = defineModel<BookLite | null>();

function selectBook(book: BookLite) {
  if (selectedBook.value?.bookid == book.bookid) {
    // handle deselect
    value.value = '';
    selectedBook.value = null;
  } else {
    value.value = book.title;
    selectedBook.value = book;
  }
 
  open.value = false;
}
</script>

<template>
  <Popover v-model:open="open">
    <PopoverTrigger as-child>
      <Button
        variant="outline"
        role="combobox"
        :aria-expanded="open"
        :class="cn('w-100 justify-between font-normal', !selectedBook && 'text-muted-foreground')"
      >
        <BookOpen/>
        <span v-if="selectedBook" class="truncate">
          <span class="font-semibold">{{ selectedBook.title }}</span>
          ({{ selectedBook.authors }})
        </span>
        <span v-else>{{ prompt }}</span>
        <ChevronsUpDownIcon class="ml-2 h-4 w-4 shrink-0" />
      </Button>
    </PopoverTrigger>
    <PopoverContent class="w-100 p-0">
      <Command :filter-function="() => 1">
        <CommandInput
          placeholder="Search books/authors..."
          :value="value"
          @update:model-value="(v : string) => value = v"
        />
        <CommandList>
          <CommandEmpty v-if="error">{{ error }}</CommandEmpty>
          <CommandEmpty v-else-if="bookResults.length === 0 && !!cleanedTitle">No results found.</CommandEmpty>
          <CommandGroup>
            <CommandItem
              v-for="book in bookResults"
              :key="book.bookid"
              :value="book.title"
              @select="selectBook(book)"
            >
              <CheckIcon
                :class="cn(
                  'mr-2 h-4 w-4',
                  selectedBook?.title === book.title ? 'opacity-100' : 'opacity-0',
                )"
              />
              <span>
                <span class="font-semibold">{{ book.title }}</span>
                ({{ book.authors }})
              </span>
            </CommandItem>
          </CommandGroup>
        </CommandList>
      </Command>
    </PopoverContent>
  </Popover>
</template>

<style scoped>

</style>