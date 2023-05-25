<script>
	import { writable } from 'svelte/store';
	import { background } from '$lib/stores.js';
	import { fade, fly } from 'svelte/transition';

	const modalOpen = writable(false);

	export const toggle = () => {
		modalOpen.update(value => !value);
	};

	export const show = () => {
		modalOpen.update(value => true);
	};

	export const hide = () => {
		modalOpen.update(value => false);
	};

	const clickOutside = (node) => {
		const handleClick = (event) => {
			if (!node.contains(event.target)) {
				node.dispatchEvent(new CustomEvent('outclick'));
			}
		};

		document.addEventListener('click', handleClick, true);

		return {
			destroy() {
				document.removeEventListener('click', handleClick, true);
			},
		};
	}

	const onKeyDown = (e) => {
		e.stopPropagation();
		if (e.key === 'Escape') { 
			hide();
		}
	}
</script>

<svelte:window on:keydown={onKeyDown} />

{#key $modalOpen}
	<div 
		class="overlay" 
		class:open={$modalOpen}
		in:fade={{ duration: 400 }}
		out:fade={{ duration: 400, delay: 500 }}
	>
		<div 
			class="modal" 
			style:background-color={$background} 
			use:clickOutside 
			on:outclick={hide} 
			in:fly={{ y: -200, duration: 1000, delay: 400 }}
			out:fly={{ y: -200, duration: 1000, delay: 0 }}
		>
			<span class="close" on:click={toggle}>&times;</span>
			<slot name="title" />
			<div class="wrapper">
				<slot />
			</div>
		</div>
	</div>
{/key}

<style>
	.overlay {
		display: none;
		position: fixed;
		z-index: 1;
		left: 0;
		top: 0;
		width: 100vw;
		height: 100vh;
		background-color: rgba(0,0,0,0.4);

		-webkit-backdrop-filter: blur(3px);
		backdrop-filter: blur(3px);
	}

	.modal {
		display: flex;
		flex-direction: column;

		position: fixed;
		top: 50%;
		left: 50%;
		transform: translate(-50%, -50%);

		border: 1px solid #fff;
		border-radius: 11px;
		max-height: 70%;
		max-width: 720px;
		height: 70%;
		width: calc(100vw - 4.8rem);

		padding: 0.6rem 1.2rem;

		background-color: #fefefe;
		background: linear-gradient(180deg, rgba(40,44,52,0.8) 0%, rgba(0,0,0,0.284) 25%, rgba(0,0,0,0) 55%);

		box-shadow: 0px 12px 12px 1px rgba(0, 0, 0, .2);
	}

	.wrapper {
		display: flex;
		flex-direction: column;
		overflow: hidden;
	}

	.open {
		display: block;
	}

	.close {
		position: absolute;
		right: 1.2rem;
		top: .4rem;
		font-size: 1.6em;
		cursor: pointer;
		z-index: 1;
	}

	.close:hover {
		font-weight: 600;
	}
</style>