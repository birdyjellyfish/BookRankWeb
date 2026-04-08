<script setup lang="ts">
import ReadListView from '@/components/ReadListView.vue';
import { getCSRFToken, useAuthStore } from '@/stores/auth';
import { onMounted } from 'vue';

import {
  Empty,
  EmptyContent,
  EmptyDescription,
  EmptyHeader,
  EmptyMedia,
  EmptyTitle,
} from '@/components/ui/empty'
import { CircleUserRound } from 'lucide-vue-next';

import {
  Field,
  FieldContent,
  FieldDescription,
  FieldError,
  FieldGroup,
  FieldLabel,
  FieldLegend,
  FieldSeparator,
  FieldSet,
  FieldTitle,
} from '@/components/ui/field'

import Input from '@/components/ui/input/Input.vue';
import Button from '@/components/ui/button/Button.vue';
import Card from '@/components/ui/card/Card.vue';
import CardContent from '@/components/ui/card/CardContent.vue';
import { ref } from 'vue';
import { toast } from 'vue-sonner';
import CardHeader from '@/components/ui/card/CardHeader.vue';

const url = `${import.meta.env.VITE_API_URL}/users/resetpassword/`

const authStore = useAuthStore();

const newpassword = ref('');

const error = ref('');
const loading = ref(false);
const success = ref('');

async function handlePwdReset() {
  error.value = '';
  success.value = '';
  loading.value = true;

  // check if new password is blank
  if (newpassword.value === '') {
    error.value = 'New password cannot be empty.'
    return;
  }
  try {
    const response = await fetch(url, {
        method: "POST",
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCSRFToken()
        },
        credentials: 'include',
        body: JSON.stringify({
          'password': newpassword.value
        })
      })

      if (!response.ok) {
        throw new Error(`Response status: ${response.status}`)
      } else {
        success.value = 'Password changed successfully.'
        toast.success(success.value);

        // reset session auth
        const username = authStore.user?.username;

        if (!!username) {
          authStore.login(username, newpassword.value)
        }
        

      }
  } catch (err) {
    error.value = (err as Error).message;
    toast.error(error.value);
  } finally {
    loading.value = false;
    newpassword.value = '';
  }
}

onMounted(() => {
  authStore.fetchUser()
})

</script>

<template>
  <div class="grid gap-4">
    <h1 class="text-3xl px-6 font-bold">My Account Information</h1>

    <div class="h-95 md:h-120 px-6 flex flex-col" v-if="!authStore.isAuthenticated">
      <Empty class="border border-dashed mt-4">
        <EmptyHeader>
          <EmptyMedia variant="icon">
            <CircleUserRound></CircleUserRound>
          </EmptyMedia>
          <EmptyTitle>
            User not signed in
          </EmptyTitle>
          <EmptyDescription>
            Sign in / sign up to access your account information.
          </EmptyDescription>
        </EmptyHeader>
      </Empty>
    </div>

    <div class="grid gap-10" v-else>
      <Card class="pl-10 pr-10 shadow-xl mx-auto">
        <CardContent>
          <CardHeader class="font-semibold pb-2">Account Settings</CardHeader>
          <div class="w-80 md:w-150 lg:w-200 px-6">
            <FieldSet>
              <FieldGroup>
                <Field ckass="max-w-1/2">
                  <FieldLabel for="username">
                    Username
                  </FieldLabel>
                  <Input id="username" :model-value="authStore.user?.username" disabled />
                </Field>
                <Field>
                  <FieldLabel for="email">
                    Email
                  </FieldLabel>
                  <Input id="email" :model-value="authStore.user?.email" disabled />
                </Field>

                <FieldSeparator />
                <form @submit.prevent="handlePwdReset">
                  <Field>
                    <FieldLabel for="password">
                      Reset password
                    </FieldLabel>
                
                    <Input
                      id="password"
                      type="password"
                      placeholder="New password"
                      required
                      v-model="newpassword"/>
                  </Field>
                  <Field  orientation="horizontal">
                    <Button class="mt-6" type="submit" v-if="newpassword">Reset</Button>
                    <Button class="mt-6" disabled v-else>Reset</Button>
                  </Field>
                </form>
                
              </FieldGroup>
            </FieldSet>
          </div>
        </CardContent>
      </Card>
      
      <ReadListView></ReadListView>
    </div>

    
  </div>
  
  
</template>