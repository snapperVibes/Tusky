export interface IUserProfile {
    username: string
    number: bigint
    is_active: boolean
    is_superuser: boolean
    full_name: string
    id: number
}

export interface IUserProfileUpdate {
    username: string
    number: bigint
    password?: string
    is_active?: boolean
    is_superuser?: boolean
}

export interface IUserProfileCreate {
    username: string
    email: string
    password?: string
    is_active?: boolean
    is_superuser?: boolean
}
