$(document).ready(function(){
	$("#id_startNode").addClass("form-control");
	$("#id_endNode").addClass("form-control");

	//$("#id_btn_single").on("dblclick",function(){
	//start single test
	$("#id_btn_single").on("click",function(){
		Udp_ajax_post_single("udp",$("#id_startNode").val(),$("#id_endNode").val(),$("#id_startNode option:selected").text(),$("#id_endNode option:selected").text());		

		$("#NodeDisplayID").show();//show table of single table
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
		success:function(data){
			alert("success!\n");
			//x = eval(data); decode json type
			var chartData,chartTime;
			$.each(data,function(i,item){
				//i is key and item is value
				
				alert("i:"+i+";item:"+item);
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
		success:function(data){
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