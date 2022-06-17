<script>
    import { API_HOST } from "../../api.js";
    import { onMount } from "svelte/internal";
    import ProductCard from "./ProductCard.svelte";

    export let pageNumber = 1;

    let products = [];

    onMount(async () => {
        const res = await fetch(`${API_HOST}/store?page=${pageNumber}`);
        products = await res.json();
    });
</script>


<div class="product-list">
    {#each products as { id, productName, productImage, authorName, price }}
        <ProductCard {id} {productName} {productImage} {authorName} {price}/>
    {/each}
</div>


<style>
    .product-list {
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
        justify-content: center;
        gap: 30px;
    }
</style>