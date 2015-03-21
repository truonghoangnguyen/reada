/**
 * convert html to md
 */
function html2md(url, cb){
	
	if (!validateURL(url)){
		alert('invalid url');
		return;
	}	
//	$.get("http://localhost:10081/sign", {"url": url, json:true},
//	  function(data){
//		cb(data);
//	  }, 'jsonp' );

	  $.ajax({
		url:"http://localhost:10081/sign",
		data: {"url": url, json:true},
		dataType: 'jsonp', // Notice! JSONP <-- P (lowercase)
		success:function(j){
			// do stuff with json (in this case an array)
			alert("Success" +j);
		},
		error:function(){
			alert("Error");
		}
	});
}

 function validateURL(textval) {
  var urlregex = new RegExp(
		"^(http|https|ftp)\://([a-zA-Z0-9\.\-]+(\:[a-zA-Z0-9\.&amp;%\$\-]+)*@)*((25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9])\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0)\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0)\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[0-9])|([a-zA-Z0-9\-]+\.)*[a-zA-Z0-9\-]+\.(com|edu|gov|int|mil|net|org|biz|arpa|info|name|pro|aero|coop|museum|[a-zA-Z]{2}))(\:[0-9]+)*(/($|[a-zA-Z0-9\.\,\?\'\\\+&amp;%\$#\=~_\-]+))*$");
  return urlregex.test(textval);
}