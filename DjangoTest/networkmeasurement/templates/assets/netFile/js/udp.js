$(document).ready(function(){

	$("#id_startNode").addClass("form-control");
	$("#id_endNode").addClass("form-control");

	//$("#id_btn_single").on("dblclick",function(){
	//start single test
	$("#id_btn_single").on("click",function(){
		Udp_ajax_post_single("udp",$("#id_startNode").val(),$("#id_endNode").val(),$("#id_startNode option:selected").text(),$("#id_endNode option:selected").text());		

		$("#NodeDisplayID").show();//show table of single table
		DisplayNodePath();//draw path diagram
		$("#PathDisplayID").show();
		$("#OverallDisplayID").hide(); //show tables of overall network testing
	});
	//start overall test
	$("#id_btn_overall").click(function(){
		Udp_ajax_post_overall("udp");
		$("#NodeDisplayID").hide();
		$("#PathDisplayID").hide();
		$("#OverallDisplayID").show();
	});

	SetDate();
})

//protocol: protocol type;1.TCP;2.UDP;3.ICMP;
//startIp:ip of startNode
//endIp:ip of endNode
//startNodeName:name of start node
//endNodeName:name of end node
function Udp_ajax_post_single(protocol,startIp,endIp,startNodeName,endNodeName)
{
	alert("Udp_ajax_post_single!\n");
	$.ajax({
		url:"/action/SingleAction",
		//async: false, //if we want to lock the screen
		data:{
			"startNodeIp":startIp,
			"endNodeIp":endIp,
			"startNodeName":startNodeName,
			"endNodeName":endNodeName,
			"protocol":protocol,
			//form:$("#id_form_node").serialize()  //using & to connetion,style:startNode=192.168.1.152&endNode=192.168.1.152
		},
		type:'POST',//action:post or get
		dataType:'json',
		beforeSend:function(){
			//alert("beforeSend!");
			showCover(); //在数据发送前，显示遮罩層，锁定屏幕
		},
		success:function(data){
			hideCover(); //在成功收到数据，隐藏遮罩層，解锁屏幕
			alert("success!\n");
			//x = eval(data); decode json type
			var chartData,chartTime;
			$.each(data,function(i,item){
				//i is key and item is value
				
				//alert("i:"+i+";item:"+item);
				//alert(data[i].bandwidth); //data.i.bandwidth is wrong
				if("single" == i) //to get table data
				{
					$.each(item,function(key,value){
					//alert("key:"+key+";value:"+value);
					//alert("#id_table_"+i+"_"+key);
					$("#id_table_single_endNode").text($("#id_endNode option:selected").text());
					$("#id_table_single_endNodeIp").text(endIp);
					$("#id_table_"+i+"_"+key).text(value);  //we have set id of <td> and <th>,so we can alter its text
					});
				}
				else if("chart" == i)
				{
					//data that we get from json is type string,so we can't get trully data. we need to convert to type object?
					//eval() can change json string to object type, otherwise you need to parse/decode by yourself using for ..... for ... to get type:int,str,date etc.
					chartData = eval(item.chartData); //it's important that we must use 'eval()',why???  check up eval().It is said to avoid using eval() in Internet
					//chartTime = eval(item["chartTime"]);  //we can use both two type:item.xxx,item["xxx"]
					//chartTime = eval("[1,3,5,7,9,11,13,15,17,19]");//eval("[1,3,5,7,9,11,13,15,17,19]") which will change str to [1,3,5,7,9,11,13,15,17,19]
					
					chartTime = $.parseJSON('['+item["chartTime"]+']');
					//alert(chartData[1].data); 
					

					
				}				
			});

			DisplayActiveChart(chartData,chartTime); // using plug-in:Highcharts  to display charts;
				

			//to display charts
			// var chartData = [{
   //          'name': 'Tokyo',
   //          'data': [7.0, 6.9, 9.5, 14.5, 18.2, 21.5, 25.2, 26.5, 23.3, 18.3, 13.9, 9.6]
   //      }, {
   //          'name': 'New York',
   //          'data': [-0.2, 0.8, 5.7, 11.3, 17.0, 22.0, 24.8, 24.1, 20.1, 14.1, 8.6, 2.5]
   //      }, {
   //          'name': 'Berlin',
   //          'data': [-0.9, 0.6, 3.5, 8.4, 13.5, 17.0, 18.6, 17.9, 14.3, 9.0, 3.9, 1.0]
   //      }, {
   //          'name': 'London',
   //          'data': [3.9, 4.2, 5.7, 8.5, 11.9, 15.2, 17.0, 16.6, 14.2, 10.3, 6.6, 4.8]
   //      }];
			// //DisplayActiveChart(chartData); // to display chart,it's good

		},
		error:function(xhr,type){
			hideCover();//失败后，隐藏遮罩層，解锁屏幕
			alert("fail!");
		}
	});
}

