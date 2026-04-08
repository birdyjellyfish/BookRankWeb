<script setup lang="ts">
import router from '@/router';
import { getCSRFToken } from '@/stores/auth';
import { ref } from 'vue';

import {
  Field,
  FieldDescription,
  FieldGroup,
  FieldLabel,
  FieldSet,
} from '@/components/ui/field'
import { Input } from '@/components/ui/input'

import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog'
import Button from '@/components/ui/button/Button.vue';
import FieldError from '@/components/ui/field/FieldError.vue';
import { Check } from 'lucide-vue-next';
import Spinner from './ui/spinner/Spinner.vue';

const url = import.meta.env.VITE_API_URL;

const error = ref<string>("");
const success = ref<string>("");
const username = ref<string>("");
const password = ref<string>("")
const email = ref<string>("");
const loading = ref(false);

async function useRegister(): Promise<void> {
  loading.value = true;
  error.value = "";
  success.value = "";

  try {
    const response = await fetch(`${url}/users/register/`, {
      method: "POST",
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCSRFToken()
      },
      credentials: 'include',
      body: JSON.stringify({
        "username": username.value,
        "password": password.value,
        "email": email.value
      })
    })

    const data = await response.json();

    if (response.ok) {
      success.value = "Successfully registered account. Redirecting you to sign in page..."
      // redirect to register page
      setTimeout(() => {
        openSignup.value = true;
        openSignin.value = true;
      }, 3000)
    } else {
      error.value = data.username[0] || "Registration failed." // api will say if username already appears in db
    }
  } catch (err) {
    error.value = `An error occured during registration: ${err}`
  }

  loading.value = false;
}

function resetError() {
  error.value = "";
}

const openDialog = defineModel<boolean>("dialog");
const openSignup = defineModel<boolean>("signup");
const openSignin = defineModel<boolean>("signin")
</script>

<template>
  <DialogContent class="sm:max-w-[425px]">
    <DialogHeader>
      <DialogTitle>
        Sign Up
      </DialogTitle>
      <DialogDescription class="min-h-10">
        <FieldError>
          {{ error }}
        </FieldError>
        <div>
          {{ success }}
        </div>
      </DialogDescription>
    </DialogHeader>

    <div class="flex items-center justify-center">
      <form class="w-full max-w-md" @submit.prevent="useRegister">
        <FieldSet>
          <FieldGroup>
            <Field>
              <FieldLabel for="email">
                Email
              </FieldLabel>
              <Input
                v-model="email"
                id="email"  
                type="text"
                placeholder="Email" 
                required
                @input="resetError"/>
            </Field>

            <Field>
              <FieldLabel for="username">
                Username
              </FieldLabel>
              <FieldDescription>
                Choose a unique username for your account.
              </FieldDescription>
              <Input 
                v-model="username"
                id="username"
                type="text"
                placeholder="Username"
                required
                @input="resetError"/>
            </Field>

            <Field>
              <FieldLabel for="password">
                Password
              </FieldLabel>
              <FieldDescription>
                Must be at least 8 characters long and contain at least 1 special character.
              </FieldDescription>
              <Input
                v-model="password"
                id="password"
                type="password"
                required
                @input="resetError"/>
            </Field>

            <Field>
              <Button disabled v-if="success"><Check /></Button>
              <Button type="submit" v-else-if="!loading">Sign Up</Button>
              <Button disabled v-else-if="loading"><Spinner /></Button>
            </Field>
          </FieldGroup>
        </FieldSet>

        
      </form>
    </div>
  </DialogContent>
</template>