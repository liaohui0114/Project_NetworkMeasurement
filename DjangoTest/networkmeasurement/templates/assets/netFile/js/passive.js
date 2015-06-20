$(document).ready(function(){

	$("#id_startNode").addClass("form-control");
	$("#id_endNode").addClass("form-control");
	SetDate();   //bind to datepicker controler

	//$("#id_btn_single").on("dblclick",function(){
	//start single test
	$("#id_btn_passive").on("click",function(){
		var st =  $("#id_input_startTime").val();
		var et = $("#id_input_endTime").val();
		//format time: like 2015-06-16 11:11:11 and make startTime<=endTime
		if(st <= et)
		{
			st = st + " 00:00:00"
			et = et + " 23:59:59"
		}
		else
		{
			var tmp = st;
			st = et;
			et = tmp;
			st = st + " 00:00:00"
			et = et + " 23:59:59"
		}
		//alert(st+'\n'+et);
		Udp_ajax_post_passive($("#id_startNode").val(),$("#id_endNode").val(),$("#id_startNode option:selected").text(),$("#id_endNode option:selected").text(),st,et);		

		
	});
	
})

//protocol: protocol type;1.TCP;2.UDP;3.ICMP;
//startIp:ip of startNode
//endIp:ip of endNode
//startNodeName:name of start node
//endNodeName:name of end node
function Udp_ajax_post_passive(startIp,endIp,startNodeName,endNodeName,startTime,endTime)
{
	alert("Udp_ajax_post_passive!\n");

	
	$.ajax({
		url:"/action/PassiveAction",
		//async: false, //if we want to lock the screen
		data:{
			"startNodeIp":startIp,
			"endNodeIp":endIp,
			"startNodeName":startNodeName,
			"endNodeName":endNodeName,
			"startTime":startTime,
			"endTime":endTime
		},
		type:'POST',//action:post or get
		dataType:'json',
		beforeSend:function(){
			//alert("beforeSend!");
			showCover(); //在数据发送前，显示遮罩層，锁定屏幕
		},
		success:function(data){
			
			alert("success!\n");

			$("#ChartDisplayID").show();//show table of single table
			var createTime;
			$.each(data,function(i,item){
				if(i == "time")
				{
					createTime = eval(item);  //to get createTime infos
				}					
			});

			//x = eval(data); decode json type
			$.each(data,function(i,item){

				//i is key and item is value
			
				//alert("i:"+i+";item:"+item);
				//alert(data[i].bandwidth); //data.i.bandwidth is wrong
				if(i != "time")
				{
					var unit = ""
					switch(i)
					{
						case 'bandwidth':
							unit = '(Mps)';
							break;

						case 'throughput':
							unit = '(Mps)';
							break;

						case 'loss':
							unit = '(%)';
							break;

						case 'rtt':
							unit = '(%)';
							break;

						case 'cpu':
							unit = '(%)';
							break;

						case 'memory':
							unit = '(%)';
							break;

						default:
							break;
					}
						//data that we get from json is type string,so we can't get trully data. we need to convert to type object?
						//eval() can change json string to object type, otherwise you need to parse/decode by yourself using for ..... for ... to get type:int,str,date etc.
						var chartData = eval(item); //it's important that we must use 'eval()',why???  check up eval().It is said to avoid using eval() in Interne
						var chartId = '#id_div_chart_'+i;
						var chartTitle = i;
						DisplayActiveChart(chartId,chartTitle,chartData,createTime,startTime,endTime,unit); // using plug-in:Highcharts  to display charts;
				}
				else
				{
					//alert("i==time,date:"+new Date());
				}
				
				
								
			});

			hideCover(); //在成功收到数据，隐藏遮罩層，解锁屏幕
				
		},
		error:function(xhr,type){
			hideCover();//失败后，隐藏遮罩層，解锁屏幕
			alert("fail!");
		}
	});

}


/*
chartId:to get element by $(chartId)
chartTitle:bandwidth,throughput,cpu etc.
chartData:data for chart
createTime: createTime of every point
unit:Mps mps ,% or others
*/
function DisplayActiveChart(chartId,chartTitle,chartData,createTime,startTime,endTime,unit){

	 $(chartId).highcharts({
	 	chart: {
          type: 'spline'
      },
        title: {
            text: 'Result of Network Condition by Passive Test:'+chartTitle,
            x: -20 //center
        },
        subtitle: {
            text: 'subtitle: Passive Network Condition between '+startTime+' and '+endTime,
            x: -20
        },
        
        xAxis: {
            categories: [],  // to show xAxis
            title:
            {
            	text:'Index'
            }
        },
        yAxis: {
            title: {
                text: chartTitle+unit
            },
            plotLines: [{
                value: 0,
                width: 1,
                color: '#808080'
            }]
        },
        tooltip: {
            //valueSuffix: unit #defualut
            //added by liaohui
            //define format output
            formatter: function() {
                return '<b>'+ this.series.name +':</b>'+ this.y+unit
                +'<br><b>time:</b>'+(new Date(createTime[this.x]*1000).Format("yyyy-MM-dd hh:mm:ss"));
                //timestamp to CST in jquery,we need to *1000

            }
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle',
            borderWidth: 0
        },
        series: chartData  // the data which chart truely need,type []
    });
}


