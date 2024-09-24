export interface Page<T> {
  items: T[]
  totalItems: number
  page: number
  pageSize: number
  totalPages: number
  hasNextPage: boolean
  hasPreviousPage: boolean
}
