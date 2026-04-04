import { dev } from '$app/environment';
import { env } from '$env/dynamic/private';
import { error, type Cookies } from '@sveltejs/kit';
import { createHmac, randomBytes, timingSafeEqual } from 'node:crypto';

const TOKEN_COOKIE = 'token';
const CSRF_COOKIE = 'csrf_token';

const CSRF_SECRET =
	env.CSRF_SECRET ??
	env.JWT_SECRET_KEY ??
	(dev ? 'dev-only-csrf-secret-change-me' : '');

if (!CSRF_SECRET) {
	throw new Error('Missing CSRF_SECRET or JWT_SECRET_KEY for frontend security helpers');
}

const COOKIE_SECURE = !dev;

export const authCookieOptions = {
	path: '/',
	httpOnly: true,
	sameSite: 'lax' as const,
	secure: COOKIE_SECURE
};

export const csrfCookieOptions = {
	path: '/',
	httpOnly: true,
	sameSite: 'strict' as const,
	secure: COOKIE_SECURE
};

function safeEqual(a: string, b: string): boolean {
	const aBuf = Buffer.from(a);
	const bBuf = Buffer.from(b);

	if (aBuf.length !== bBuf.length) {
		return false;
	}

	return timingSafeEqual(aBuf, bBuf);
}

function signRawToken(raw: string, sessionBinding: string): string {
	return createHmac('sha256', CSRF_SECRET)
		.update(`${raw}.${sessionBinding}`)
		.digest('base64url');
}

function buildToken(sessionBinding: string): string {
	const raw = randomBytes(32).toString('base64url');
	const sig = signRawToken(raw, sessionBinding);
	return `${raw}.${sig}`;
}

function isValidToken(token: string, sessionBinding: string): boolean {
	const parts = token.split('.');

	if (parts.length !== 2) {
		return false;
	}

	const [raw, providedSig] = parts;
	const expectedSig = signRawToken(raw, sessionBinding);

	return safeEqual(providedSig, expectedSig);
}

function firstForwardedValue(value: string | null): string | null {
	if (!value) return null;
	return value.split(',')[0]?.trim() || null;
}

function getExpectedOrigin(url: URL, headers: Headers): string {
	const forwardedProto = firstForwardedValue(headers.get('x-forwarded-proto'));
	const forwardedHost = firstForwardedValue(headers.get('x-forwarded-host'));
	const forwardedPort = firstForwardedValue(headers.get('x-forwarded-port'));

	const proto = forwardedProto || url.protocol.replace(':', '');
	let host = forwardedHost || headers.get('host') || url.host;

	if (forwardedPort && forwardedHost && !forwardedHost.includes(':')) {
		const defaultPort =
			(proto === 'https' && forwardedPort === '443') ||
			(proto === 'http' && forwardedPort === '80');

		if (!defaultPort) {
			host = `${forwardedHost}:${forwardedPort}`;
		}
	}

	return `${proto}://${host}`;
}

export function ensureCsrfCookie(
	cookies: Cookies,
	sessionToken: string | null | undefined
): string {
	const binding = sessionToken ?? '';
	const existing = cookies.get(CSRF_COOKIE);

	if (existing && isValidToken(existing, binding)) {
		return existing;
	}

	const fresh = buildToken(binding);

	cookies.set(CSRF_COOKIE, fresh, {
		...csrfCookieOptions,
		maxAge: 60 * 60 * 8
	});

	return fresh;
}

export async function validateCsrf(opts: {
	request: Request;
	cookies: Cookies;
	url: URL;
	sessionToken: string | null | undefined;
}) {
	const { request, cookies, url, sessionToken } = opts;

	const origin = request.headers.get('origin');
	const expectedOrigin = getExpectedOrigin(url, request.headers);

	if (origin && origin !== expectedOrigin) {
		throw error(403, 'Invalid request origin');
	}

	const cookieToken = cookies.get(CSRF_COOKIE);

	if (!cookieToken) {
		throw error(403, 'Missing CSRF cookie');
	}

	const formData = await request.formData();
	const submittedToken = String(formData.get('_csrf') ?? '').trim();

	if (!submittedToken) {
		throw error(403, 'Missing CSRF token');
	}

	if (!safeEqual(submittedToken, cookieToken)) {
		throw error(403, 'Invalid CSRF token');
	}

	const binding = sessionToken ?? '';

	if (!isValidToken(submittedToken, binding)) {
		throw error(403, 'Invalid CSRF token');
	}

	return formData;
}

export function setSessionCookie(cookies: Cookies, accessToken: string) {
	cookies.set(TOKEN_COOKIE, accessToken, {
		...authCookieOptions,
		maxAge: 60 * 60
	});

	ensureCsrfCookie(cookies, accessToken);
}

export function clearSessionCookies(cookies: Cookies) {
	cookies.delete(TOKEN_COOKIE, authCookieOptions);
	cookies.delete(CSRF_COOKIE, csrfCookieOptions);
}