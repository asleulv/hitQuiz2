<script>
	import { onMount, tick } from 'svelte';

	export let trigger;
	export let target;
	export let position = 'left';

	let timeout;
	let visible = false;
	let self;

	const show = async (e) => {
		visible = true;
		await tick();

		let x, y;
		switch(position) {
		case 'bottom': 
			x = e.target.offsetLeft + e.target.offsetWidth / 2;
			y = e.target.offsetTop + e.target.offsetHeight + 12;
			break;
		case 'left':
			x = e.target.offsetLeft - 12;
			y = e.target.offsetTop + e.target.offsetHeight / 2;
			break;
		case 'right':
			x = e.target.offsetLeft + e.target.offsetWidth + 12;
			y = e.target.offsetTop + e.target.offsetHeight / 2;
			break;
		case 'top':
			x = e.target.offsetLeft + e.target.offsetWidth / 2;
			y = e.target.offsetTop - 12;
			break;
		default:
			console.error('illegal position');
		}

		self.style.top = (y) + 'px';
		self.style.left = (x) + 'px';

		clearTimeout(timeout);
		setTimeout(hide, 1500);
	};

	const hide = () => {
		visible = false;
	};

	const registerListener = () => {
		const elem = document.querySelector(target);
		elem.addEventListener(trigger, show);

	};

	onMount(registerListener);
</script>

{#if visible}
	<div class="tooltip {position}" bind:this={self}>
		<slot />
	</div>
{/if}

<style>
	.tooltip {
		position: absolute;
		z-index: 1;
		background-color: #fff;
		border: 1px solid #fff;
		border-radius: 3px;
		color: #000;
		padding: 0.6rem .84rem;
	}

	.left {
		transform: translateX(-100%) translateY(-50%);
	}

	.right {
		transform: translateY(-50%);
	}

	.bottom {
		transform: translateX(-50%);
	}

	.top {
		transform: translateX(-50%) translateY(-100%);
	}

	.left:after {
		content: "";
		position:absolute;
		left: 100%;
		top: 50%;
		margin-top: 0px;
		transform:translateY(-50%);
		border:10px solid #fff;
		border-color: transparent transparent transparent white;
		display:block;
	}

	.right:after {
		content: "";
		position:absolute;
		left: -20px;
		top: 50%;
		transform:translateY(-50%);
		border:10px solid #fff;
		border-color: transparent white transparent transparent;
		display:block;
	}

	.bottom:after {
		content: "";
		position:absolute;
		left: 50%;
		top: -50%;
		margin-top: 10px;
		transform:translateY(-50%) translateX(-50%);
		border:10px solid #fff;
		border-color: transparent transparent white transparent;
		display:block;
	}

	.top:after {
		content: "";
		position:absolute;
		left: 50%;
		top: 100%;
		margin-top: 10px;
		transform:translateY(-50%) translateX(-50%);
		border:10px solid #fff;
		border-color: white transparent transparent transparent;
		display:block;
	}


</style>