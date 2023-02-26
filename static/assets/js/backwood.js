if (!$) {
    $ = django.jQuery;
}

function getCookie(name) {
let cookieValue = null;
if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
        }
    }
}
return cookieValue;
}

function setCookie(name, value, options = {}) {

    options = {
        path: '/',
    };

    if (options.expires instanceof Date) {
        options.expires = options.expires.toUTCString();
    }

    let updatedCookie = encodeURIComponent(name) + "=" + encodeURIComponent(value);

    for (let optionKey in options) {
        updatedCookie += "; " + optionKey;
        let optionValue = options[optionKey];
        if (optionValue !== true) {
            updatedCookie += "=" + optionValue;
        }
    }

    document.cookie = updatedCookie;
}

function deleteCookie(name) {
    setCookie(name, "", {
        'max-age': -1
    })
}

const csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function isFilter() {

    if($('#isFilter').val() == 'true') {
        x = setTimeout(function () {
            $("#clearButton").fadeIn(400)
        }, 1000)

    } else {
        x = setTimeout(function () {
            $("#clearButton").fadeOut(100)
        }, 50)
    }
}


$(document).ready(function() {
    isFilter()
});

$("#headerInfoButton").click(function(){

    setCookie('header_banner', 'accepted')

    $('.header-safeinfo').stop().animate({
        height: "0px",
        opacity: 0,
        padding: 0,
        borderWidth: 0
    }, 300, function() {
        $(this).remove();
    })
});


$(document).on('submit', '.add-product-form', function(e){
    e.preventDefault()
    var form = $(this)
    var button = $(form).find('button')
    var url = $(this).attr("action")
    var defaultData = {
        'csrftoken': csrftoken,
        'quantity': '1',
        'override': 'False',
        'slug': $('#id_slug').val(),
        'location': window.location.pathname,
    }

    var postData = ($(this).hasClass('miniproduct-form')) ? defaultData : $(this).serialize()
    $.ajax({
        url: url,
        type: 'POST',
        cache: false,
        data: postData,

        success: function (response) {
            if (response.err) {

                $(button).attr('active', false)
                $(button).attr('data-tooltip', response.err)

                if ($(button).find('i').hasClass('fa-shopping-cart')) {

                    $(button).find('i').animate({  textIndent: 0 }, {
                        step: function(fx) {
                          $(this).css('-webkit-transform', 'rotateY(90deg)');
                        },
                        duration: 170,
                        complete: function() {
                                    $(this).removeClass('fa-shopping-cart')
                                    $(this).addClass('fa-times')
                                    $(button).find('i').animate({  textIndent: 0 }, {
                                        step: function(fx) {
                                          $(this).css('-webkit-transform','rotateY(0deg)');
                                        },
                                        duration: 0,
                                        complete: function() {
                                                    setTimeout(function(){
                                                        $(button).find('i').animate({  textIndent: 0 }, {
                                                            step: function(fx) {
                                                              $(this).css('-webkit-transform','rotateY(90deg)');
                                                            },
                                                            duration: 170,
                                                            complete: function() {
                                                                        $(this).removeClass('fa-times')
                                                                        $(this).addClass('fa-shopping-cart')
                                                                        $(button).find('i').animate({  textIndent: 0 }, {
                                                                            step: function(fx) {
                                                                              $(this).css('-webkit-transform','rotateY(0deg)');
                                                                            },
                                                                            duration: 0},'linear');
                                                                      }
                                                        },'linear');
                                                    }, 1200)
                                                  }
                                    },'linear');

                                  }
                    },'linear');
                } else if ($(button).hasClass('miniproduct-btn')) {
                    if (!$('.cart-add-errors').length ) {
                        $(button).after('<span class="cart-add-errors"></span>')
                    }
                    $('.cart-add-errors').text(response.err)
                }
            } else {
                $(button).attr('active', true)
                $('.cart-add-errors').remove()

                if ($(button).hasClass('add-cart-btn') || $(button).hasClass('wood-cart-btn') ||
                    $(button).hasClass('add-to-cart-btn')) {
                    var btn_width = $(button).outerWidth()
                    $(button).css('width', btn_width);

                    $(button).animate({fontSize: '0.91em'}, {
                        duration: 100
                    },'linear');
                } else {
                    $(button).find('i').animate({  textIndent: 0 }, {
                        step: function(fx) {
                          $(this).css('scale', '0.8');
                        },
                        duration: 100,
                        complete: function() {

                                    $(button).find('i').animate({  textIndent: 0 }, {
                                        step: function(fx) {
                                          $(this).css('scale', '0.8');
                                        },
                                        duration: 0,
                                        complete: function() {
                                                        $(button).find('i').animate({  textIndent: 0 }, {
                                                            step: function(fx) {
                                                              $(this).css('scale', '1');
                                                            },
                                                            duration: 100,
                                                            complete: function() {
                                                                      }
                                                        },'linear');
                                                  }
                                    },'linear');

                                  }
                    },'linear');
                }

                $('.cart_and_wish').html(response.sidebar_actions)

                if (window.location.pathname != '/') {
                        $('.header__action').html(response.header_actions)
                } else {
                    $('.header__bottom-right-render').html(response.header_actions)
                }

                $.ajax({
                    type: 'GET',
                    url: '/cart/cart/',
                    headers: {
                        "accept": "application/json",
                        "Access-Control-Allow-Origin":"*"
                    },
                    success: function (response) {
                        $('#cartMiniModal').html(response)
                    }
                });
            }

        }
    });
});

