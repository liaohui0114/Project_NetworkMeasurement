$(document).ready(function(){
	var i=1;
	$id_table_upload = $("#id_table_upload");
	var	$el;
	var lastTmpBytes = 0;
	var startTime;
	var endTime;
	var fileSize;				      	
//using uploadify.js to show progressBar when unloading
	$("#id_upload_btn").uploadify({
		'swf':'assets/netFile/uploadify/uploadify.swf',
		'uploader':'action/UploadAction',
		'progressData':'speed',   //or percentage
		'method':'post',
		'buttonText': '选择文件',
		'fileObjName':'uploadFile',
		'fileSizeLimit':'100MB',
		'auto':true,
		'removeCompleted':false,
		'fileTypeExts':'^*.*', //filter file type like *.exe
		dataType:'json',
		//'fileSizeLimit':'10GB',
		//'queueID':'id_upload_queueID',
		'onUploadStart':function(file){
			//alert('start upload!');
			// $("#id_upload_id").html(i++);
			// $("#id_upload_name").html(file.name);
			// $("#id_upload_status").html("<font color='red'>uploading...</font>");
			startTime = new Date().getTime(); //to get timestamp(ms) when file start upload
			$el = $("<tr>\
								<td></td>\
							<td></td>\
							<td id='id_upload_queueID_'"+i+"></td>\
							<td></td>\
							<td></td>\
							<td></td>\
					  </tr>");
			$id_table_upload.find('tbody').append($el);
			$el.find("td").eq(0).html(i++);
			$el.find("td").eq(1).html(file.name);
			$el.find("td").eq(3).html(file.size+'bytes');
			$el.find("td").eq(5).html("<font color='red'>uploading...</font>");
		},

		'onUploadProgress':function(file, bytesUploaded, bytesTotal, totalBytesUploaded, totalBytesTotal) {
    	//$('#id_upload_progress').html(bytesUploaded + ' bytes / ' + bytesTotal + ' bytes.');

	    	$el.find("td").eq(2).html(bytesUploaded + ' bytes / ' + bytesTotal + ' bytes.\n');
	    	$("#id_percentage").text((bytesUploaded/bytesTotal)*100);				            	
			fileSize = bytesTotal;
		},

		'onUploadSuccess':function(file,data,response){
			//  var msg="";
			// $.each(data,function(i,item){
			// 	//msg += "key:"+key+";";
			// 	//msg += "value:"+value+"\n";
			// 	alert('ok');
			// });
			//alert("success!\n"+data);
			//$("#id_upload_status").html("<font color='red'>success</font>");

			$el.find("td:last").html("<font color='red'>success</font>");
			endTime = new Date().getTime(); //to get the timestamp(ms) after file upload 
			//alert(fileSize + ";" + (endTime-startTime));
			var averageSpeed = 0;
			averageSpeed = 1000*fileSize/(endTime-startTime);
			// while (averageSpeed > 1024){
			// 	averageSpeed = averageSpeed/1024;
			// }
			// averageSpeed = Math.round(averageSpeed*100)/100;
			$el.find("td").eq(4).html(getFormat(averageSpeed)+"/s");

		},
		// onCancel:function(file){
		// 	alert("cancel upload!");
		// },
		'onUploadError':function(file, errorCode, errorMsg, errorString) {
		//alert('The file ' + file.name + ' could not be uploaded: ' + errorString);
		//$("#id_upload_status").html("<font color='red'>"+errorString+"</font>");
		$el.find("td:last").html("<font color='red'>"+errorString+"</font>");
	}
	});

});

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