<script>
    import { Router, Route } from "svelte-routing";
    import RegPage from "./pages/reg/RegPage.svelte";
    import AuthPage from "./pages/auth/AuthPage.svelte";
    import StorePage from "./pages/store/StorePage.svelte";
    import UploadPage from "./pages/upload/UploadPage.svelte";
    import ProductPage from "./pages/product/ProductPage.svelte";
    import ProfilePage from "./pages/profile/ProfilePage.svelte";
    import Header from "./components/Header.svelte";
    import Footer from "./components/Footer.svelte";
</script>


<Router>
    <Header/>
    <main>
        <Route path="/" component={StorePage} />
        <Route path="/reg" component={RegPage} />
        <Route path="/auth" component={AuthPage} />
        <Route path="/upload" component={UploadPage} />
        <Route path="/profile" component={ProfilePage} />
        <Route path="/store/:id" component={ProductPage} />
    </main>
    <Footer/>
</Router>


<style>
    main {
        max-width: 1280px;
        margin: 0px auto;
    }
</style>