$(document).on('submit', '.remove-product-form', function(e){
    e.preventDefault()
    var url = $(this).attr("action")
    var parent = $(this).parent('td')
    var cart_total_price = ''

    if (parent.length != 0) {
        cart_total_price = 'True'
    }
    $.ajax({
        url: url,
        type: 'POST',
        cache: false,
        data: {
            'csrftoken': csrftoken,
            'cart_total_price': cart_total_price,
            'location': window.location.pathname
        },

        success: function (response) {

            if (parent.length != 0) {
                $(parent).parent().remove()
                $('#cartTotalPrice').html('$' + response.cart_total_price)
                if (response.cart == 'empty') {
                    $('.cart-area .container').html(response.empty_cart)
                }
            } else {
                $('.cart_and_wish').html(response.sidebar_actions)

                if (window.location.pathname != '/') {
                        $('.header__action').html(response.header_actions)
                } else {
                    $('.header__bottom-right-render').html(response.header_actions)
                }

                $.ajax({
                    type: 'GET',
                    url: '/cart/cart/',
                    headers: {
                        "accept": "application/json",
                        "Access-Control-Allow-Origin":"*"
                    },
                    success: function (response) {
                        $('#cartMiniModal').html(response)
                    }
                });
            }
        }
    });
});


function filterProducts(data) {
    $('.products-overlay').css('display', 'block')
    clearTimeout(timer);
    var colours = $('#filterColors').closest('form').serialize()
    var categories = $('#filterCategories').closest('form').serialize()
    if (categories || colours) {
        var post_data = {
                'colours': colours,
                'categories': categories,
                'price': $('#amount').val()
            }
    } else {
        if ($('#amount').val()) {
            var post_data = {
                'price': $('#amount').val()
            }
        } else {
            var post_data = ''
        }
    }

    timer = setTimeout(function () {
        $.ajax({
            url: '/shop/',
            type: 'GET',
//            cache: true,
            data: post_data,
            success: function (response) {
                $('.col-xxl-9').html(response)
//                $('.products-overlay').css('display', 'none')
                if (post_data == '') {
                    $('#isFilter').val(false)
                    isFilter()
                } else {
                    $('#isFilter').val(true)
                    isFilter()
                }

            }
        });
    }, 800);
}


var timer = 0;
$('#filterCategories input[type="checkbox"]').on('change', function(){
    data = ''
    filterProducts(data)
});

$('#filterAmount').on('click', function(){
    if ($('#amount').val()) {
        data = ''
        filterProducts(data)
    }
});

