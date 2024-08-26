var sliderthumb;

var sliderfiche;



var sliderthumbcont = $(".thumslist").html();

var sliderfichecont = $(".ficheslidercont").html();



$(document).ready(function(){

	$("a.avanceea").click(function(e){

		e.preventDefault();

		$('.avanceediv').slideToggle();

	});

	var sliderthumbcont = $(".thumslist").html();

	var sliderfichecont = $(".ficheslidercont").html();

	

    //Nouvelle fiche détail

    $(".hiddenfiche").hide();

	$('a.openfiche:not(.openfiche2):not(.close)').click(function(e){

        e.preventDefault();

        $(this).prev(".hiddenfiche").slideDown();

        $(this).hide();

        $(this).next('a').css('display', 'block');

    });

    

    $('a.openfiche.openfiche2:not(.close)').click(function(e){

        e.preventDefault();

        $(this).prev("p.fullfichep").slideDown();

        $(this).prev("p.fullfichep").prev("p").slideUp();

        $(this).hide();

        $(this).next('a').css('display', 'block');

    });

    

    $('a.openfiche.close:not(.openfiche2)').click(function(e){

        e.preventDefault();

        $(this).prev('a').prev(".hiddenfiche").slideUp();

        $(this).hide();

        $(this).prev('a').css('display', 'block');

    });

    

    $('a.openfiche.openfiche2.close').click(function(e){
        e.preventDefault();
        $(this).prev('a').prev("p.fullfichep").slideUp();
        $(this).prev('a').prev("p.fullfichep").prev("p").slideDown();
        $(this).hide();
        $(this).prev('a').css('display', 'block');

    });

    

    $('.navcalculateurs a').click(function(e){
        e.preventDefault();
        $('.navcalculateurs a.active').removeClass('active');
        $('.pannelcalcul.active').removeClass('active');
        $(this).addClass('active');
        var href = $(this).attr('href');
        $('.'+href).addClass('active');

    });


    $('a.btnpopfiche').click(function(e){

        e.preventDefault();

        var title = $(this).text();

		var buttonTxt = $(this).attr("name");

		$('#submitFiche').val(buttonTxt);

		

        $('.popfiche h2').text(title);

		$("[name=objet]").val(title);
        $('#sujet-2').val(title);
		

		$("#formfiche").show();

        $('.popfiche').fadeIn();

    });

    $('.popfiche .close').click(function(e){

        e.preventDefault();

        $('.popfiche').fadeOut();

		$("#formfiche").trigger("reset");

		$("#confirm_message").html("");

    });


	if($('.fullscreenfiche').length){

        $('.fullscreenfiche').magnificPopup({

          type: 'image',

          gallery:{

            enabled:true

          },

		  callbacks: {

			open: function() {

                $("body").swipe({

                    swipeLeft: function(event, direction, distance, duration, fingerCount) {

                        $(".mfp-arrow-left").magnificPopup("prev");

                    },

                    swipeRight: function() {

                        $(".mfp-arrow-right").magnificPopup("next");

                    },

                    threshold: 50,

                    excludedElements: "label, button, input, select, textarea, p"

                });

             },

			 close: function() {

			 }

		   }

        });

		

    }

    //Fin Nouvelle fiche détail

    

	$('.menu-ico').click(function(){

		$('header nav').slideToggle();

	});

	

	

	

	function YTid(url){

		var videoid = url.match(/(?:https?:\/{2})?(?:w{3}\.)?youtu(?:be)?\.(?:com|be)(?:\/watch\?v=|\/)([^\s&]+)/);

		if(videoid != null) {

		   //console.log("video id = ",videoid[1]);

			return videoid[1];

		}

	}

    

    function GetVimeoIDbyUrl(url) {

	  var id = false;

	  $.ajax({

		url: 'https://vimeo.com/api/oembed.json?url='+url,

		async: false,

		success: function(response) {

		  if(response.video_id) {

			id = response.video_id;

		  }

		}

	  });

	  return id;

	}

    

    $('span.close').click(function(){

		$('.poppod, .popnews, .popwwu').fadeOut();

		if($('.poppod').length){

			$('.poppod article').html("");

		}

		if($('.popwwu').length){

			$("#confirmationContact").html("");

			$("#confirmationBuyers").html("");

			$("#confirmationListing").html("");

			$('#formContact')[0].reset();

			$('#formBuyers')[0].reset();

			$('#formListing')[0].reset();

			$('#formContact').show();

			$('#formBuyers').show();

			$('#formListing').show();

		}

			

	});

	

	$('.capsule .bouton, .capsule .img, .capswrap .img, .videoshomecont a').click(function(e){

		e.preventDefault();

		

		var url = $(this).attr('href');

		var yt = "youtube";

		var vim = "vimeo";

		if(url.indexOf(yt) != -1){

			$('.poppod article').html("<iframe width='560' height='315' src='https://www.youtube.com/embed/"+YTid(url)+"' frameborder='0' allow='autoplay; encrypted-media' allowfullscreen></iframe>");

		}else if(url.indexOf(vim) != -1){

			$('.poppod article').html("<iframe src='https://player.vimeo.com/video/"+GetVimeoIDbyUrl(url)+"' width='640' height='360' frameborder='0' webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>");

		}

		

		

		$('.poppod').fadeIn();

	});

	

	$('.capsules .capsule p a').on('click', function(e){

		e.preventDefault();

		$('.capsule').css('height','auto');

		$(this).parent('p').slideUp();

		$(this).parent('p').siblings('p:not(.sm)').slideDown("fast",function(){

			

			setTimeout(function(){

                    

                    //$('.capsules .wrap').msrItems('refresh');

                    if($(window).width() > 800){

                        $('.capsules .wrap').msrItems({

                            'colums': 3, //columns number

                            'margin': 30 //right and bottom margin

                        });

                    }else{

                        $('.capsules .wrap').msrItems({

                            'colums': 2, //columns number

                            'margin': 15 //right and bottom margin

                        });

                    }

                    

                    $('.capsule').each(function(){

                        $(this).css('height','auto');

                        $(this).height($(this).height());

                    });

                    if($(window).width() > 800){

                        $('.capsules .wrap').msrItems({

                            'colums': 3, //columns number

                            'margin': 30 //right and bottom margin

                        });

                    }else{

                        $('.capsules .wrap').msrItems({

                            'colums': 2, //columns number

                            'margin': 15 //right and bottom margin

                        });

                    }

                }, 300);

			

		});

		

	});

	

	$('.openNewletter').click(function(e){
		e.preventDefault();
		$('#newsteller').fadeIn();

	});

	
	$('a.btn-wwu').click(function(e){

		e.preventDefault();

		$('.popwwu.'+$(this).attr('data-pop')).fadeIn();

	});



	$.fn.visible = function(partial) {

    

      var $t            = $(this),

          $w            = $(window),

          viewTop       = $w.scrollTop(),

          viewBottom    = viewTop + $w.height(),

          _top          = $t.offset().top,

          _bottom       = _top + $t.height(),

          compareTop    = partial === true ? _bottom : _top,

          compareBottom = partial === true ? _top : _bottom;

    

    return ((compareBottom <= viewBottom) && (compareTop >= viewTop));



  };

	$(window).scroll(function(event) {

		

		$('.statel .num').each(function () {

			if(!$(this).hasClass('counting') && $(this).visible(true)){

				

				$(this).addClass('counting');

				$(this).prop('Counter',0).animate({

					Counter: $(this).text()

				}, {

					duration: 1000,

					easing: 'swing',

					step: function (now) {

						$(this).text(Math.round(now * 100) / 100);

					}

				});

			}

		});

	});

		

});







