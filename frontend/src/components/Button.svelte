<script>
    export let type = "light";
    export let size = "medium";
    export let text = "button";
    export let action;
</script>


<button class={type + " " + size} on:click|preventDefault={action}>{text}</button>


<style>
    button {
        border-radius: 100px;
        font-weight: 700;
        text-align: center;
    }

    .big {
        font-size: 16px;
        padding: 12px 30px;
    }

    .medium {
        font-size: 14px;
        padding: 10px 18px;
    }

    .small {
        font-size: 12px;
        padding: 8px 12px;
    }
    
    .light {
        border: 2px solid var(--color-neutral-2);
        background-color: var(--color-neutral-1);
        color: var(--color-neutral-6);
    }
    
    .light:hover {
        border: 2px solid var(--color-primary);
        background-color: var(--color-primary);
        color: var(--color-neutral-1);
    }
    
    .accent {
        border: 2px solid var(--color-primary);
        background-color: var(--color-primary);
        color: var(--color-neutral-1);
    }
</style>