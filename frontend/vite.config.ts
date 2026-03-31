import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig, loadEnv } from 'vite';

export default defineConfig(({ mode }) => {
	const env = loadEnv(mode, process.cwd(), '');

	const allowedHosts = (env.VITE_ALLOWED_HOSTS || '')
		.split(',')
		.map((host) => host.trim())
		.filter(Boolean);

	return {
		plugins: [sveltekit()],
		server: {
			host: '0.0.0.0',
			allowedHosts
		}
	};
});