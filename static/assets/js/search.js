(function ($) {
	"use strict";

let suggestions = [];

const searchWrapper = document.querySelector(".header__search-input") != null ? document.querySelector(".header__search-input") : document.querySelector(".header__search-input-2");
const inputBox = searchWrapper.querySelector("input") != null ? searchWrapper.querySelector("input") : null;
const suggBox = searchWrapper.querySelector(".searched");
const icon = searchWrapper.querySelector(".search-button");
let linkTag = searchWrapper.querySelector("a");
let webLink;


$('html').click(function (e) {
    if(!$(e.target).parents().hasClass("searched")){
        suggBox.innerHTML = ''
    }
});

$( "#searchIcon" ).click(function() {
    if ($('.search-input').val() != '') {
        $('.search-input').val('')
        $('#searchIcon').animate({  textIndent: 0 }, {
            step: function(fx) {
              $(this).css('-webkit-transform','rotateY(90deg)');
            },
            duration: 100,
            complete: function() {
                        $(this).removeClass('fa-times')
                        $(this).addClass('fa-search')
                        $('#searchIcon').animate({  textIndent: 0 }, {
                            step: function(fx) {
                              $(this).css('-webkit-transform','rotateY(0deg)');
                            },
                            duration: 100,
                            complete: function() {
                                        $(this).removeClass('fa-times')
                                        $(this).addClass('fa-search')

                                      }
                        },'linear');

                      }
        },'linear');
    }
});

inputBox.onkeyup = (e)=>{
    var searched_list = $('.searched li').get()
    var userData = e.target.value;
    var categoriesArray = [];
    var typesArray = [];
    var productsArray = [];

    if (userData) {
        if ($('#searchIcon').hasClass('fa-search')) {
            $('#searchIcon').animate({  textIndent: 0 }, {
                step: function(fx) {
                  $(this).css('-webkit-transform','rotateY(90deg)');
                },
                duration: 100,
                complete: function() {
                            $(this).removeClass('fa-search')
                            $(this).addClass('fa-times')
                            $('#searchIcon').animate({  textIndent: 0 }, {
                                step: function(fx) {
                                  $(this).css('-webkit-transform','rotateY(0deg)');
                                },
                                duration: 100,
                                complete: function() {
                                            $(this).removeClass('fa-search')
                                            $(this).addClass('fa-times')

                                          }
                            },'linear');

                          }
            },'linear');
        }

        $.ajax({
            url: '/search/',
            type: 'GET',
            data: {
                'data': e.target.value,
            },

            success: function (response) {
                var products = response.products
                var categories = response.categories
                var types = response.types

                $.each(products ,function(index,value){
                    productsArray.push(this)
                });

                $.each(categories ,function(index,value){
                    categoriesArray.push(this)
                });

                $.each(types ,function(index,value){
                    typesArray.push(this)
                });

                typesArray = typesArray.map((data)=>{
                    return data = `<li class="cartmini__item p-relative d-flex align-items-start">
                                        <a class="d-flex" href="${data.url}">
                                            <div class="cartmini__thumb mr-15">
                                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16"
                                                     fill="currentColor" class="bi bi-arrow-90deg-right"
                                                     viewBox="0 0 16 16">
                                                    <path fill-rule="evenodd"
                                                          d="M14.854 4.854a.5.5 0 0 0 0-.708l-4-4a.5.5 0 0 0-.708.708L13.293 4H3.5A2.5 2.5 0 0 0 1 6.5v8a.5.5 0 0 0 1 0v-8A1.5 1.5 0 0 1 3.5 5h9.793l-3.147 3.146a.5.5 0 0 0 .708.708l4-4z"/>
                                                </svg>


                                            </div>
                                            <div class="cartmini__content">
                                                <h3 class="cartmini__title">
                                                    ${data.name}
                                                </h3>
                                            </div>
                                        </a>
                                    </li>`;
                });


                categoriesArray = categoriesArray.map((data)=>{
                    return data = `<li class="cartmini__item p-relative d-flex align-items-start">
                                        <a class="d-flex" href="${data.url}">
                                            <div class="cartmini__thumb mr-15">
                                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16"
                                                     fill="currentColor" class="bi bi-arrow-90deg-right"
                                                     viewBox="0 0 16 16">
                                                    <path fill-rule="evenodd"
                                                          d="M14.854 4.854a.5.5 0 0 0 0-.708l-4-4a.5.5 0 0 0-.708.708L13.293 4H3.5A2.5 2.5 0 0 0 1 6.5v8a.5.5 0 0 0 1 0v-8A1.5 1.5 0 0 1 3.5 5h9.793l-3.147 3.146a.5.5 0 0 0 .708.708l4-4z"/>
                                                </svg>


                                            </div>
                                            <div class="cartmini__content">
                                                <h3 class="cartmini__title">
                                                    ${data.name}
                                                </h3>
                                            </div>
                                        </a>
                                    </li>`;
                });


                suggestions = productsArray;
                productsArray = productsArray.map((data)=>{
                    return data = `<li class="cartmini__item p-relative d-flex align-items-start">
                                        <a class="d-flex" href="${data.url}">
                                            <div class="cartmini__thumb mr-15">

                                                    <img src="${data.image}" alt="${data.name}">

                                            </div>
                                            <div class="cartmini__content">
                                                <h3 class="cartmini__title">
                                                    ${data.name}
                                                </h3>
                                            </div>
                                        </a>
                                    </li>`;
                });
                let result = categoriesArray.concat(typesArray).concat(productsArray);
                showSuggestions(result);
            }
        });

    } else {
        if ($('#searchIcon').hasClass('fa-times')) {
            $('#searchIcon').animate({  textIndent: 0 }, {
                step: function(fx) {
                  $(this).css('-webkit-transform','rotateY(90deg)');
                },
                duration: 100,
                complete: function() {
                            $(this).removeClass('fa-times')
                            $(this).addClass('fa-search')
                            $('#searchIcon').animate({  textIndent: 0 }, {
                                step: function(fx) {
                                  $(this).css('-webkit-transform','rotateY(0deg)');
                                },
                                duration: 100,
                                complete: function() {
                                            $(this).removeClass('fa-times')
                                            $(this).addClass('fa-search')

                                          }
                            },'linear');

                          }
            },'linear');
        }
        suggBox.innerHTML = ''
    }
}

function showSuggestions(list){
    let listData;
    if(!list.length){
        var userValue = inputBox.value;
        listData = `<li class="cartmini__item p-relative d-flex align-items-start empty-search">
                            <div class="cartmini__content">
                                <p class="cartmini__title searched_nothing">
                                    We didn't find anything. Try to use <a href="/shop/">our catalog</a>
                                </p>
                            </div>
                    </li>`;
    }else{
      listData = list.join('');
    }
    suggBox.innerHTML = listData;
}

})(jQuery);

