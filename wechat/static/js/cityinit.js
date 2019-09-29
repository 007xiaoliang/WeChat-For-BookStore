/**======================================
省市区三级联动
======================================**/
$(function(){
$.fn.cityChoose=function(settings){
  var json;
  if(this.length<1){return;};
  // 默认值
  settings=$.extend({
    url:"http://static.tcxy.com.cn/admin/js/city.min.js",//url:省市数据josn文件路径
    prov:null,  //prov:默认省份
    city:null,  //city:默认城市
    dist:null,  //dist:默认地区（县
    nodata:null,//nodata:无数据状态
    required:true
  },settings);

  var box_obj=this;
  var prov_obj=$(".prov");
  var city_obj=$(".city");
  var dist_obj=$(".dist");
  var prov_val=settings.prov;
  var city_val=settings.city;
  var dist_val=settings.dist;
  var city_json;
  var temp_html=""

  // 赋值市级函数
  var cityStart=function(e){
    temp_html="";
    var prov_id = e.index();
    console.log(prov_id);

    if(prov_id<0||typeof(city_json.citylist[prov_id].c)=="undefined"){
      if(settings.nodata=="none"){
        city_obj.css("display","none");
        dist_obj.css("display","none");
      }else if(settings.nodata=="hidden"){
        city_obj.css("visibility","hidden");
        dist_obj.css("visibility","hidden");
      };
      return;
    };

    // 遍历赋值市级下拉列表
    $.each(city_json.citylist[prov_id].c,function(i,city){
      if(city.n == city_val){
        temp_html+="<li class='active'>"+city.n+"</li>";
      }else{
        temp_html+="<li>"+city.n+"</li>";
      }

    });
    city_obj.html(temp_html).css({"display":"","visibility":""});

    city_obj.find("li").each(function(){
      if($(this).hasClass("active"))
      {
        distStart($(this));
        $(this).siblings().hide();
      }
    })
    // 选择市级时发生事件
    city_obj.find("li").on("click",function(){
      if($(this).hasClass("active"))
      {
        dist_obj.css("display","none");
        $(this).removeClass("active");
        $(this).siblings().show();
      }else{
        $(this).addClass("active");
        $(this).siblings().hide().removeClass("active");
        distStart($(this));
      }
    });
  };

  // 赋值地区（县）函数
  var distStart=function(e){
    temp_html="";
    var prov_id = "";
    var prov_text=""
    prov_obj.find("li").each(function(index,ele){
      if($(this).hasClass("active"))
      {
        prov_id = index;
        prov_text = ele.innerHTML;
      }
    })
    var city_id = e.index();
    var city_text = e[0].innerHTML;
    if(prov_id<0||city_id<0||typeof(city_json.citylist[prov_id].c[city_id].a)=="undefined"){
      if(settings.nodata=="none"){
        dist_obj.css("display","none");
        box_obj.html("<span>"+prov_text+"</span><span>"+city_text+"</span>");
        box_obj.siblings("input").val("");
        $("[name=province]").val(prov_text);
        $("[name=city]").val(city_text);
        $(".citylist").hide();
      }else if(settings.nodata=="hidden"){
        dist_obj.css("visibility","hidden");
      };
      return;
    };
    // 遍历赋值市级下拉列表
    $.each(city_json.citylist[prov_id].c[city_id].a,function(i,dist){
      if(dist.s == dist_val){
        box_obj.html("<span>"+prov_text+"</span><span>"+city_text+"</span><span>"+dist_val+"</span>");
        $("[name=province]").val(prov_text);
        $("[name=city]").val(city_text);
        $("[name=district]").val(dist_val);
      }
      temp_html+="<li>"+dist.s+"</li>";
    });
    dist_obj.html(temp_html).css({"display":"","visibility":""});
    dist_obj.find("li").on("click",function(){
      box_obj.html("<span>"+prov_text+"</span><span>"+city_text+"</span><span>"+this.innerHTML+"</span>")
      box_obj.siblings("input").val("");
      $("[name=province]").val(prov_text);
      $("[name=city]").val(city_text);
      $("[name=district]").val(this.innerHTML);
      $(".citylist").hide();
    })

  };

  var init=function(){
    // 遍历赋值省份下拉列表
    $.each(city_json.citylist,function(i,prov){
      if(prov.p == prov_val){
        temp_html+="<li class='active'>"+prov.p+"</li>";
      }else{
        temp_html+="<li>"+prov.p+"</li>";
      }
    });
    prov_obj.html(temp_html);

    // 选择省份时发生事件
    prov_obj.find("li").on("click",function(){
      if($(this).hasClass("active"))
      {
        $(this).removeClass("active");
        $(this).siblings().show();
        city_obj.find("li").hide();
        dist_obj.find("li").hide();
      }else{
        $(this).addClass("active");
        $(this).siblings().hide().removeClass("active");
        cityStart($(this));
      }
    });

    prov_obj.find("li").each(function(){
      if($(this).hasClass("active"))
      {
        cityStart($(this));
        $(this).siblings().hide();
      }
    })
  };

  // 设置省市json数据
  if(typeof(settings.url)=="string"){
    $.getJSON("http://static.tcxy.com.cn/admin/js/city.min.js",function(json){
      city_json=json;
      init();
    });
  }else{
    city_json = settings.url;
    init();
  };
};
});
