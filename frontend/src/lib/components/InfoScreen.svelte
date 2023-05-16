<script>
	import { fade } from 'svelte/transition';
	import { Confetti } from 'svelte-confetti';

	export let success = false;
</script>

<div in:fade={{ duration: 800 }}>
	{#if success}
		<div class="confetti-overlay">
			<Confetti 
				x={[-5, 5]} 
				y={[0, 0.1]} 
				delay={[500, 2000]}  
				infinite 
				duration=5000 
				amount=200 
				fallDistance="16rem" 
			/>
		</div>
	{/if}
	<slot />
</div>

<style>
	.confetti-overlay {
		position: fixed; 
		top: -100px; 
		left: 0; 
		height: 16rem; 
		width: 100vw; 
		display: flex; 
		justify-content: center; 
		overflow: hidden;
	}

	div {
		margin: 5.6rem 0;
	}

	div :global(p) {
		margin: 1.2rem 0 2.4rem ;
	}

	div :global(button) {
		padding: 0.5rem 1.5rem;
		border: 1px solid #ddd;
		border-radius: 3px;
		background-color: #eee;
		font-size: 0.85em;
		transition-property: color, background-color;
		transition-duration: 200ms;
		transition-timing-function: ease-out;
	}

	div :global(button:hover) {
		background-color: #dedede;
	}

	div :global(button:active) {
		background: linear-gradient(-45deg, #aaa, #ccc, #aaa, #fff);
		background-size: 400% 400%; 
		animation: gradient 15s ease infinite;
	}
/*
	div :global(button[disabled]) {
		color: #dedede;
	}
*/
</style>