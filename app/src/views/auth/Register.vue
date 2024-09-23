<script setup lang="ts">
import { FormField } from '@/components/ui/form'
import { useRegisterMutation } from '@/composables/mutations/use-register-mutation'
import { toTypedSchema } from '@vee-validate/zod'
import { LoaderCircle } from 'lucide-vue-next'
import { useForm } from 'vee-validate'
import { registerSchema } from './schemas'

const router = useRouter()
const { mutate: registerMutate, isPending } = useRegisterMutation()

const { isFieldDirty, handleSubmit } = useForm({
  validationSchema: toTypedSchema(registerSchema)
})

const onSubmit = handleSubmit((values) => {
  registerMutate(values, {
    onSuccess: () => {
      toast.success({ message: 'Register success' })
      router.push({
        path: '/register-success',
        query: { email: values.email }
      })
    },
    onError: (error) => {
      toast.error({ message: error.response?.data.message })
    }
  })
})
</script>

<template>
  <div class="flex justify-center w-full min-w-[600px] min-h-screen bg-gray-200">
    <div class="flex items-center justify-center">
      <Card class="max-w-sm md:min-w-[400px] md:min-h-[400px] mx-auto border-none">
        <CardHeader>
          <CardTitle class="text-2xl">
            Sign Up
          </CardTitle>
          <CardDescription> Enter your information to create an account </CardDescription>
        </CardHeader>
        <CardContent>
          <form autocomplete="off" @submit.prevent="onSubmit">
            <div class="grid gap-4">
              <div class="grid grid-cols-2 gap-4">
                <FormField v-slot="{ componentField }" name="firstName" :validate-on-blur="!isFieldDirty">
                  <FormItem>
                    <FormLabel>First name</FormLabel>
                    <FormControl>
                      <Input type="text" placeholder="Max" v-bind="componentField" autocomplete="off" />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                </FormField>
                <FormField v-slot="{ componentField }" name="lastName" :validate-on-blur="!isFieldDirty">
                  <FormItem>
                    <FormLabel>Last name</FormLabel>
                    <FormControl>
                      <Input type="text" placeholder="Mustermann" v-bind="componentField" autocomplete="off" />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                </FormField>
              </div>
              <FormField v-slot="{ componentField }" name="email" :validate-on-blur="!isFieldDirty">
                <FormItem>
                  <FormLabel>Email</FormLabel>
                  <FormControl>
                    <Input type="text" placeholder="max@mustermann.com" v-bind="componentField" autocomplete="off" />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              </FormField>
              <FormField v-slot="{ componentField }" name="password" :validate-on-blur="!isFieldDirty">
                <FormItem>
                  <FormLabel>Password</FormLabel>
                  <FormControl>
                    <Input type="password" placeholder="********" v-bind="componentField" autocomplete="new-password" />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              </FormField>
              <Button class="w-full" type="submit" :disabled="isPending">
                <LoaderCircle v-if="isPending" class="w-4 h-4 mr-2 animate-spin" />
                Sign up
              </Button>
              <div class="mt-4 text-sm text-center">
                Already have an account?
                <RouterLink to="/login" class="underline">
                  Login
                </RouterLink>
              </div>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  </div>
</template>
