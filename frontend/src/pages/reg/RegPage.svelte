<script>
    import { Link } from "svelte-routing";
    import Button from "../../components/Button.svelte";
    
    let maxlength = 30;
</script>


<div class="container">
    <form>
        <input type="text" placeholder="Login" {maxlength}>
        <input type="email" placeholder="Email" {maxlength}>
        <input type="password" placeholder="Password" {maxlength}>
        <input type="password" placeholder="Repeat password" {maxlength}>
        <Link to="auth">
            <div class="auth-button">Already have an account?</div>
        </Link>
        <Link to="/">
            <Button type="accent" size="big" text="Sing up" />
        </Link>
    </form>
</div>


<style>
    .container {
        height: 90vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }

    form {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding-bottom: 100px;
    }

    input {
        width: 300px;
        font-size: 14px;
        padding: 12px 18px;
        border-radius: 8px;
        border: 2px solid var(--color-neutral-2);
        margin: 6px;
    }

    input:focus {
        border: 2px solid var(--color-primary);
    }

    .auth-button {
        font-size: 14px;
        margin: 14px;
        color: var(--color-neutral-3);
        text-decoration: underline;
    }
    
    .auth-button:hover {
        color: var(--color-primary);
    }
</style>