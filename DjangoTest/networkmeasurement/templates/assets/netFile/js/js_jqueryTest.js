$(document).ready(function(){
	$("p").click(function(){
		$(this).hide();
	});
	$("h1").click(function(){
		$(this).hide();
	});
	//dblclick:double click
	$("div#p_h1").dblclick(function(){
		$(this).hide();
	});

	$("button#pHideBtn").click(function(){
		$("p").hide("slow");
	});
	//test slideup   slideToggle
	$("div#p_slideup").click(function(){
		//$("div#div_slideup").slideUp("slow",display);
		$("div#div_slideup").slideToggle("slow",display);
	});
	$("div input#input_focus").focus(function(){
		//alert("focus");  //happen when getting focus
		$(this).val("You have get focused");
	});

	//test fadeIn
	$("button#button_fadeIn").dblclick(function(){
		$("p").fadeIn("slow");
	});

	//test animate func
	$("button#button_animate").click(function(){
		//$("div#div_animate").animate({left:'100px',fontSize:'3em'},"slow");
		var div_animate = $("div#div_animate")
		div_animate.animate({left:'100px'},"slow");
		div_animate.animate({fontSize:'3em'},"slow");
	});

	$("#button_attr").click(function(){
		alert("attr: href="+$("#herf_baidu").attr("href")+";id="+$("#herf_baidu").attr("id"));
	});
	$("#button_html").click(function(){
		alert("html:"+$("#herf_baidu").html());
		//using callback func to change button text aslo with attr() and html()
		$(this).text(function(i,oldText){
			return oldText+" New";
		});
	});
	$("#button_addcss").click(function(){
		$("p").addClass("important blue")
	})

	$("#button_createDiv").click(function(){
		$("#div_hide").html(" \
			<p><b>This is div created by button</b></p> \
			<h1 id=\"xxx\">This is h1 created by button</h1>");
	});
	$("#button_ajax").click(function(){
		getDataByAjax();
	});
});

function display(){
	alert("You have finished!");
}

function getDataByAjax(){
	$.ajax({
		url:"/test/operateDB",
		//url:"assets/netFile/css/css_jqueryTest.css",
		data:{
			liaohui: "liaohui"
		},
		type:'post', //it will wrong in Djaong if type:POST
		dataType:'json',
		success:function(data){
			var jsonData = eval(data);
			var alertMsg = "Data from mysql with json\n";
			$(jsonData).each(function(index){
				var tempData = jsonData[index];
				alertMsg += "id:"+tempData.id+";";
				alertMsg += "name:"+tempData.name+";";
				alertMsg += "\n";

				$("#div_mysql").append("<div id=div_mysql_children"+index+"></div>");
				$("#div_mysql_children"+index).html("<p>id="+tempData.id+"</p>"+"<p>name="+tempData.name+"</p>");
			})
			alert("ajax json success!\n"+alertMsg);//
		},
		error:function(xhr,type){
			alert("ajax json error!")//
		}
	});
}
