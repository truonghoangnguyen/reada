var me;
var cov = Markdown.getSanitizingConverter(),
	handler = {
		handler: function(){
			window.open('http://en.wikipedia.org/wiki/Markdown');
		}
	},
	editor = new Markdown.Editor(cov, undefined, handler);
editor.run();

function readmarkdown(){
	/**
	 * send url to server and show markdow
	 */
	var ip = $('input[name="url"]');
	// valid url
	if (!validateURL(ip.val())){
		alert('invalid url');
		return;
	}
	//
	ip.attr('disabled', '');
	// send to server
	$.get("/sign", { "url": ip.val(),json:true },
	  function(data){
		  $('#wmd-input').val(data.content);
		  ip.removeAttr('disabled');
		  editor.refreshPreview();
		//console.log(data); // John
	  }, 'json' );
	// show to screen
	
}

 function validateURL(textval) {
  var urlregex = new RegExp(
		"^(http|https|ftp)\://([a-zA-Z0-9\.\-]+(\:[a-zA-Z0-9\.&amp;%\$\-]+)*@)*((25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9])\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0)\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0)\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[0-9])|([a-zA-Z0-9\-]+\.)*[a-zA-Z0-9\-]+\.(com|edu|gov|int|mil|net|org|biz|arpa|info|name|pro|aero|coop|museum|[a-zA-Z]{2}))(\:[0-9]+)*(/($|[a-zA-Z0-9\.\,\?\'\\\+&amp;%\$#\=~_\-]+))*$");
  return urlregex.test(textval);
}