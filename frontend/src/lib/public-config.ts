import {
  PUBLIC_AGENT_BACKEND_URL_HTTP,
  PUBLIC_AGENT_BACKEND_URL_HTTPS,
  PUBLIC_BACKEND_URL_HTTP,
  PUBLIC_BACKEND_URL_HTTPS
} from '$env/static/public';

function normalize(url: string): string {
  return url.replace(/\/+$/, '');
}

export function getBackendUrl(): string {
  const url = import.meta.env.DEV ? PUBLIC_BACKEND_URL_HTTP : PUBLIC_BACKEND_URL_HTTPS;

  if (!url) {
    throw new Error('Backend URL is not configured');
  }

  return normalize(url);
}

export function getAgentBackendUrl(): string {
  const primary = import.meta.env.DEV
    ? PUBLIC_AGENT_BACKEND_URL_HTTP || PUBLIC_BACKEND_URL_HTTP
    : PUBLIC_AGENT_BACKEND_URL_HTTPS || PUBLIC_BACKEND_URL_HTTPS;

  if (!primary) {
    throw new Error('Agent backend URL is not configured');
  }

  return normalize(primary);
}

export function getBrowserWsUrl(path: string): string {
  if (typeof window === 'undefined') {
    throw new Error('getBrowserWsUrl must be called in the browser');
  }

  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  return `${protocol}//${window.location.host}${path}`;
}