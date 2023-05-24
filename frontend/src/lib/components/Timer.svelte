<script>
	import { createEventDispatcher, onDestroy } from 'svelte';
	import { tweened } from 'svelte/motion';
	import { linear as easing } from 'svelte/easing';

	const dispatch = createEventDispatcher();

	const duration = 10;

	let interval = null; 
	let ticks = 0;

	const updateTimer = () => {
		ticks += 1;
	};
	
	export const start = () => {
		clearInterval(interval);
		interval = setInterval(updateTimer, 1000);
	};

	export const stop = () => {
		clearInterval(interval);
	};

	export const reset = () => {
		ticks = 0;
	};

	onDestroy(() => {
		clearInterval(interval);
	});

	$: seconds = Math.max(0, duration - ticks);
	$: if (seconds === 0) {
		stop();
		dispatch('stop');
	};

	let offset = tweened(1, { duration, easing });

	$: offset.set(Math.max(seconds , 0) / duration);
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
		<text x="0" y="0.3em">
			<tspan font-weight="plain">{seconds}</tspan>
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