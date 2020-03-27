$(document).ready(function(){
    setTimeout(function(){
       swiper1()
       swiper2()
    },100)

})

function swiper1(){
    var mySwiper1 = new Swiper('#topSwiper',{
        direction: 'horizontal',
        loop: true,
        speed: 500,
        autoplay: 2000,
        pagination: '.swiper-pagination',
        control: true,
        spaceBetween:2,
    });
};

function swiper2(){
    var mySwiper2 = new Swiper('#swiperMenu',{
        slidesPerView: 3,
        paginationClickable: true,
        loop: false,
        spaceBetween: 2,
        nextButton: '.swiper-button-next',
        prevButton: '.swiper-button-prev',
    });
};







