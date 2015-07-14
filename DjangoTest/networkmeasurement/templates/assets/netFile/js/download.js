$(document).ready(function(){
	$("#id_select_video").change(function(){
		//$("#videoShowID").attr("src",$("#id_video_select option:selected").val());
		$("#videoShowID").attr("src",$(this).val());
	});

	$("#id_select_downloadFile").change(function(){
		//$("#videoShowID").attr("src",$("#id_select_video option:selected").val());
		//alert($(this).val());
	});
	$("#id_btn_download").click(function(){
		//alert("start download!"+$("#id_select_downloadFile option:selected").val());
		window.location.href=$("#id_select_downloadFile option:selected").val();  //to get a href's location
	});
	
})
