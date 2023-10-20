const multipleCarousel = document.querySelector('#prevData')

if (window.matchMedia("(min-width:576px)")){



let carouselInner = $(".c-inner")[0].scrollWidth;
let carouselItem = $(".c-item").width()
let item = document.querySelectorAll(".c-item");
item[0].classList.add("active")

let carouselPos = 0

$(".carousel-control-next").on("click", () => {
    
    if(carouselPos < (carouselInner - (carouselItem * 10))){
        carouselPos += carouselItem;
        $(".c-inner").animate({scrollLeft: carouselPos}, 900);
    }
});

$(".carousel-control-prev").on("click", () => {

    if(carouselPos > 0){
        carouselPos -= carouselItem;
        $(".c-inner").animate({scrollLeft: carouselPos}, 900);
    }
});

}else{

    $(multipleCarousel).addClass("slide")

}


    