$(window).load(function(){

	var sliderthumbcont = $(".thumslist").html();

	var sliderfichecont = $(".ficheslidercont").html();

	

    //Nouvelle fiche détail

	$(".navmedia a.selected").click(function(e){

		e.preventDefault();

	});

	

    if($('.thumbpager').length){



		if($(window).width() > 700){

			var slideimgH = $(".ficheslide>img").height();

		

			$(".ficheslide>img").each(function(){

				if($(this).height() < slideimgH){

					slideimgH = $(this).height();

				}

			});



			$(".thumslist img").height((slideimgH+20) / 5);



			sliderthumb=$('.thumbpager').bxSlider({

				mode: 'vertical',

				minSlides: 5,

				maxSlides: 6,

				moveSlides:1,

				pager:false

			});

		}else{

			var thumbW = ($(window).width() - 20 ) / 5;

			sliderthumb=$('.thumbpager').bxSlider({

				mode: 'horizontal',

				minSlides: 5,

				maxSlides: 6,

				moveSlides:1,

				slideWidth:thumbW,

				pager:false

			});

		}

        

    }

    if($('.ficheslidercont>div:first-child').length){

        sliderfiche=$('.ficheslidercont>div:first-child').bxSlider({

            mode: 'horizontal',

            auto: false,

            pagerCustom: '.thumbpager',

            adaptiveHeight: true,

			useCSS: false

        });

    }

    

    //Fin Nouvelle fiche détail

    if($('.temslider').length){

        $(".temslider").bxSlider({

            mode: 'fade',

            prevText: "<",

            nextText: ">",

            pager: false,

            auto: true,

            adaptiveHeight: true

        });

    }

    if($('.slider').length){

        $(".slider").bxSlider({

            mode: 'fade',

            controls: false,

            pager: false,

            auto: true,

            adaptiveHeight: true

        });

    }

	

	

	$(window).resize(function(){

	//sliderthumb.destroySlider();

	//	sliderfiche.destroySlider();

		$(".ficheslidercont .bx-wrapper").remove();

		$(".thumslist .bx-wrapper").remove();

		$(".ficheslidercont").html(sliderfichecont);

		$(".thumslist").html(sliderthumbcont);



		if($(window).width() > 700){

			var slideimgH = $(".ficheslide>img").height();



			$(".ficheslide>img").each(function(){

				if($(this).height() < slideimgH){

					slideimgH = $(this).height();

				}

			});



			$(".thumslist img").height((slideimgH+20) / 5);



			sliderthumb=$('.thumbpager').bxSlider({

				mode: 'vertical',

				minSlides: 5,

				maxSlides: 6,

				moveSlides:1,

				pager:false

			});

		}else{

			var thumbW = ($(window).width() - 20 ) / 5;

			sliderthumb=$('.thumbpager').bxSlider({

				mode: 'horizontal',

				minSlides: 5,

				maxSlides: 6,

				moveSlides:1,

				slideWidth:thumbW,

				pager:false

			});

		}

		sliderfiche=$('.ficheslidercont>div:first-child').bxSlider({

			mode: 'horizontal',

			auto: false,

			pagerCustom: '.thumbpager',

			adaptiveHeight: true,

			useCSS: false

		});



	});

});





$(window).scroll(function(){

	//Nouvelle fiche détail

	if($('.descriptionbloc').length){

		if($(window).width() >= 800){

			var asidetotop = $('.descriptionbloc').offset().top - $(window).scrollTop();

			if(asidetotop <= 70){

				$('.descriptionbloc aside').addClass('fixedaside');

			}else{

				$('.descriptionbloc aside').removeClass('fixedaside');

			}

		}

	}

	//Fin Nouvelle fiche détail

});



