new WOW().init();

$(".owl-carousel").owlCarousel({
    rtl: true,
    loop: true,
    nav: true,
    dots: false,
    responsive: {
        0:{
            items: 1
        },
        576:{
            items: 2
        },
        992:{
            items: 2
        },
        1200:{
            items: 2
        }
    }
});