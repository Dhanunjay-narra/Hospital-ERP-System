const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000/api/v1";

export interface ApiResponse<T = any> {
  data?: T;
  items?: T[];
  total?: number;
  error?: string;
}

export class ApiClient {
  private static getAuthToken(): string | null {
    if (typeof window === "undefined") return null;
    return localStorage.getItem("access_token");
  }

  static async request<T = any>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const token = this.getAuthToken();
    const headers: Record<string, string> = {
      "Content-Type": "application/json",
      ...(options.headers as Record<string, string> || {}),
    };

    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }

    const url = endpoint.startsWith("http") ? endpoint : `${API_BASE_URL}${endpoint}`;
    
    try {
      const response = await fetch(url, {
        ...options,
        headers,
      });

      if (response.status === 401) {
        if (typeof window !== "undefined" && !window.location.pathname.includes("/login")) {
          localStorage.removeItem("access_token");
          localStorage.removeItem("user_info");
          window.location.href = "/login";
        }
      }

      if (!response.ok) {
        const errorBody = await response.json().catch(() => ({}));
        throw new Error(errorBody.detail || `Request failed with status ${response.status}`);
      }

      return await response.json();
    } catch (err: any) {
      console.error(`API Error on [${options.method || "GET"}] ${endpoint}:`, err.message);
      throw err;
    }
  }

  static get<T = any>(endpoint: string, params?: Record<string, any>): Promise<T> {
    let url = endpoint;
    if (params) {
      const query = new URLSearchParams();
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined && value !== null && value !== "") {
          query.append(key, String(value));
        }
      });
      const queryString = query.toString();
      if (queryString) url += `?${queryString}`;
    }
    return this.request<T>(url, { method: "GET" });
  }

  static post<T = any>(endpoint: string, body: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: "POST",
      body: JSON.stringify(body),
    });
  }

  static patch<T = any>(endpoint: string, body: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: "PATCH",
      body: JSON.stringify(body),
    });
  }

  static delete<T = any>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: "DELETE" });
  }
}
