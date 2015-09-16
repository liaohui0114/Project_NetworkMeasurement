$(document).ready(function(){
	$("#id_select_video").change(function(){
		//$("#videoShowID").attr("src",$("#id_video_select option:selected").val());
		$("#videoShowID").attr("src",$(this).val());
	});

	$("#id_select_downloadFile").change(function(){
		//$("#videoShowID").attr("src",$("#id_select_video option:selected").val());
		//alert($(this).val());
	});
	$("#id_btn_download").on("click",function(){
		//alert("start download!"+$("#id_select_downloadFile option:selected").val());
		//window.location.href=$("#id_select_downloadFile option:selected").val();  //to get a href's location
		//$("#id_div_download").hide();
		var fileSize = 0;
		var url = $("#id_select_downloadFile option:selected").val();
		switch(url){
			case "assets/netFile/downloadFile/low":
				fileSize = 1*1024*1024; //B
				break;
			case "assets/netFile/downloadFile/middle":
				fileSize = 10*1024*1024; //B
				break;
			case "assets/netFile/downloadFile/high":
				fileSize = 300*1024*1024;
				break;
		}
		
		//var startTime = new Date().getTime(); //ms
		var startDate = new Date();
		//var endTime;
		 $.ajax(window.location.href=url)
		 .done(function () {

		 	//endTime = new Date().getTime(); //ms
		 	var endDate = new Date();
		 	var duration = endDate.getTime()- startDate.getTime(); //ms
		 	var speed = getFormat(1000*fileSize/duration); //Bps
		 	//alert('File download a success! endTime-startTime=:'+(endDate-startDate)+";speed:"+speed+"/s"); 
		 	$("#id_div_download").find("li").eq(0).html("<strong>开始时间:</strong>"+ getFormatTime(startDate));
		 	$("#id_div_download").find("li").eq(1).html("<strong>结束时间:</strong>"+getFormatTime(endDate));
		 	$("#id_div_download").find("li").eq(2).html("<strong>持续时间:</strong>"+duration+" ms");
		 	$("#id_div_download").find("li").eq(3).html("<strong>平均速度:</strong>"+speed +"/s");
		 	$("#id_div_download").show();
		 })
		 .fail(function () { 
		 	alert('File download failed!'); 
		 	$("#id_div_download").hide();
		 });
	});
	
})

//format b/B to KB, MB, GB
function getFormat(data){
	var counter = 0;
	var msg = "";
	while (data>1000){
		data = data/1000;
		counter = counter+1;
	}
	data = Math.round(data*100)/100; //keep last two after .,like 1.01,1.32...
	switch(counter){
		case 0:
			msg = data+" B";
			break;
		case 1:
			msg = data+" KB";
			break;
		case 2:
			msg = data +" MB";
			break;
		case 3:
			msg = data + " GB";
			break;
		default:
			break;
	}
	return msg;
}

function getFormatTime(date){
	var timeStr = date.getFullYear()+'-'+date.getMonth()+'-'+date.getDate()+' '+date.getHours()+":"+date.getMinutes()+":"+date.getSeconds()+":"+date.getMilliseconds();
	return timeStr;
}