//overall test
function Udp_ajax_post_overall(protocol)
{
	alert("Udp_ajax_post_overall!\n");
	$.ajax({
		url:"/action/OverallAction",
		data:{
			"protocol":protocol,//TCP;UDP;ICMP
			//form:$("#id_form_node").serialize()  //using & to connetion,style:startNode=192.168.1.152&endNode=192.168.1.152
		},
		type:'POST',
		dataType:'json',
		beforeSend:function(){
			//alert("beforeSend!");
			showCover();
		},
		success:function(data){
			hideCover();
			alert("success!!!!\n");
			// $.each(data,function(i,item){
			// 	//i is key and item is value

			// 	alert("i:"+i+";item:"+item);
			// 	//alert(data[i].bandwidth); //data.i.bandwidth is wrong
			// 	$.each(item,function(key,value){
			// 		//alert("key:"+key+";value:"+value);
			// 		//alert("#id_table_"+i+"_"+key);
			// 		$("#id_table_single_endNode").text($("#id_endNode option:selected").text());
			// 		$("#id_table_single_endNodeIp").text(endIp);
			// 		$("#id_table_"+i+"_"+key).text(value);  //we have set id of <td> and <th>,so we can alter its text
			// 	});
				
			// });
			$.each(data,function(conditon,startData){
				//clear table because every time it will add child element to the table when clicking btn
				$("#id_table_"+conditon).find('thead').find('tr').empty();
				$("#id_table_"+conditon).find('tbody').find('tr').empty();

				$("#id_table_"+conditon).find('thead').find('tr').append("<th>"+conditon+"</th>");
				var isFirst = true;  // to avoid $("#id_table_"+conditon).find('thead').find('tr').append("<th>"+end+"</th>"); running every <th>
				$.each(startData,function(start,endData){
					var thTmp = "<th>"+start+"</th>";
					
					$.each(endData,function(end,value){

						if(isFirst)
						{
							$("#id_table_"+conditon).find('thead').find('tr').append("<th>"+end+"</th>");
						}					
						
						//$("#id_table_"+conditon).find('tbody').append("<tr><td>"+value+"</td></tr>");
						thTmp += "<td>"+value+"</td>"
						//$("#id_table_"+conditon+" tbody tr").append("<td>"+value+"</td>");
					});
					isFirst = false;
					$("#id_table_"+conditon).find('tbody').append("<tr>"+thTmp+"</tr>");
				});

			});

		},
		error:function(xhr,type){
			hideCover();
			alert("fail!");
			$("#OverallDisplayID").hide();
		}
	});
}

