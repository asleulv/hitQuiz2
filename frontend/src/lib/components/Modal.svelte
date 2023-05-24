<script>
	import { writable } from 'svelte/store';
	import { background } from '$lib/stores.js';
	import { fade, fly } from 'svelte/transition';

	const modalOpen = writable(false);

	export const toggleModal = () => {
		modalOpen.update(value => !value);
	};

	export const showModal = () => {
		modalOpen.update(value => true);
	};

	export const hideModal = () => {
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
			hideModal();
		}
	}
</script>

<svelte:window on:keydown={onKeyDown} />

{#key $modalOpen}
	<div 
		class="modal" 
		class:open={$modalOpen}
		in:fade={{ duration: 400 }}
		out:fade={{ duration: 400, delay: 500 }}
	>
		<div 
			class="modal-content" 
			style:background-color={$background} 
			use:clickOutside 
			on:outclick={hideModal} 
			in:fly={{ y: -200, duration: 1000, delay: 400 }}
			out:fly={{ y: -200, duration: 1000, delay: 0 }}
		>
			<span class="close" on:click={toggleModal}>&times;</span>
			<slot name="title" />
			<div class="wrapper">
				<slot />
			</div>
		</div>
	</div>
{/key}

<style>
	/* rename overlay */
	.modal {
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

	.modal-content {
/*		position: relative;*/
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
		padding-bottom: 2.4rem;

		background-color: #fefefe;
		background: linear-gradient(180deg, rgba(40,44,52,0.8) 0%, rgba(0,0,0,0.284) 25%, rgba(0,0,0,0) 55%);
/*		transition: background-color 0.5s ease;*/

		box-shadow: 0px 12px 12px 1px rgba(0, 0, 0, .2);
	}

	.wrapper {
		box-sizing: border-box;
		position: relative;
		height: auto;
		overflow: scroll;
		display: block;
		overflow: auto;
	}

	.open {
		display: block;
	}

	.close {
		position: absolute;
		right: 1.2rem;
		font-size: 1.6em;
		cursor: pointer;
	}

	.close:hover {
		font-weight: 600;
	}
</style>