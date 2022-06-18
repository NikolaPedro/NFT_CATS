<script>
    import { Router, Route } from "svelte-routing";
    import StorePage from "./pages/store/StorePage.svelte";
    import RegPage from "./pages/reg/RegPage.svelte";
    import AuthPage from "./pages/auth/AuthPage.svelte";
    import Header from "./components/Header.svelte";
    import Footer from "./components/Footer.svelte";
</script>


<Router>
    <Header/>
    <main>
        <Route path="reg" component={RegPage} />
        <Route path="auth" component={AuthPage} />
        <Route path="/" component={StorePage} />
    </main>
    <Footer/>
</Router>


<style>
    main {
        max-width: 1280px;
        margin: 0px auto;
    }
</style>