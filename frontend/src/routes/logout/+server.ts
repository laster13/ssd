import { redirect } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

const cookieOptions = {
	path: '/',
	httpOnly: true,
	sameSite: 'lax' as const,
	secure: false
};

export const GET: RequestHandler = async ({ cookies }) => {
	cookies.delete('token', cookieOptions);
	throw redirect(303, '/login');
};

export const POST: RequestHandler = async ({ cookies }) => {
	cookies.delete('token', cookieOptions);
	throw redirect(303, '/login');
};