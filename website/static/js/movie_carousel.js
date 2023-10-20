const popCarousel = document.querySelector('#popCarousel');
const movCarousel = document.querySelector('#movCarousel');
const upcomCarousel = document.querySelector('#upcommingCarousel');

// popular
let popularInner = $(".popular-inner")[0].scrollWidth;
let popularItem = $(".popular-item").width()
// movies
let movieInner = $(".movie-inner")[0].scrollWidth;
let movieItem = $(".movie-item").width()
// upcomming 
let upcomInner = $(".upcomming-inner")[0].scrollWidth;
let upcomItem = $(".upcomming-item").width()
// positions
let popularScrollPos = 0
let movieScrollPos = 0
let upcommingScrollPos = 0
// carousel function
function carouselItems(nextBtn, prevBtn, scrollPosition, innerItem, itemData, animateItem, numOfItem){
    // for next button
    nextBtn.on("click", () => {
        if(scrollPosition < (innerItem - (itemData * numOfItem))){
            scrollPosition += itemData;
            animateItem.animate({scrollLeft : scrollPosition }, 600)
        }
    })
    prevBtn.on("click", () => {
        scrollPosition -= itemData;
        animateItem.animate({scrollLeft : scrollPosition }, 600)
    })
}
if(window.matchMedia("(min-width: 280px)")) {

    new bootstrap.Carousel(popCarousel, {
        interval: false
    });

    new bootstrap.Carousel(movCarousel, {
        interval: false
    });

    new bootstrap.Carousel(upcomCarousel, {
        interval: false
    });
    carouselItems($(".popular-next"), $(".popular-prev"), popularScrollPos, popularInner, popularItem, $(".popular-inner"), 2)
    carouselItems($(".movie-next"), $(".movie-prev"), movieScrollPos, movieInner, movieItem, $(".movie-inner"), 2)
    carouselItems($(".upcom-next"), $(".upcom-prev"), upcommingScrollPos, upcomInner, upcomItem, $(".upcomming-inner"), 2)

}else if(window.matchMedia("(min-width: 400px)")) {

    carouselItems($(".popular-next"), $(".popular-prev"), popularScrollPos, popularInner, popularItem, $(".popular-inner"), 6)
    carouselItems($(".movie-next"), $(".movie-prev"), movieScrollPos, movieInner, movieItem, $(".movie-inner"), 6)
    carouselItems($(".upcom-next"), $(".upcom-prev"), upcommingScrollPos, upcomInner, upcomItem, $(".upcomming-inner"), 6)

}else{
    (popCarousel).addClass("slide");
    (movCarousel).addClass("slide");
    (upcomCarousel).addClass("slide");
}
