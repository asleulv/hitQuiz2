<script>
	import { createEventDispatcher, onDestroy } from 'svelte';
	import { tweened } from 'svelte/motion';
	import { linear as easing } from 'svelte/easing';

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

	let offset = tweened(1, { duration, easing });

	$: offset.set(Math.max(ticks , 0) / duration);
</script>

<svg viewBox="-16 -16 32 32" width="92" height="92">
	<title>Remaining seconds: {seconds}</title>
	<g fill="none" stroke="currentColor" stroke-width="1">
		<circle stroke="rgba(255,255,255,0.2)" r="11" />
		<path
			stroke="white"
			d="M 0 -11 a 11 11 0 0 0 0 22 11 11 0 0 0 0 -22"
			pathLength="1"
			stroke-dasharray="1"
			stroke-dashoffset={$offset}
		/>
	</g>

	<g
		fill="currentColor"
		text-anchor="middle"
		dominant-baseline="baseline"
		font-size="0.4em"
	>
		<text x="-3" y="2.25">
			<tspan dx="3" font-weight="plain">{seconds}</tspan>
		</text>
	</g>
</svg>

<style>
	svg {
		position: absolute;
		left: 50%;
		transform: translateX(-50%);
		z-index: 1;
	}
</style>