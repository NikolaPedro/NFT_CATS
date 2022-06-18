<script>
    import { navigate } from "svelte-routing";
    import Button from "../../components/Button.svelte";
    import validate from "../../utils/validation.js";

    const maxlength = 30;

    let error = "";
    let form = {
        login: "",
        email: "",
        password: "",
        repeatPassword: ""
    };
    let answer = []

    let login = async () => {
        error = validate(form);
        if (error == "") {
            const responce = fetch(`${API_HOST}/registration`, {
                method: 'POST',
                body: JSON.stringify(form)
            });
            const answer = await responce.json();
            alert(JSON.stringify(answer));
            navigate("/");
        }
    }
</script>


<div class="container">
    <form>
        <div class="error">{error}</div>
        <input type="text" placeholder="Login" {maxlength} bind:value={form.login}>
        <input type="email" placeholder="Email" {maxlength} bind:value={form.email}>
        <input type="password" placeholder="Password" {maxlength} bind:value={form.password}>
        <input type="password" placeholder="Repeat password" {maxlength} bind:value={form.repeatPassword}>
        <button class="auth-button" on:click={() => navigate("/auth")}>Already have an account?</button>
        <Button type="accent" size="big" text="Sing up" action={login}/>
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

    .error {
        margin: 10px;
        color: var(--color-error);
        font-size: 16px;
        font-weight: 500;
    }
</style>