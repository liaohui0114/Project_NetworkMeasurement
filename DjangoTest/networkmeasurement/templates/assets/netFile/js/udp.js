$(document).ready(function(){
	$("#id_startNode").addClass("form-control");
	$("#id_endNode").addClass("form-control");
	$("#id_btn_single").hover(function()
	{
		$("#id_div_tip").css({
	  'opacity': .5, //透明度
	  'position': 'absolute',

	  //'background-color': 'black',
	  'color':'black',
	  'font-weight ':700,
	  //'width': '200px',
	  //'height':'100px',
	  'z-index': 5000 //保证这个悬浮层位于其它内容之上
	}).html("测量起始结点到终止结点之间的网络性能情况,包括指标：带宽、时延、抖动、拥塞、可用性等");
	  $("#id_div_tip").show();
	},function()
	{
		$("#id_div_tip").hide();
	});
	$("#id_btn_overall").hover(function()
	{
		$("#id_div_tip").css({
	  'opacity': .5, //透明度
	  'position': 'absolute',

	  //'background-color': 'black',
	  'color':'black',
	  'font-weight ':700,
	  //'width': '200px',
	  //'height':'100px',
	  'z-index': 5000 //保证这个悬浮层位于其它内容之上
	}).html("测量所有结点两两之间的网络性能情况,包括指标：带宽、时延、抖动、拥塞、可用性等，全局测量时间比较长，请耐心等候！");
	  $("#id_div_tip").show();
	},function()
	{
		$("#id_div_tip").hide();
	});

	//$("#id_btn_single").on("dblclick",function(){
	//start single test
	$("#id_btn_single").on("click",function(){
		//alert($("#id_btn_single").val());

		//we define that startnode could not be the endnode，起始结点与目标结点不能一致
		//alert($("#id_startNode").val() + $("#id_endNode").val());
		//alert($("#id_startNode").val() ==  $("#id_endNode").val());
		if($("#id_startNode").val() != $("#id_endNode").val())
		{
			var protocol = $("#id_btn_single").val();//get protocol info
			Udp_ajax_post_single(protocol,$("#id_startNode").val(),$("#id_endNode").val(),$("#id_startNode option:selected").text(),$("#id_endNode option:selected").text());		

			$("#NodeDisplayID").show();//show table of single table
			//DisplayNodePath();//draw path diagram
			//$("#PathDisplayID").show();
			$("#ChartDisplayID").show();
			$("#OverallDisplayID").hide(); //show tables of overall network testing
			TracerouteDisplay($("#id_startNode").val(),$("#id_endNode").val(),$("#id_startNode option:selected").text(),$("#id_endNode option:selected").text()); 
		}
		else
		{
			//显示错误信息
			$("#id_div_tip").css({
				'opacity': .5, //透明度
				'position': 'absolute',

				//'background-color': 'black',
				'color':'red',
				'font-weight':700,
				//'width': '200px',
				//'height':'100px',
				'z-index': 5000 //保证这个悬浮层位于其它内容之上
				}).html("*起始结点与目标结点相同");
			$("#id_div_tip").show();
		}
		
	});
	//start overall test
	$("#id_btn_overall").click(function(){
		var protocol = $("#id_btn_overall").val()
		//$("#OverallDisplayID").show();
		
		Udp_ajax_post_overall(protocol);
		$("#NodeDisplayID").hide();
		$("#PathDisplayID").hide();
		$("#ChartDisplayID").hide();
		//$("#OverallDisplayID").show();
	});

})

//protocol: protocol type;1.TCP;2.UDP;3.ICMP;
//startIp:ip of startNode
//endIp:ip of endNode
//startNodeName:name of start node
//endNodeName:name of end node
function Udp_ajax_post_single(protocol,startIp,endIp,startNodeName,endNodeName)
{
	//alert("Udp_ajax_post_single!\n");
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
			//alert("success!\n");
			//x = eval(data); decode json type
			var chartData,chartTime,createTime;
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
					createTime = eval(item.time);  //to get createTime infos

					
				}				
			});

			DisplayActiveChart(chartData,chartTime,createTime); // using plug-in:Highcharts  to display charts;
				

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
			//alert("Fail!!Please check your network!");
			$("#PathDisplayID").hide();
			$("#ChartDisplayID").hide();
			$("#OverallDisplayID").hide();
			//alert("fail!");
		}
	});
}

//overall test
function Udp_ajax_post_overall(protocol)
{
	//alert("Udp_ajax_post_overall!\n");
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
			//alert("success!!!!\n");
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

				//$("#id_table_"+conditon).find('thead').find('tr').append("<th>"+conditon+"</th>");
				$("#id_table_"+conditon).find('thead').find('tr').append("<th>起点->终点</th>");
				var isFirst = true;  // to avoid $("#id_table_"+conditon).find('thead').find('tr').append("<th>"+end+"</th>"); running every <th>
				$.each(startData,function(start,endData){
					var thTmp = "<th>"+start+"</th>";
					
					$.each(endData,function(end,value){

						if(isFirst)
						{
							$("#id_table_"+conditon).find('thead').find('tr').append("<th>"+end+"</th>");
						}					
						
						//$("#id_table_"+conditon).find('tbody').append("<tr><td>"+value+"</td></tr>");
						thTmp += "<td>"+value+"</td>";
						//$("#id_table_"+conditon+" tbody tr").append("<td>"+value+"</td>");
					});
					isFirst = false;
					$("#id_table_"+conditon).find('tbody').append("<tr>"+thTmp+"</tr>");
					
				});

			});
			$("#OverallDisplayID").show();  //show infomations

		},
		error:function(xhr,type){
			hideCover();
			$("#OverallDisplayID").hide();
			$("#NodeDisplayID").hide();
			$("#PathDisplayID").hide();
			$("#ChartDisplayID").hide();
			
			alert("Fail!!Please check your network!");
		}
	});
}