$('#filterColors input[type="checkbox"]').on('change', function(){
    values = []
    data = ''
    $.each(data, function(){
        values.push(this.value)
    });

    pre_data = {
        'colours': values
    }
    filterProducts(JSON.stringify(pre_data))
});

$('#clearButton button').on('click', function(){
    $('input:checkbox:checked').each(function(){
        $(this).prop('checked', false)
    });
    $('#amount').val('')
    $('#isFilter').val(false)
    isFilter()
    data = ''
    filterProducts(data)
});

var exampleModal = document.getElementById('productModalId')

if (exampleModal) {
    exampleModal.addEventListener('show.bs.modal', function (event) {
        $(".cart-plus-minus").append('<div class="dec qtybutton">-</div><div class="inc qtybutton">+</div>');

        var button = event.relatedTarget

        var recipient = button.getAttribute('data-bs-target')
        var product_name = button.getAttribute('data-name')
        $.ajax({
            url: '/products/' + product_name,
            type: 'GET',
            cache: false,
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": getCookie("csrftoken"),
            },
            success: function (response) {
                $(exampleModal).html(response)
            }
        });
    })
}

function invoicePrint() {
    var divToPrint = document.getElementById('invoice');
    var newWin = window.open('','Print-Window');

    newWin.document.open();
    newWin.document.write(`
    <html>
    <head>
    <style>

.invoice-wrapper{
    background:#eee;
}

.invoice {
    background: #fff;
    padding: 20px
}

.invoice-company {
    font-size: 20px
}

.invoice-header {
    margin: 0 -20px;
    background: #f0f3f4;
    padding: 20px
}

.invoice-date,
.invoice-from,
.invoice-to {
    display: table-cell;
    width: 1%
}

.invoice-from,
.invoice-to {
    padding-right: 20px
}

.invoice-date .date,
.invoice-from strong,
.invoice-to strong {
    font-size: 16px;
    font-weight: 600
}

.invoice-date {
    text-align: right;
    padding-left: 20px
}

.invoice-price {
    background: #f0f3f4;
    display: table;
    width: 100%
}

.invoice-price .invoice-price-left,
.invoice-price .invoice-price-right {
    display: table-cell;
    padding: 20px;
    font-size: 20px;
    font-weight: 600;
    width: 75%;
    position: relative;
    vertical-align: middle
}

.invoice-price .invoice-price-left .sub-price {
    display: table-cell;
    vertical-align: middle;
    padding: 0 20px
}

.invoice-price small {
    font-size: 12px;
    font-weight: 400;
    display: block
}

.invoice-price .invoice-price-row {
    display: table;
    float: left
}

.invoice-price .invoice-price-right {
    width: 25%;
    background: #2d353c;
    color: #fff;
    font-size: 28px;
    text-align: right;
    vertical-align: bottom;
    font-weight: 300
}

.invoice-price .invoice-price-right small {
    display: block;
    opacity: .6;
    position: absolute;
    top: 10px;
    left: 10px;
    font-size: 12px
}

.invoice-footer {
    border-top: 1px solid #ddd;
    padding-top: 10px;
    font-size: 10px
}

.invoice-note {
    color: #999;
    margin-top: 80px;
    font-size: 85%
}

.invoice>div:not(.invoice-footer) {
    margin-bottom: 20px
}

.btn.btn-white, .btn.btn-white.disabled, .btn.btn-white.disabled:focus, .btn.btn-white.disabled:hover, .btn.btn-white[disabled], .btn.btn-white[disabled]:focus, .btn.btn-white[disabled]:hover {
    color: #2d353c;
    background: #fff;
    border-color: #d9dfe3;
}

.pull-right {
    float: right;
}
    </style>
    </head>
    <body onload="window.print()">${divToPrint.innerHTML}
    </body>
    </html>`);

    newWin.document.close();
    setTimeout(function(){newWin.close();},10);
}
$('#couponForm').submit(function(e){
e.preventDefault()

if ($('#coupon_code').val() != '') {
        $.ajax({
            url: '/coupon/apply/',
            type: 'POST',
            cache: false,
            data: {
                'csrftoken': csrftoken,
                'code': $('#coupon_code').val()
            },

            success: function (response) {
                var message = response
                var path = window.location.pathname
                if (path == '/order/checkout/') {
                    $.ajax({
                        url: path,
                        type: 'GET',
                        cache: false,
                        data: {
                            'csrftoken': csrftoken,
                        },

                        success: function (response) {
                            $('#orderTotal').text('$'+ response.total)
                            $('.checkout-area').stop().animate({
                                paddingTop: '70px'
                            })
                            $('#couponBlock').stop().animate({
                                    height: "0px",
                                    opacity: 0,
                                    padding: 0
                                }, 400, function() {
                                    $(this).remove();
                                    var element = $('<tr class="cart-subtotal"><th>Coupon</th><td><span>%' + response.discount + ' ($' + response.get_discount +')</span></td></tr>' )
                                    $(element).hide()
                                    $('#shipping').after($(element).slideDown(66000, 'linear', ))
                                    $('main').prepend(message)

                                }
                            );
                        }
                    });
                } else {
                    $('main').prepend(message)
                    $.ajax({
                        url: '/cart/',
                        type: 'GET',
                        cache: false,
                        data: {
                            'csrftoken': csrftoken,
                        },

                        success: function (response) {
                            $('#cartTotalPrice').text('$'+ response.total)
                            $('#couponBlock').stop().animate({
                                    height: "0px",
                                    opacity: 0,
                                }, 400, function() {
                                    $(this).remove();
                                    var element = $('<li>Coupon <span>%'+  response.discount + ' (<span id="cartDiscount">$' + response.get_discount + '</span>)</span></li>')
                                    $(element).hide()
                                    $('#cartSubTotalPrice').after($(element).slideDown(400, 'linear', ))
                                }
                            );
                        }
                    });
                }
            },

            error: function () {
                $('#coupon_code').val('')
                $("#couponForm").effect( "shake",
                {times:2,distance: 5}, 500 );
            }
        });
    }
})

