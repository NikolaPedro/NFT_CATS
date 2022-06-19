<script>
    import { API_HOST } from "../../utils/api.js"
    import { onMount } from "svelte/internal";
    import ProductCard from "./ProductCard.svelte";

    export let pageNumber = 1;

    let products = [];

    onMount(async () => {
        try {
            const res = await fetch(`${API_HOST}/store?page=${pageNumber}`);
            products = await res.json();
        } catch (error) {
            products = [
                { id: 1, productName: "BEER", productImage: "", authorName: "Pedro", price: 75.7},
                { id: 2, productName: "VODKA", productImage: "", authorName: "Pedro", price: 34.2},
                { id: 3, productName: "GAMEBOY", productImage: "", authorName: "Roma", price: 332.99}
            ];
        }
        
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