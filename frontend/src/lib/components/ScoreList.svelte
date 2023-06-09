<script>
	import { onMount } from 'svelte';
	import { writable, get } from 'svelte/store';
	import { getQueryString } from '$lib/utils.js';

	const LIMIT = 20; 
	const store = writable({}); 

	let checked = false;

	onMount(async () => {
		await load();
	});

	const load = async () => {
		const params = { per_page: LIMIT };
		if (!checked) {
			params['d'] = new Date().toISOString().slice(0, 10);
		}
		let url = `/scores/?` + getQueryString(params);
		const response = await fetch(url); 
		const data = await response.json();
		store.set(data);
	};

	const loadMore = () => {
		const currentData = get(store); 
		const nextPage = getNextPage(currentData); 
		if (nextPage) {
			fetch(nextPage)
				.then(response => response.json())
				.then(data => {
					store.update(d => {
						d.data = [...d.data, ...data.data]
						d.meta.next = data.meta.next || null;
						return d;
					});
				});
		}
	}

	const getNextPage = (data) => {
		const meta = data.meta;
		return meta && meta.next;
	}

	const hasNextPage = () => {
		return $store.meta && $store.meta.next;
	}

	const createObserver = () => {
		return new IntersectionObserver(entries => {
			entries.forEach(entry => {
				if (entry.isIntersecting) {
					loadMore();
				}
			});
		});
	}

	let observer;
	const observeFooter = (node) => {
		if (node) {
			observer = observer || createObserver();
			observer.observe(node);
		}
	}
</script>

<div style="margin: 1.5rem;">
	<span style="vertical-align: super; padding: .3rem">Today</span>
	<label class="switch">
		<input type="checkbox" bind:checked={checked} on:change={load}>
		<span class="slider round"></span>
	</label>
	<span style="vertical-align: super; padding: .3rem">All</span>
</div>

<div class="scroller">
	<table>
		<tr>
		  <th>#</th>
		  <th class="namefield">Name</th>
		  <th>Score</th>
		</tr>
		{#each $store.data || [] as item, index}
		<tr style="border: {item.points > 1500 || item.points > 1000 ? '1px solid rgba(255, 215, 0, 0.6)' : '1px solid rgba(255, 255, 255, 0.34)'};">
		  <td>{item.rank}</td>
		  <td style="color: {item.points > 1500 ? 'gold' : (item.points > 1000 ? 'white' : 'lightgrey')}; text-align: left;">
			{#if item.points > 3000}
				<span style="margin-right: 0.25rem;">🎯</span>
			{:else if item.points > 1500}
				<span style="margin-right: 0.25rem;">🔥</span>
			{:else if item.points > 1000}
				<span style="margin-right: 0.25rem;">⭐️</span>
			{:else}
				<span style="margin-right: 0.25rem;">👶🏽</span>
			{/if}
			{item.name}
		  </td>
		  <td>{item.points}</td>
		</tr>
		{/each}
	  </table>
	{#if ($store.data || []).length >= LIMIT && hasNextPage()}
		<div use:observeFooter>Loading more...</div>
	{/if}
</div>

<style>
	.scroller {
		box-sizing: border-box;
		position: relative;
		height: auto;
		display: block;
		overflow: auto;
/*		margin: 1.5rem 0;*/
		margin: 1rem 0 1.5rem;
	}
	table {
		width: 100%;
		border-collapse: collapse;
	}

	.namefield {
		text-align: left;
		padding-left: 0.5rem;
	}


	/* --- */

	.switch {
		position: relative;
		display: inline-block;
		width: 48px;
		height: 24px;
	}

	.switch input {
		display:none;
	}

	.slider {
		position: absolute;
		cursor: pointer;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		border: 2px solid #fff;
		-webkit-transition: .4s;
		transition: .4s;
	}

	.slider:before {
		position: absolute;
		content: '';
		height: 16px;
		width: 16px;
		left: 2px;
		bottom: 2px;
		background-color: white;
		-webkit-transition: .4s;
		transition: .4s;
	}

	input:checked + .slider {
	}

	input:focus + .slider {
		box-shadow: 0 0 1px #2196F3;
	}

	input:checked + .slider:before {
		-webkit-transform: translateX(24px);
		-ms-transform: translateX(24px);
		transform: translateX(24px);
	}

	.slider.round {
		border-radius: 24px;
	}

	.slider.round:before {
		border: 0px;
		border-radius: 50%;
	}

</style>