$(document).on('submit', '.add-wish-product-form', function(e){
    e.preventDefault()
    var url = $(this).attr("action")
    $(this).find('.like-button').toggleClass('animate')

    $.ajax({
        url: url,
        type: 'POST',
        cache: false,
        data: {
            'product_id': $(this).children('#product_id').val(),
            'location': window.location.pathname,
        },

        success: function (response) {
            $('.cart_and_wish').html(response.sidebar_actions)

            if (window.location.pathname != '/') {
                    $('.header__action').html(response.header_actions)
            } else {
                $('.header__bottom-right-render').html(response.header_actions)
            }
        }
    });
});

$(document).on('submit', '.remove-wish-product-form', function(e){
    e.preventDefault()
    var url = $(this).attr("action")

    $.ajax({
        url: url,
        type: 'POST',
        cache: false,
        data: {
            'product_id': $(this).children('#product_id').val(),
        },

        success: function (response) {
            $('.favourites').html(response)
        }
    });
});

$('#contacts-form').on('submit', function(e){
    e.preventDefault()
    var url = window.location.pathname
    $.ajax({
        url: url,
        type: 'POST',
        cache: false,
        data: $(this).serialize(),

        success: function (response) {

            if (response != '') {
                $('#contacts-form').stop().animate({
                        height: "0px",
                        opacity: 0,
                        padding: 0
                    }, 400, function() {
                        $(this).remove();
                        $('main').prepend(response)
                    }
                );
            }

        }
    });
});

$("[data-tooltip]").mousemove(function (eventObject) {

    if ($(this).attr('active') == 'false') {
        $data_tooltip = $(this).attr("data-tooltip");
        $("#tooltip").text($data_tooltip)
            .css({
             "top" : eventObject.pageY + 5,
            "left" : eventObject.pageX + 5
            })
            .show();
    }

}).mouseout(function () {

    $("#tooltip").hide()
                 .text("")
                 .css({
                     "top" : 0,
                    "left" : 0
                 });
});

