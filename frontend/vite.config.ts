import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig, loadEnv } from 'vite';
import tailwindcss from '@tailwindcss/vite';

function parseCsv(value: string): string[] {
	return value
		.split(',')
		.map((entry) => entry.trim())
		.filter(Boolean);
}

export default defineConfig(({ mode }) => {
	const env = loadEnv(mode, process.cwd(), '');
	const allowedHosts = parseCsv(env.VITE_ALLOWED_HOSTS || '');
	const bindAll = env.VITE_DEV_BIND_ALL === 'true';

	return {
		plugins: [tailwindcss(), sveltekit()],
		server: {
			host: bindAll ? '0.0.0.0' : '127.0.0.1',
			port: Number(env.VITE_PORT || 5173),
			strictPort: true,
			allowedHosts
		},
		preview: {
			host: '127.0.0.1',
			port: Number(env.VITE_PREVIEW_PORT || 4173),
			strictPort: true,
			allowedHosts
		}
	};
});