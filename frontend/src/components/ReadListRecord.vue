<script setup lang="ts">
import BookDetail from './BookDetail.vue';
import { Book, type BookUser } from './types';
import { computed, onMounted, ref, watch, type Ref } from 'vue';
import { useReadlist } from '@/composables/readlistRecord';

import type { DateValue } from '@internationalized/date'
import { CalendarDate, DateFormatter, getLocalTimeZone, today } from '@internationalized/date'
import { CalendarIcon } from 'lucide-vue-next'
import { cn } from '@/lib/utils'
import { Button } from '@/components/ui/button'
import { Calendar } from '@/components/ui/calendar'
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover'

import {
  ButtonGroup,
  ButtonGroupSeparator,
  ButtonGroupText,
} from '@/components/ui/button-group'

import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from '@/components/ui/alert-dialog'
import Spinner from './ui/spinner/Spinner.vue';
import { toast } from 'vue-sonner';

const defaultPlaceholder = today(getLocalTimeZone())
const date = ref() as Ref<DateValue>
const df = new DateFormatter('en-US', {
  dateStyle: 'long',
})

const record = defineModel<BookUser>('record', {required: true});

const datefinished = ref<string | null>(record.value.datefinished);

const dateChanged = ref(false);

function toYYYYMMDD(date: DateValue | undefined) {
  if (!date) return null;
  return `${date.year}-${String(date.month).padStart(2, "0")}-${String(date.day).padStart(2, "0")}`;
}

watch(() => date.value, (newDate) => {
  error.value = "";
  success.value = "";

  // check if newDate and datefinished are the same
  // newDate is undefined and datefinished is null
  // or newDate == current datefinished
  dateChanged.value  = (toYYYYMMDD(newDate) !== datefinished.value) ;
})

const {error, loading, success, editRecord, deleteRecord} = useReadlist();

const emit = defineEmits(['refresh', 'close'])

async function handleDateChange() {
  success.value = "";
  error.value = "";

  if (!date.value) {
    datefinished.value = null;
  } else {
    datefinished.value = date.value.toString();
  }
  
  await editRecord(record.value.bookid, datefinished.value);
  dateChanged.value = false;
  emit('refresh');
  
  if (success.value) {
    toast.success("Date successfully edited.")
  }

  if (error.value) {
    toast.error(error);
  }
}

const open = ref(false);

async function handleDelete() {
  success.value = "";
  error.value = "";
  
  await deleteRecord(record.value.bookid);
  emit('refresh');
  emit('close');

  if (success.value) {
    toast.success("Record successfully deleted.")
  }

  if (error.value) {
    toast.error(error);
  }
  
}

onMounted(() => {
  if (!datefinished.value) return;

  const [y, m, d] = datefinished.value.split('-').map(Number);
  date.value = new CalendarDate(y, m, d);
})

</script>

<template>
  <div class="grid gap-4 md:gap-10">
    <BookDetail :bookid="record.bookid"></BookDetail>

    <div class="flex flex-col sm:flex-row gap-3">
       <Popover v-slot="{ close }">
        <PopoverTrigger as-child>
          <Button
            variant="outline"
            :class="cn('w-[240px] justify-start text-left font-normal', !date && 'text-muted-foreground')"
          >
            <CalendarIcon />
            {{ date ? df.format(date.toDate(getLocalTimeZone())) : "Date finished" }}
          </Button>
        </PopoverTrigger>
        <PopoverContent class="w-auto p-0" align="start">
          <Calendar
            v-model="date"
            :default-placeholder="defaultPlaceholder"
            layout="month-and-year"
            initial-focus
            @update:model-value="close"
          />
        </PopoverContent>
      </Popover>

      <ButtonGroup class="grid grid-cols-2 w-30">
        <Button
          variant="default"
          v-if="dateChanged"
          @click="handleDateChange">
          Edit
        </Button>
        <Button
          variant="default"
          v-else-if="loading"
          disabled>
          <Spinner />
        </Button>
        <Button
          variant="default"
          v-else
          disabled>
          Edit
        </Button>

        <Button
          variant="destructive"
          @click="open = true">
          Delete
        </Button>
      </ButtonGroup>
    </div>
  </div>

  <AlertDialog v-model:open="open">
    <AlertDialogContent>
      <AlertDialogHeader>
        <AlertDialogTitle>Delete read record</AlertDialogTitle>
        <AlertDialogDescription>
          This action cannot be undone.
        </AlertDialogDescription>
      </AlertDialogHeader>
      <AlertDialogFooter>
        <AlertDialogCancel>Cancel</AlertDialogCancel>
        <AlertDialogAction @click="handleDelete">
          Delete
        </AlertDialogAction>
      </AlertDialogFooter>
    </AlertDialogContent>
  </AlertDialog>
</template>