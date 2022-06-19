<script>
    import { navigate } from "svelte-routing";
    import { productID } from "../../stores/stores.js";

    export let id = 0;
    export let productName = "productName";
    // export let productImage = "";
    export let authorName = "authorName";
    // export let authorImage = "";
    export let price = 999;

    let transition = () => {
        $productID = id;
        navigate(`/store/${id}`);
    };
</script>


<button on:click={transition}>
        <div class="img"></div>
        <!-- <img src={image_file} alt=""> -->
        <div class="info">
            <div class="names">
                <div class="product-name">{productName}</div>
                <div class="author-name">{authorName}</div>
            </div>
            <div class="price">{price}</div>
        </div>
</button>


<style>
    button {
        display: flex;
        flex-direction: column;
        padding: 14px 14px 16px 14px;
        border-radius: 20px;
        border: 2px solid var(--color-neutral-2);
        gap: 16px;
    }

    .img {
        background-color: aquamarine;
        width: 237px;
        height: 237px;
        border-radius: 10px;
    }

    .info {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: flex-start;
    }

    .names {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
    }

    .product-name {
        color: var(--color-neutral-6);
        font-size: 16px;
        font-weight: 700;
    }

    .author-name {
        font-size: 12px;
        font-weight: 500;
        color: var(--color-neutral-6);
    }

    .price {
        font-size: 12px;
        font-weight: 500;
        color: var(--color-success);
        border-radius: 4px; 
        padding: 4px 6px;
        border: 2px solid var(--color-success);
    }
</style>