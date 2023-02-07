(function ($) {
	"use strict";

        $('input').on('keyup', function(e) {
            if ($('.errorlist').length) {
                console.log($('.errorlist').prevAll('input'))
                $(this).nextAll('.errorlist').remove()
            }
        });

})(jQuery);