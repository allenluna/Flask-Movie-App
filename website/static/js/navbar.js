// nav sticky
document.addEventListener("scroll", () => {
    const nav = document.querySelector(".nav-fixed");
    const navBody = document.querySelector(".offcanvas");

    if(window.scrollY > 50){
        nav.classList.add("scrolled");
        navBody.style.height = "100vh"
    }else{
        nav.classList.remove("scrolled");
    }
})


var date = new Date();
document.querySelector("#footer-date").innerHTML = `
© ${date.toLocaleString('en-US', {year: 'numeric'})} MOVIES
`