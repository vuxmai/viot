<script setup lang="ts">
import { MailCheck } from 'lucide-vue-next'

const route = useRoute()
const router = useRouter()
const email = route.query.email as string

onMounted(() => {
  if (!email) {
    router.push('/login')
  }
})
</script>

<template>
  <div class="flex justify-center w-full min-w-[600px] min-h-screen bg-gray-200">
    <div class="flex items-center justify-center">
      <Card class="max-w-sm md:min-w-[500px] mx-auto border-none items-center justify-center">
        <CardHeader class="items-center text-center">
          <MailCheck class="w-8 h-8 text-green-600" />
          <CardTitle class="text-2xl text-center">
            Email Confirmation
          </CardTitle>
          <CardDescription>
            We have sent email to <code class="font-mono text-blue-600">{{ email }}</code> to
            confirm the validity of the email address. After receiving the email, follow the link
            provided to complete your registration.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div class="grid items-center justify-center gap-4">
            <p class="mt-4 text-sm text-center text-gray-600">
              Already confirmed your email?
              <RouterLink to="/login" class="text-blue-600 hover:underline">
                Go to login page
              </RouterLink>
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  </div>
</template>
