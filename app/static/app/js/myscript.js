$('#slider1, #slider2, #slider3').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 5,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})

// ----------------------------startplus---------------------------------
$('.plus-cart').click(function() {
    var id = $(this).attr("pid").toString(); // Fix the typo: "attrs" should be "attr"
    var eml = this.parentNode.children[2]

    // Use $.ajax instead of $.ajex
    $.ajax({
        type: "GET",
        url: "/pluscart",
        data: {
            prod_id: id // Fix the typo: "=" should be ":"
        },
        success: function(data) {
            eml.innerText = data.quantity
            document.getElementById("amount").innerText = data.amount
            document.getElementById("totalamount").innerText = data.totalamount

        }
    });
});

// ----------------------------------Endplus-------------------------------


//----------------------------------startmiuns----------------------------------
$('.minus-cart').click(function() {
    var id = $(this).attr("pid").toString(); // Fix the typo: "attrs" should be "attr"
    var eml = this.parentNode.children[2]

    // Use $.ajax instead of $.ajex
    $.ajax({
        type: "GET",
        url: "/minuscart",
        data: {
            prod_id: id // Fix the typo: "=" should be ":"
        },
        success: function(data) {
            eml.innerText = data.quantity
            document.getElementById("amount").innerText = data.amount
            document.getElementById("totalamount").innerText = data.totalamount

        }
    });
});

// -------------------------------------Endmiuns-----------------------


$('.remove-cart').click(function() {
    var id = $(this).attr("pid").toString(); // Fix the typo: "attrs" should be "attr"
    var eml = this

    // Use $.ajax instead of $.ajex
    $.ajax({
        type: "GET",
        url: "/removecart",
        data: {
            prod_id: id // Fix the typo: "=" should be ":"
        },
        success: function(data) {
            console.log("Delete")
            document.getElementById("amount").innerText = data.amount
            document.getElementById("totalamount").innerText = data.totalamount
            eml.parentNode.parentNode.parentNode.parentNode.remove()
        }
    });
});