var mySwiper = new Swiper('.swiper-container', { //首页焦点图
	autoplay: 5000,//可选选项，自动滑动
	pagination : '.swiper-pagination',
	paginationClickable:true,
});
var code = {
	close:function(id) {// 取消蒙版
		if(id) {
			$(".mask").css({"display":"none"});
			$("body").css({"overflow":"visible"});
		}
	},
	open:function(id) {// 打开蒙版
		if($(id).parent().hasClass("delete")) {
			var length = $(".collection .icon i.active").length;
			console.log(length);
			if(length<=0) {
				return false;
			}
		}
		if(id) {
			$(".mask").css({"display":"block"});
			$("body").css({"overflow":"hidden"});
			$(".main-info").scrollTop(0);
		}
	}
}
$(".main-info>div").on("click","div",function(e) {// 商品详情页 条件切换
	e.preventDefault();
	$(this).addClass("active").siblings().removeClass("active");
})
$(".mask>div").on("click",function(e) { //阻止因为蒙版层关闭的冒泡
	e.stopPropagation();
	return false;
});
$(".collection .icon i,.delete i:eq(0)").on("touchstart",function() {// 选择按钮功能
	if($(this).data("all") =="ok") {
		$(".collection .icon i").addClass("active");
		$(this).data("all","true"); 
	} else {
		if($(this).data("all")) {
			$(".collection .icon i").removeClass("active");
			$(this).data("all","ok");
		}
	}
	if($(this).hasClass("active")) {
		$(this).removeClass("active");
		$(".delete i:eq(0)").removeClass("active").data("all","ok");
	} else {
		$(this).addClass("active");
	}
	var lengthT= $(".collection .icon i").length;
	var length = $(".collection .icon i.active").length;
	if(length == lengthT) {
		$(".delete i:eq(0)").addClass("active");
		$(".delete i:eq(0)").data("all","true"); 
	}
});
$(".main-number i").on("touchstart",function() {// 商品数量计算 通过数量对价格以及数量实时展示
	var num = $(this).siblings("input").val();
	var str = $(this).parent().prev().children("strong").html().substring(1);
	if($(this).data("number") == "up") {
		num ++;
		var money = num * str;
		$(this).siblings("input").val(num).attr("data-money",money);
	} else {
		num --;
		var money = (parseInt($(this).siblings("input").attr("data-money")))- str;
		if(num <= 1) {
			num = 1;
			money = str;
		}
		$(this).siblings("input").attr("data-money",money);
		$(this).siblings("input").val(num);
	}
	if($(this).parent().data("show") == "number") {
		allMoney();
	}
});
function allMoney() { // 购物车  底部总价格与数量 
	var num =0,all_money = 0;
	$(".main-number input").each(function() {
		num += parseInt($(this).val());
		var code = parseInt($(this).attr("data-money"));
		all_money += code;
	});
	all_money = "¥" + all_money;
	$("#all_number").html(num);
	$("#all_money").html(all_money);
}
allMoney();
function translate3d(id,key) {
	var pagex;
	var width = parseInt($(id).width() / 5);
	var widthT = parseInt($(id).width() / 5) *2;
	$(id).on('touchstart',function(e) {// 记录滑屏起点
		if($(this).data("key") == "no") {
			return false;
		}
		var touch = e.originalEvent.targetTouches[0];
		pagex = touch.pageX;
		$(this).css({"transitionDuration":0});
	});
	$(id).on('touchmove',function(e) {// 计算滑屏的数值 ，然后赋值给动画
		if($(this).data("key") == "no") {
			return false;
		}
		var touch = e.originalEvent.targetTouches[0];
		var num =  parseInt((pagex - touch.pageX) * 2);
		var length = -num;
		key = $(this).data("key");

		if(num >= 50) {
			length = -width;
			if(key == "edit") {
				length = -widthT;
			}
			setTimeout(function(){
				$(this).next().css({"zIndex":"5"});
			},300);
		} else if (num <= 0) {
			length = 0;
			setTimeout(function() {
				$(this).next().css({"zIndex":0});
			},300);
		}
		length = length + "px";
		var code = 'translate3d('+ length +',0,0)';
		$(this).stop().css({"transform":code,"transitionDuration":"300ms"});
	});
	$(id).on("touchend",function(e) {
		if($(this).data("key") == "no") {
			return false;
		}
		var touch = e.originalEvent.changedTouches[0];
		var outX = touch.pageX;
		var length;
		if(pagex - outX < 40) {
			length = 0;
			length = length + "px";
			var code = 'translate3d('+ length +',0,0)';
			$(this).stop().css({"transform":code,"transitionDuration":"300ms"});
		}
	});
}
translate3d(".view-box");
$(".btns-box .btns a").on("touchstart",function(e) { // 打开蒙版层
	e.preventDefault();
	$(".mask").css({"display":"block"});
});
(function() {  //通过计算高度 设置子元素垂直居中
	$(".btns-box a").css({"lineHeight":parseInt($(".btns-box .btns").height()) + "px"});
})();

$("body").on("touchmove",function(e) { //  禁止冒泡设置
	e.preventDefault();
});
$(".screen-box").on('touchstart',function(e) {
	e.preventDefault();
	$(this).addClass("active");
	$(".screen-box ul").slideToggle(100);
});
$(".screen-box ul").on("touchstart","li",function(e) {
	var _self = $(this);
	var text = $(this).html();
	var code = $(this).parent().parent().children("span").html();
	var html = "<li>"+code+"</li>";
	$(this).addClass("active").siblings().removeClass("active");
	$(this).parent().parent().children("span").html(text);
	$(this).parent().slideToggle(100,function() {
		$(this).parent().removeClass("active");
	});
	e.stopPropagation();
})

//产品分类设置显示区域高度
function setHight(type){
    var windowH=$(window).height()
    var productH=windowH-$('.head').height()-$('.footr-nav').height()-$('.search').height()-34;
    var orderH=windowH-$('.head').height()-$('.footr-nav').height()-50;
//    alert(productH)
    if(type=='product'){
        $('.h1').height(productH)
    }
    if(type=='order'){
        $('.h1').height(orderH)
    }
}
//产品分类页面tab功能
//点击后执行ajax获取数据后通过append()在右边进行添加
$('.tab-box .left-tab ul li').click(function(){
	
//	数据获取完后执行显示当前点击的tab,隐藏其他窗口
	$('.tab-box .right-tab-cont ul').eq($(this).index()).show().siblings().hide()
	
})