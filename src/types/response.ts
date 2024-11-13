import { ApiError } from "./error";

export interface ApiResponse<T = unknown> {
    success: boolean; 
    data?: T; 
    error?: ApiError; 
    message?: string; 
    timestamp: string; 
}