//to display chart of bandwidth 
function DisplayActiveChart(chartData,chartTime){
	// var chart = new Highcharts.Chart({
	// 	chart:{
 //            renderTo:'id_div_activeChart',
 //            //type:'column' //显示类型 柱形
 //        },
	// 	title: {
 //            text: 'Monthly Average Temperature',
 //            x: -20 //center
 //        },
 //        subtitle: {
 //            text: 'subtitle: liaohui:highcharts test!',
 //            x: -20
 //        },
 //        xAxis: {
 //            categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun','Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
 //        },
 //        yAxis: {
 //            title: {
 //                text: 'Temperature (°C)'
 //            },
 //            plotLines: [{
 //                value: 0,
 //                width: 1,
 //                color: '#808080'
 //            }]
 //        },
 //        tooltip: {
 //            valueSuffix: '°C'
 //        },
 //        legend: {
 //            layout: 'vertical',
 //            align: 'right',
 //            verticalAlign: 'middle',
 //            borderWidth: 0
 //        },
 //        series: [{name:'aaa',data:[]}]

	// 	});
	// 	chart.series[0].setData(chartData[0].data);//数据填充到highcharts上面
	// 	chart.series[0].name = chartData[0].name;//数据填充到highcharts上面

	//#id_div_activeChart: the div to show chart
	 $('#id_div_activeChart').highcharts({
        title: {
            text: 'Bandwidth Condition of the lastest 10 times',
            x: -20 //center
        },
        subtitle: {
            text: 'subtitle: liaohui:highcharts test!',
            x: -20
        },
        xAxis: {
            categories: chartTime  // to show xAxis
        },
        yAxis: {
            title: {
                text: 'Bandwidth (Mbps)'
            },
            plotLines: [{
                value: 0,
                width: 1,
                color: '#808080'
            }]
        },
        tooltip: {
            valueSuffix: 'Mp/s'
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

function DisplayNodePath()
{
	//alert("DisplayNodePath");
	var radius = 15;
	var offet = 40;
	var nodedic = {"nodeA":{"x":50+offet,"y":100+offet},
					"nodeB":{"x":150+offet,"y":100+offet},
					"nodeC":{"x":250+offet,"y":100+offet},
					"nodeD":{"x":100+offet,"y":200+offet},
					"nodeE":{"x":200+offet,"y":200+offet},
					"nodeF":{"x":300+offet,"y":200+offet}};

	///////init  draw pic/////////
	/////clear canvas///////
	var can = document.getElementById('id_canvas_router');
	var clearNode = can.getContext('2d');
	clearNode.fillStyle = "black";
	clearNode.strokeStyle = "black";
	clearNode.lineWidth = 1;
	clearNode.clearRect(0,0,1024,400);
	
	////////end clear canvas///////////
	//alert("pathDisplay2 after clear");
	var node = can.getContext('2d');
	var nodeText = can.getContext('2d');
	nodeText.font = "10px Arial";
	
	var imgWidth = 60; //width 60px
	for (var key in nodedic)
	{
	var img = document.getElementById("id_img_router");
	node.drawImage(img,nodedic[key].x,nodedic[key].y,imgWidth,imgWidth);
		nodeText.fillText(key,nodedic[key].x+10,nodedic[key].y+10);
	}
	//default line: nodeA-nodeB-nodeC,nodeA-nodeD-nodeE-nodeF
	//alert("after for");
	var cxt = can.getContext('2d');
	//cxt.moveTo(0,0);
	//cxt.lineTo(nodedic.nodeA.x-radius,nodedic.nodeA.y-radius);
	cxt.beginPath();
	cxt.moveTo(nodedic.nodeA.x+imgWidth,nodedic.nodeA.y+imgWidth/2);
	cxt.lineTo(nodedic.nodeB.x,nodedic.nodeB.y+imgWidth/2);
	cxt.moveTo(nodedic.nodeB.x+imgWidth,nodedic.nodeB.y+imgWidth/2);
	cxt.lineTo(nodedic.nodeC.x,nodedic.nodeC.y+imgWidth/2);
	
	cxt.moveTo(nodedic.nodeA.x+imgWidth/2,nodedic.nodeA.y+imgWidth);
	cxt.lineTo(nodedic.nodeD.x,nodedic.nodeD.y);
	cxt.moveTo(nodedic.nodeD.x+imgWidth,nodedic.nodeD.y+imgWidth/2);
	cxt.lineTo(nodedic.nodeE.x,nodedic.nodeE.y+imgWidth/2);
	cxt.moveTo(nodedic.nodeE.x+imgWidth,nodedic.nodeE.y+imgWidth/2);
	cxt.lineTo(nodedic.nodeF.x,nodedic.nodeF.y+imgWidth/2);
	cxt.closePath();
	cxt.stroke();
	
	////////end init////////////////
	
	
	var nodeArray = new Array("nodeA","nodeB","nodeF","nodeG");
	var nodeCircle = document.getElementById("id_canvas_router").getContext('2d');
	var nodeLine = document.getElementById("id_canvas_router").getContext('2d');
	var img = document.getElementById("id_img_router");
	var lineX = 0;
	var lineY = 0;
	var isStart = true;
	
	
	for (var i in nodeArray)
	{
	
		//如果字典nodedic 存在关键字的话
		if(nodedic[nodeArray[i]])
		{
			//alert("key="+nodeArray[i]);
			
			// 如果是第一个点的话
			if (isStart)
			{
				//alert("isStart="+isStart+"\n node_x="+nodedic[nodeArray[i]].x);				
				
				nodeCircle.drawImage(img,nodedic[nodeArray[i]].x-imgWidth,nodedic[nodeArray[i]].y-imgWidth,imgWidth,imgWidth);				
				
				//to get (x,y) of startNode
				lineX = nodedic[nodeArray[i]].x-imgWidth+imgWidth/2;
				lineY = nodedic[nodeArray[i]].y-imgWidth+imgWidth/2;
				
				isStart = false;
			}
			
			
			nodeCircle.drawImage(img,nodedic[nodeArray[i]].x,nodedic[nodeArray[i]].y,60,60);
			
			
			
			nodeLine.beginPath();
			nodeLine.moveTo(lineX,lineY);
			nodeLine.lineTo(nodedic[nodeArray[i]].x+imgWidth/2,nodedic[nodeArray[i]].y+imgWidth/2);
			//draw line from (lineX,lineY) to (nodedic[nodeArray[i]].x,nodedic[nodeArray[i]].y)
			lineX = nodedic[nodeArray[i]].x+imgWidth/2;
			lineY = nodedic[nodeArray[i]].y+imgWidth/2;
			//update(lineX,lineY),move to next node
			nodeLine.closePath();
			nodeLine.strokeStyle="green";
			nodeLine.lineWidth=4
			nodeLine.stroke();		
			
			
		}
		
	}
	

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
	$("#id_input_startTime").val(ct+" 00:00:00");
	$("#id_input_endTime").val(ct+" 23:59:59");

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