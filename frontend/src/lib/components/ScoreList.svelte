<script>
	import { onMount } from 'svelte';
	import { writable, get } from 'svelte/store';
	
	const LIMIT = 10; 
	const store = writable({}); 

	onMount(async () => {
		const response = await fetch('/scores/');
		const data = await response.json();
		store.set(data);
	});

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
			{#if item.points > 1500}
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
		margin: 1.5rem 0;
	}
	table {
		width: 100%;
		border-collapse: collapse;
	}

	.namefield {
		text-align: left;
		padding-left: 0.5rem;
	}



</style>