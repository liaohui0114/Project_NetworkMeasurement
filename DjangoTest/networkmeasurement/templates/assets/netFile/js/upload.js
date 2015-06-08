$(document).ready(function(){
	var i=1;
	$id_table_upload = $("#id_table_upload");
	var	$el;
	var lastTmpBytes = 0;				      	
//using uploadify.js to show progressBar when unloading
	$("#id_upload_btn").uploadify({
		'swf':'assets/netFile/uploadify/uploadify.swf',
		'uploader':'action/UploadAction',
		'progressData':'speed',   //or percentage
		'method':'post',
		'buttonText': '选择文件',
		'fileObjName':'uploadFile',
		'auto':true,
		'removeCompleted':false,
		'fileTypeExts':'^*.*', //filter file type like *.exe
		dataType:'json',
		//'fileSizeLimit':'10GB',
		//'queueID':'id_upload_queueID',
		'onUploadStart':function(file){
			alert('start upload!');
			// $("#id_upload_id").html(i++);
			// $("#id_upload_name").html(file.name);
			// $("#id_upload_status").html("<font color='red'>uploading...</font>");
			$el = $("<tr>\
								<td></td>\
							<td></td>\
							<td id='id_upload_queueID_'"+i+"></td>\
							<td></td>\
							<td></td>\
					  </tr>");
			$id_table_upload.find('tbody').append($el);
			$el.find("td").eq(0).html(i++);
			$el.find("td").eq(1).html(file.name);
			$el.find("td").eq(3).html(file.size+'bytes');
			$el.find("td").eq(4).html("<font color='red'>uploading...</font>");
		},

		'onUploadProgress':function(file, bytesUploaded, bytesTotal, totalBytesUploaded, totalBytesTotal) {
    	//$('#id_upload_progress').html(bytesUploaded + ' bytes / ' + bytesTotal + ' bytes.');

    	$el.find("td").eq(2).html(bytesUploaded + ' bytes / ' + bytesTotal + ' bytes.\n');
    	$("#id_percentage").text((bytesUploaded/bytesTotal)*100);				            	
			
		},

		'onUploadSuccess':function(file,data,response){
			//  var msg="";
			// $.each(data,function(i,item){
			// 	//msg += "key:"+key+";";
			// 	//msg += "value:"+value+"\n";
			// 	alert('ok');
			// });
			alert("success!\n"+data);
			//$("#id_upload_status").html("<font color='red'>success</font>");
			$el.find("td:last").html("<font color='red'>success</font>");

		},
		// onCancel:function(file){
		// 	alert("cancel upload!");
		// },
		'onUploadError':function(file, errorCode, errorMsg, errorString) {
		alert('The file ' + file.name + ' could not be uploaded: ' + errorString);
		//$("#id_upload_status").html("<font color='red'>"+errorString+"</font>");
		$el.find("td:last").html("<font color='red'>"+errorString+"</font>");
	}
	});

});