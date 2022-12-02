declare global {
    type User = {
        _id: string,
        username: string,
        email: string,
        password: string,
        name: string,
        phoneNumber: string,
        tokens: string[],
        confirmedRetas: string[],
        createdAt: string,
        updatedAt: string,
        __v: number
    }

    type LoginResponse = {
        success: boolean,
        message: string,
        user: User,
        token: string
    }

    type ErrorResponse = {
        code: number,
        msg: string
    }
}

export { }