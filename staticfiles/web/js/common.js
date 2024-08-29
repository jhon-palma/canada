/* ==================================================

   Initial

================================================== */





$.fn.isInViewport = function() {

    var elementTop = $(this).offset().top;

    var elementBottom = elementTop + $(this).outerHeight();



    var viewportTop = $(window).scrollTop();

    var viewportBottom = viewportTop + $(window).height();



    return elementBottom > viewportTop && elementTop < viewportBottom;

};



$.fn.extend({

	animateCss: function (animationName) {

		var animationEnd = 'webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend';

		this.addClass('animated ' + animationName).one(animationEnd, function() {

		$(this).removeClass('animated ' + animationName);

		});

	}

});



$(window).on('resize scroll', function() {

	

});









