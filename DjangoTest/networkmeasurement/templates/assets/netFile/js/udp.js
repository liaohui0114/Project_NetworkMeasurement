$(document).ready(function(){
	$("#id_startNode").addClass("form-control");
	$("#id_endNode").addClass("form-control");

	$("#id_btn_single").on("dblclick",function(){
		Udp_ajax_post($("#id_startNode").val(),$("#id_startNode").val());		
		$("#NodeDisplayID").show();
		$("#PathDisplayID").show();
		$("#OverallDisplayID").hide();
	});
	$("#id_btn_overall").click(function(){
		$("#NodeDisplayID").hide();
		$("#PathDisplayID").hide();
		$("#OverallDisplayID").show();
	});
})


function Udp_ajax_post(startIp,endIp)
{
	alert("Udp_ajax_post");
	$.ajax({
		url:"/protocol/jsonAction",
		data:{
			"startNodeIp":startIp,
			"endNodeIp":endIp,
			"protocol":"udp",
			//form:$("#id_form_node").serialize()  //using & to connetion,style:startNode=192.168.1.152&endNode=192.168.1.152
		},
		type:'POST',
		dataType:'json',
		success:function(data){
			alert("success!\n");
			//x = eval(data); decode json type
			$.each(data,function(i,item){
				//i is key and item is value

				alert("i:"+i+";item:"+item);
				//alert(data[i].bandwidth); //data.i.bandwidth is wrong
				$.each(item,function(key,value){
					//alert("key:"+key+";value:"+value);
					//alert("#id_table_"+i+"_"+key);
					$("#id_table_single_endNode").text($("#id_endNode option:selected").text());
					$("#id_table_single_endNodeIp").text(endIp);
					$("#id_table_"+i+"_"+key).text(value);  //we have set id of <td> and <th>,so we can alter its text
				});
				
			});

		},
		error:function(xhr,type){
			alert("fail!");
		}
	});
}