//show div: #id_div_cover；添加遮罩层（该元素弹出在并在最前端显示）
function showCover()
{
	var docHeight = $(document).height(); //获取窗口高度
	//var docWidth = $(document).width();
			  
	$('#id_div_cover')
	.height(docHeight)
	.css({
	  'opacity': .9, //透明度
	  'position': 'absolute',
	  'top': 0,
	  'left': 0,
	  'background-color': 'black',
	  'width': '100%',
	  'z-index': 5000 //保证这个悬浮层位于其它内容之上
	});
	$('#id_img_cover').css({
	  'opacity': .9, //透明度
	  'position': 'absolute',
	  'top': 200,  //from top
	  'left': 300,  //from left
	  'background-color': 'black',
	});

	$('#id_div_cover').show();   //show the div


}
//hide div: #id_div_cover
function hideCover()
{				    
	setTimeout(function(){$('#id_div_cover').fadeOut('slow')}, 1000); //设置1秒后覆盖层自动淡出
}



/////////copy from internet to formate Date() like "yyyy-MM-dd hh:mm:ss"
Date.prototype.Format = function (fmt) { //author: meizz 
    var o = {
        "M+": this.getMonth() + 1, //月份 
        "d+": this.getDate(), //日 
        "h+": this.getHours(), //小时 
        "m+": this.getMinutes(), //分 
        "s+": this.getSeconds(), //秒 
        "q+": Math.floor((this.getMonth() + 3) / 3), //季度 
        "S": this.getMilliseconds() //毫秒 
    };
    if (/(y+)/.test(fmt)) fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
    for (var k in o)
    if (new RegExp("(" + k + ")").test(fmt)) fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
    return fmt;
}
///////////end format/////////////////////////

//use datepicker to get datetime
function SetDate()
{
	var d = new Date();
	//ct = d.Format("yyyy-MM-dd hh:mm:ss")
	ct = d.Format("yyyy-MM-dd");
	//alert(ct);
	$("#id_input_startTime").val(ct);
	$("#id_input_endTime").val(ct);

	$("#id_input_startTime").datepicker({//添加日期选择功能  
            numberOfMonths:1,//显示几个月  
            dateFormat: 'yy-mm-dd',//日期格式 

            showButtonPanel:true,//是否显示按钮面板  
            clearText:"清除",//清除日期的按钮名称  
            closeText:"关闭",//关闭选择框的按钮名称 
            maxDate: new Date(),
            yearSuffix: '年', //年的后缀  
            showMonthAfterYear:true,//是否把月放在年的后面  
            monthNames: ['一月','二月','三月','四月','五月','六月','七月','八月','九月','十月','十一月','十二月'],  
            dayNames: ['星期日','星期一','星期二','星期三','星期四','星期五','星期六'],  
            dayNamesShort: ['周日','周一','周二','周三','周四','周五','周六'],  
            dayNamesMin: ['日','一','二','三','四','五','六'],
            
              
            });

	$("#id_input_endTime").datepicker({//添加日期选择功能  
            numberOfMonths:1,//显示几个月  
            dateFormat: 'yy-mm-dd',//日期格式 

            showButtonPanel:true,//是否显示按钮面板  
            clearText:"清除",//清除日期的按钮名称  
            closeText:"关闭",//关闭选择框的按钮名称  
            
            maxDate: new Date(),
            //changeMonth:true,
            //changeYear:true,
            yearSuffix: '年', //年的后缀  
            showMonthAfterYear:true,//是否把月放在年的后面  
            monthNames: ['一月','二月','三月','四月','五月','六月','七月','八月','九月','十月','十一月','十二月'],  
            dayNames: ['星期日','星期一','星期二','星期三','星期四','星期五','星期六'],  
            dayNamesShort: ['周日','周一','周二','周三','周四','周五','周六'],  
            dayNamesMin: ['日','一','二','三','四','五','六']
              
            });
}
