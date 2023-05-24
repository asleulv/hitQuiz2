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
	 	{#each $store.data || [] as item}
		<tr>
			<td>{item.rank}</td>
			<td>{item.name}</td>
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
	table, th, td {
		border: 1px solid white;
	}
</style>