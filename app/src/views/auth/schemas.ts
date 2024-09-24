import { NAME_REGEX, PASSWORD_REGEX } from '@/constants'
import { z } from 'zod'

export const loginSchema = z.object({
  email: z.string().email('Invalid email'),
  password: z
    .string()
    .regex(
      PASSWORD_REGEX,
      'Password must be 8-20 characters, include a number and a special character'
    )
})

export const registerSchema = loginSchema.extend({
  firstName: z
    .string()
    .min(1, 'First name is required')
    .max(20, 'Max 20 characters')
    .regex(NAME_REGEX, 'Only letters allowed'),
  lastName: z
    .string()
    .min(1, 'Last name is required')
    .max(20, 'Max 20 characters')
    .regex(NAME_REGEX, 'Only letters allowed')
})
