<script>
    import { navigate } from "svelte-routing";

    let product = {};
</script>


<button on:click={() => navigate(`/store/${product.id}`)}>
        <img src={product.productImage} alt="" />
        <div class="info">
            <div class="name">Значения из числовых input элементов автоматически приводятся к нужному типу</div>
            <!-- <div class="name">{product.productName}</div> -->
            <div class="price">{product.price}</div>
        </div>
</button>


<style>
    button {
        display: flex;
        flex-direction: column;
        padding: 16px;
        border-radius: 20px;
        border: 2px solid var(--color-neutral-2);
    }

    img {
        background-color: aquamarine;
        width: 237px;
        height: 237px;
        border-radius: 10px;
    }

    .info {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: center;
        padding-top: 16px;
    }

    .name {
        color: var(--color-neutral-6);
        font-size: 16px;
        font-weight: 700;
    }

    .price {
        color: var(--color-success);
        font-size: 12px;
        font-weight: 500;
        border-radius: 4px; 
        padding: 4px 6px;
        border: 2px solid var(--color-success);
    }
</style>