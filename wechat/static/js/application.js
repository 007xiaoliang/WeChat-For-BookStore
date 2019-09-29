
//  page javascripts
var rating = function(ele){
    var vi = ele.attr("data-value");
    for(i=0; i<vi ;i++)
    {
      ele.children().eq(i).addClass("rated");
    }
}
function parseURL(url) {
    var a =  document.createElement('a');
    a.href = url;
    return {
        source: url,
        protocol: a.protocol.replace(':',''),
        host: a.hostname,
        port: a.port,
        query: a.search,
        params: (function(){
            var ret = {},
                seg = a.search.replace(/^\?/,'').split('&'),
                len = seg.length, i = 0, s;
            for (;i<len;i++) {
                if (!seg[i]) { continue; }
                s = seg[i].split('=');
                ret[s[0]] = s[1];
            }
            return ret;
        })(),
        file: (a.pathname.match(/\/([^\/?#]+)$/i) || [,''])[1],
        hash: a.hash.replace('#',''),
        path: a.pathname.replace(/^([^\/])/,'/$1'),
        relative: (a.href.match(/tps?:\/\/[^\/]+(.+)/) || [,''])[1],
        segments: a.pathname.replace(/^\//,'').split('/')
    };
}


$(function(){
  $(document).on('click',".menu>li",function(){
    if($(this).find(".mmenu-submenu").is(":visible"))
    {
      $(this).find(".mmenu-submenu").hide();
    }else{
      $(this).find(".mmenu-submenu").show();
      $(this).siblings("li").find(".mmenu-submenu").hide();
    }

  });

  $(document).scroll(function() {
		if($(document).scrollTop()!==0 )
		{
			$(".backToTop").fadeIn(500);
		}
		else{
			$(".backToTop").fadeOut(500);
		}
	});
  $(".backToTop").on('click',function(e){
		e.preventDefault();
		$(document.documentElement).animate({
			scrollTop: 0
		},200);
		//鏀寔chrome
		$(document.body).animate({
			scrollTop: 0
		},200);
	});

  $.fn.scrollTo =function(options){
         var defaults = {
             toT : 0,    //滚动目标位置
             durTime : 500,  //过渡动画时间
             delay : 30,     //定时器时间
             callback:null   //回调函数
         };
         var opts = $.extend(defaults,options),
             timer = null,
             _this = this,
             curTop = _this.scrollTop(),//滚动条当前的位置
             subTop = opts.toT - curTop,    //滚动条目标位置和当前位置的差值
             index = 0,
             dur = Math.round(opts.durTime / opts.delay),
             smoothScroll = function(t){
                 index++;
                 var per = Math.round(subTop/dur);
                 if(index >= dur){
                     _this.scrollTop(t);
                     window.clearInterval(timer);
                     if(opts.callback && typeof opts.callback == 'function'){
                         opts.callback();
                     }
                     return;
                 }else{
                     _this.scrollTop(curTop + index*per);
                 }
             };
         timer = window.setInterval(function(){
             smoothScroll(opts.toT);
         }, opts.delay);
         return _this;
     };
});

$(function(){
      $("select").on('change',function(){
           $(this).css({'color':'#333'});
       });


    if($(".tabmenu .menu2").length>0)
    {
      $(".tabmenu .menu2").navfix(0,99);
    }

    $('.slide').swipeSlide({
        continuousScroll:true,
        speed : 3000,
        transitionType : 'cubic-bezier(0.22, 0.69, 0.72, 0.88)',
        autoSwipe:true,
        lazyLoad:true,
        firstCallback : function(i,sum,me){
            me.find('.dot').children().first().addClass('cur');
        },
        callback : function(i,sum,me){
            me.find('.dot').children().eq(i).addClass('cur').siblings().removeClass('cur');
        }
    });

    $(document).on('click','.popslides',function(){
      if($(this).hasClass("active"))
      {
        $(this).removeClass("active");
        $(this).removeAttr("style");
        $(this).find("img").removeAttr("style");
      }else{
        $(this).addClass("active");
        $(this).css({
          "position":"fixed",
          "width":"100%",
          "z-index":"1",
          "height":$(window).height()+'px',
          "background":"#000",
          "top":"0"
        });
        $(this).find("img").each(function(){
          $(this).css({
            "top":"50%",
            "margin-top": '-' + $(this).height()/2+'px'
          });
        });
      }
    });



    $(".standard>div input[type=radio]").each(function(){
      $(this).hide();
      var obj = $("<a>"+$(this).val()+"</a>");
      obj.insertAfter($(this));
      if($(this).attr("checked"))
      {
        obj.addClass("active");
      }
      obj.on('click',function(){
        $(this).addClass("active");
        $(this).prev("input[type=radio]").attr("checked","checked");
        $(this).prev("input[type=radio]").trigger("click");
        $(this).prev("input[type=radio]").siblings("input[type=radio]").removeAttr("checked");
        $(this).siblings("a").removeClass("active");
      });
    });

    $(".standard>div input[type=checkbox]").each(function(){
      $(this).hide();
      var obj = $("<a>"+$(this).val()+"</a>");
      obj.insertAfter($(this));
      if($(this).attr("checked"))
      {
        obj.addClass("active");
      }
      obj.on('click',function(){
        if($(this).hasClass("active"))
        {
          $(this).removeClass("active");
          $(this).prev("input[type=checkbox]").removeAttr("checked");
          $(this).prev("input[type=radio]").trigger("click");
        }else{
          $(this).addClass("active");
          $(this).prev("input[type=radio]").trigger("click");
          $(this).prev("input[type=checkbox]").attr("checked","checked");
        }
      });
    });


    $(".star-score").each(function(){
      rating($(this));
    });

    $(document).on("click",function(e){
  		var target  = $(e.target);
      var bh = $(window).height();
  		if(target.closest(".dropdown-toggle").length === 0){
        $(".dropdown").removeClass("open");
        $(".wrapper form").removeClass("fixedform");
        $(".dropdown .blackbg").remove();
        $(".btnfixed").hide();
        $("body").css({"overflow":"auto","height":"auto","min-height":bh});
  		}
  	});

  $(document).on('touchend','[data-type=popbox]',function(){
    var target = $(this).attr("data-href");
    if($(this).hasClass("empty"))
    {
      return;
    }else{
      $("#" + target).show();
      var obj =$("<div class='blackbg bgprebuy' style='position:fixed; height:100%; top:0;'></div>");
      obj.insertAfter("body");
      obj.on('click',function(){
        $("#" + target).hide();
        obj.remove();
      });
      $("[data-dismiss=popbox]").on("click",function(){
        $("#" + target).hide();
        obj.remove();
      });
    }
  });

  $(".addresslists>div>ul").swipe( {
        //Single swipe handler for left swipes
        swipeLeft:function(event, direction, distance, duration, fingerCount) {
          if(!$(this).parent("div").hasClass("active"))
          {
            var height = $(this).parent("div").outerHeight();
            var move = $(this).next(".hidebtn-group").width();
            $(this).next(".hidebtn-group").height(height);
            $(this).parent("div").siblings("div").find("ul").trigger("swipeRight");
            $(this).css({"transform":"translateX(-"+ move +"px)","-webkit-transform":"translateX(-"+ move +"px)"});
            $(this).next(".hidebtn-group").css({"transform":"translateX(-"+ move +"px)","-webkit-transform":"translateX(-"+ move +"px)"});
            $(this).parent("div").addClass("active");
          }
        },
        swipeRight:function(event, direction, distance, duration, fingerCount) {
          if($(this).parent("div").hasClass("active"))
          {
            $(this).css({"transform":"translateX(0)","-webkit-transform":"translateX(0)"});
            $(this).next(".hidebtn-group").css({"transform":"translateX(0)","-webkit-transform":"translateX(0)"});
            $(this).parent("div").removeClass("active");
          }
        },
        //Default is 75px, set to 0 for demo so any distance triggers swipe
        threshold:0
  });

  /*$(".addresslists").on('swipeUp',function(){
		var dis =$(this).scrollTop();
		$(this).scrollTo({toT:dis+100});
	});
	$(".addresslists").on('swipeDown',function(){
		var dis =$(this).scrollTop();
		$(this).scrollTo({toT:dis-+100});
	});*/
  //document.addEventListener('touchmove', function (event) {
    //event.preventDefault();
  //}, false);

});

//spinner +-数量
$.fn.removeSpinner = function(opts){
  return this.each(function () {
    var textField = $(this);
    textField.unbind("spinner");
    textField.siblings().remove();
    textField.unwrap();
  });
};

$.fn.spinner = function (opts) {
  return this.each(function () {
    var defaults = {value:0, min:0, max:9999};
    var options = $.extend(defaults, opts);
    var textField = $(this);

    textField.attr("readOnly","readOnly");
    if (options.max>0) {
      $.extend(options, {min:1});
    }
    var keyCodes = {up:38, down:40};
    var container = $('<div></div>');
    container.addClass('spinner');
    var value = textField.val();
    textField.attr('maxlength', '2').val(value ? value : options.value)
      .bind('keyup paste change', function (e) {
        var field = $(this);
        if (e.keyCode == keyCodes.up) changeValue(1);
        else if (e.keyCode == keyCodes.down) changeValue(-1);
        else if (getValue(field) != container.data('lastValidValue')) validateAndTrigger(field);
      });
    textField.wrap(container);

    var increaseButton = $('<button class="increase icon-add" type="button"></button>').click(function () { changeValue(1) });
    var decreaseButton = $('<button class="decrease icon-reduce" type="button"></button>').click(function () { changeValue(-1) });


    if (options.max>0) {
      container.data('lastValidValue', 1);
    }else{
      container.data('lastValidValue', options.value);
    }
    validate(textField);
    textField.before(decreaseButton);
    textField.after(increaseButton);

    function changeValue(delta) {
      textField.val(getValue() + delta);
      validateAndTrigger(textField);
    }

    function validateAndTrigger(field) {
      clearTimeout(container.data('timeout'));
      var value = validate(field);
      if (!isInvalid(value)) {
        textField.trigger('update', [field, value]);
      }
    }

    function validate(field) {
      var value = getValue();
      if (value <= options.min) decreaseButton.attr('disabled', 'disabled');
      else decreaseButton.removeAttr('disabled');
      if (value >= options.max) increaseButton.attr('disabled', 'disabled');
      else increaseButton.removeAttr('disabled');

      field.toggleClass('passive', value === 0);

      if (isInvalid(value)) {
        var timeout = setTimeout(function () {
          textField.val(container.data('lastValidValue'));
          validate(field);
        }, 200);
        container.data('timeout', timeout);
      } else {
        container.data('lastValidValue', value);
      }
      return value;
    }

    function isInvalid(value) { return isNaN(+value) || value < options.min || value > options.max; }

    function getValue(field) {
      field = field || textField;
      return parseInt(field.val() || 0, 10)
    }
  })
}
$.fn.navfix=function(mtop,zindex){var nav=$(this),mtop=mtop,zindex=zindex,dftop=nav.offset().top-$(window).scrollTop(),dfleft=nav.offset().left-$(window).scrollLeft(),dfcss=new Array;dfcss[0]=nav.css("position"),dfcss[1]=nav.css("top"),dfcss[2]=nav.css("left"),dfcss[3]=nav.css("zindex"),$(window).scroll(function(e){$(this).scrollTop()>dftop?$.browser.msie&&$.browser.version=="6.0"?nav.css({position:"absolute",top:eval(document.documentElement.scrollTop),left:dfleft,"z-index":zindex}):nav.css({position:"fixed",top:mtop+"px",left:dfleft,"z-index":zindex}):nav.css({position:dfcss[0],top:dfcss[1],left:dfcss[2],"z-index":dfcss[3]})})}
