import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
    server: {
        proxy: {
            '/quiz': 'http://127.0.0.1:5000',
        }
    },
    plugins: [sveltekit()]
});