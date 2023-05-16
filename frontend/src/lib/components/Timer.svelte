<script>
	import { createEventDispatcher, onDestroy } from 'svelte';

	const dispatch = createEventDispatcher();

	const duration = 10;

	let interval = null; 
	let now = new Date().getTime();
	let end = now + duration * 1000;

	const updateTimer = () => {
		now = new Date().getTime();
	};
	
	export const start = () => {
		clearInterval(interval);
		interval = setInterval(updateTimer, 1000);
	};

	export const stop = () => {
		clearInterval(interval);
	};

	export const reset = () => {
		now = new Date().getTime();
		end = now + duration * 1000;
	};

	onDestroy(() => {
		clearInterval(interval);
	});

	$: ticks = Math.max(0, Math.round((end - now) / 1000));
	$: seconds = Math.floor((ticks % (1000 * 60)));
	$: if (ticks === 0) {
		stop();
		dispatch('stop');
	};
</script>

<span>{seconds}</span>

<style>
	span {
		display: inline-block;
		min-width: 1.2rem;
	}
</style>