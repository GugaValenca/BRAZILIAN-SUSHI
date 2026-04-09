const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "/api";

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

type RequestOptions = RequestInit & {
  token?: string;
};

function formatFieldLabel(field: string) {
  return field
    .replace(/_/g, " ")
    .replace(/\b\w/g, (match) => match.toUpperCase());
}

function flattenErrorMessage(value: unknown): string {
  if (typeof value === "string") {
    return value;
  }

  if (Array.isArray(value)) {
    return value.map(flattenErrorMessage).filter(Boolean).join(" ");
  }

  if (value && typeof value === "object") {
    const entries = Object.entries(value as Record<string, unknown>);
    return entries
      .map(([field, fieldValue]) => {
        if (field === "detail") {
          return flattenErrorMessage(fieldValue);
        }
        return `${formatFieldLabel(field)}: ${flattenErrorMessage(fieldValue)}`;
      })
      .filter(Boolean)
      .join(" ");
  }

  return "";
}

async function parseResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const errorBody = await response.text();
    if (!errorBody.trim()) {
      throw new Error(`Request failed with status ${response.status}`);
    }

    try {
      const parsedError = JSON.parse(errorBody) as unknown;
      const message = flattenErrorMessage(parsedError);
      throw new Error(message || `Request failed with status ${response.status}`);
    } catch {
      throw new Error(errorBody || `Request failed with status ${response.status}`);
    }
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return response.json() as Promise<T>;
}

export async function apiRequest<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const { token, headers, ...rest } = options;
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...rest,
    headers: {
      ...(rest.body ? { "Content-Type": "application/json" } : {}),
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...headers,
    },
  });

  return parseResponse<T>(response);
}

export async function apiFormRequest<T>(path: string, body: Record<string, string>): Promise<T> {
  return apiRequest<T>(path, {
    method: "POST",
    body: JSON.stringify(body),
  });
}

export { API_BASE_URL };
