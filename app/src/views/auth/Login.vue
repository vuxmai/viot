<script setup lang="ts">
import LoginBackground from '@/assets/images/login-background.png'
import { FormField } from '@/components/ui/form'
import { useLoginMutation } from '@/composables/mutations/use-login-mutation'
import { PASSWORD_REGEX } from '@/constants'
import { toTypedSchema } from '@vee-validate/zod'
import { LoaderCircle } from 'lucide-vue-next'
import { useForm } from 'vee-validate'
import { useI18n } from 'vue-i18n'
import { z } from 'zod'

const { t } = useI18n()

const formSchema = toTypedSchema(
  z.object({
    email: z.string().email('Invalid email'),
    password: z
      .string()
      .regex(
        PASSWORD_REGEX,
        'Password must be 8-20 characters, include a number and a special character'
      )
  })
)
const router = useRouter()
const { mutate: loginMutate, isPending } = useLoginMutation()

const { isFieldDirty, handleSubmit } = useForm({
  validationSchema: formSchema
})

const onSubmit = handleSubmit((values) => {
  loginMutate(values, {
    onSuccess: () => {
      setTimeout(() => {
        router.push('/')
      }, 300)
      toast.success({ message: t('login.success') })
    },
    onError: (error) => {
      toast.error({ message: error.response?.data.message })
    }
  })
})
</script>

<template>
  <div class="flex justify-center w-full min-w-[600px] min-h-screen">
    <img
      :src="LoginBackground"
      alt="login image"
      class="absolute inset-0 object-cover w-full h-full -z-10"
    >
    <div class="flex items-center justify-center">
      <Card class="max-w-sm md:min-w-[400px] md:min-h-[400px] mx-auto border-none">
        <CardHeader>
          <CardTitle class="text-2xl">
            Login
          </CardTitle>
          <CardDescription> Enter your email below to login to your account </CardDescription>
        </CardHeader>
        <CardContent>
          <form @submit.prevent="onSubmit">
            <div class="space-y-4">
              <FormField v-slot="{ componentField }" name="email" :validate-on-blur="!isFieldDirty">
                <FormItem>
                  <FormLabel>Username</FormLabel>
                  <FormControl>
                    <Input type="text" placeholder="acount@gmail.com" v-bind="componentField" />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              </FormField>
              <FormField v-slot="{ componentField }" name="password" :validate-on-blur="!isFieldDirty">
                <FormItem>
                  <FormLabel>Password</FormLabel>
                  <FormControl>
                    <Input type="password" placeholder="********" v-bind="componentField" />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              </FormField>
              <Button class="w-full" type="submit" :disabled="isPending">
                <LoaderCircle v-if="isPending" class="w-4 h-4 mr-2 animate-spin" />
                Sign in
              </Button>
              <Button variant="outline" class="w-full">
                Login with Google
              </Button>
            </div>
            <div class="mt-4 text-sm text-center">
              Don't have an account?
              <RouterLink to="/register" class="underline">
                Sign up
              </RouterLink>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  </div>
</template>