//to display chart of bandwidth 
function DisplayActiveChart(chartData,chartTime,createTime){
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
            text: '起始结点到其它各个结点最近10次测量结果数据统计',
            x: -20 //center
        },
        subtitle: {
            text: '测量指标：当前网络可达的最大发送带宽!',
            x: -20
        },
        xAxis: {
            categories: chartTime,  // to show xAxis
            title: {
                text: 'Index'
            }
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
            //valueSuffix: 'Mp/s'

            //valueSuffix: 'Mp/s'
            //valueSuffix: unit #defualut
            //added by liaohui
            //define format output
            formatter: function() {
            	var i = 0;
                return '<b>'+ this.series.name +':</b>'+ this.y+' Mp/s'
                +'<br><b>时间:</b>'+(new Date(createTime[this.series.name][this.x-1]*1000).Format("yyyy-MM-dd hh:mm:ss"));
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

/*
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
*/
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
	  //'background-color': 'white',
	  'width': '100%',
	  'z-index': 5000 //保证这个悬浮层位于其它内容之上
	});
	$('#id_img_cover').css({
	  'opacity': .9, //透明度
	  'position': 'absolute',
	  'top': 350,  //from top
	  'left': 500,  //from left
	  //'background-color': 'white',
	});

	$('#id_div_cover').show();   //show the div


}
//hide div: #id_div_cover
function hideCover()
{				    
	setTimeout(function(){$('#id_div_cover').fadeOut('slow')}, 1000); //设置1秒后覆盖层自动淡出
}
/*
//function:to get trace path info by traceroute command
function TracerouteDisplay(startIp,endIp,startNodeName,endNodeName)
{
	//alert("Udp_ajax_post_single!\n");
	$.ajax({
		url:"/action/TracerouteAction",
		//async: false, //if we want to lock the screen
		data:{
			"startNodeIp":startIp,
			"endNodeIp":endIp,
			"startNodeName":startNodeName,
			"endNodeName":endNodeName,
			"protocol":"TRACEROUTE",
			//form:$("#id_form_node").serialize()  //using & to connetion,style:startNode=192.168.1.152&endNode=192.168.1.152
		},
		type:'POST',//action:post or get
		dataType:'json',
		beforeSend:function(){
			//alert("beforeSend!");
			//showCover(); //在数据发送前，显示遮罩層，锁定屏幕
		},
		success:function(data){
			var radius = 15;
			var offet = 200;
			var st_x = 100;
			var st_y = 100;
			var imgWidth = 60; //width 60px
			///////init  draw pic/////////
			/////clear canvas///////
			var can = document.getElementById('id_canvas_router');
			var clearNode = can.getContext('2d');
			clearNode.fillStyle = "green";
			clearNode.strokeStyle = "green";
			clearNode.lineWidth = 4;
			clearNode.clearRect(0,0,1024,400);
			
			////////draw startNode///////////
			var img = document.getElementById("id_img_router");
			var node = can.getContext('2d');
			node.drawImage(img,st_x,st_y,imgWidth,imgWidth);

			var nodeText = can.getContext('2d');
			nodeText.font = "10px Arial";
			var startText = startIp + "\n("+startNodeName+")";
			nodeText.fillText(startText,st_x-imgWidth/2,st_y+imgWidth);

			var cxt = can.getContext('2d');
			cxt.beginPath();
			cxt.moveTo(st_x+imgWidth,st_y+imgWidth/2);

			

			$.each(data,function(i,item){
				st_x = st_x + offet;
				node.drawImage(img,st_x,st_y,imgWidth,imgWidth);
				tmpText = i + "("+item+")";
				nodeText.fillText(tmpText,st_x-imgWidth/2,st_y+imgWidth);

				cxt.lineTo(st_x,st_y+imgWidth/2);
				cxt.moveTo(st_x+imgWidth,st_y+imgWidth/2);
			});
			
			//draw end Node
			st_x = st_x + offet;
			node.drawImage(img,st_x,st_y,imgWidth,imgWidth);
			var endText = endIp + "("+endNodeName+")";
			nodeText.fillText(endText,st_x-imgWidth/2,st_y+imgWidth);

			cxt.lineTo(st_x,st_y+imgWidth/2);
			cxt.closePath();
			cxt.stroke();


		},
		error:function(xhr,type){
			$("#PathDisplayID").hide();
		}
	});
}
*/
//function:to get trace path info by traceroute command
function TracerouteDisplay(startIp,endIp,startNodeName,endNodeName)
{
	//alert("Udp_ajax_post_single!\n");
	$.ajax({
		url:"/action/TracerouteAction",
		//async: false, //if we want to lock the screen
		data:{
			"startNodeIp":startIp,
			"endNodeIp":endIp,
			"startNodeName":startNodeName,
			"endNodeName":endNodeName,
			"protocol":"TRACEROUTE",
			//form:$("#id_form_node").serialize()  //using & to connetion,style:startNode=192.168.1.152&endNode=192.168.1.152
		},
		type:'POST',//action:post or get
		dataType:'json',
		beforeSend:function(){
			//alert("beforeSend!");
			//showCover(); //在数据发送前，显示遮罩層，锁定屏幕
		},
		success:function(data){
			$("#PathDisplayID").show();
			$.each(data,function(i,item){
				//i is key and item is value
				if("url" == i) //to get table data
				{
					//alert("url:"+item);
					$("#id_img_traceroute").attr("src",item);
				}
			});

		},
		error:function(xhr,type){
			//alert("trace fail!");
			$("#PathDisplayID").hide();
		}
	});
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
