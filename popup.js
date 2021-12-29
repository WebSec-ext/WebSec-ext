// Purpose - This file contains all the logic relevant to the extension such as getting the URL, calling the server
// side clientServer.php which then calls the core logic.

function transfer(){	
	var tablink;
	chrome.tabs.getSelected(null,function(tab) {
	   	tablink = tab.url;
		$("#p1").text("Selected URL - "+tablink);

		var xhr=new XMLHttpRequest();
		params="url="+tablink;
        // alert(params);
		var markup = "url="+tablink+"&html="+document.documentElement.innerHTML;
		//fetch API call...		
		fetch("http://localhost/WebExt/clientServer.php",{
			method:'POST',
			body:params,
			headers:{
				"Content-Type":"application/x-www-form-urlencoded"
			}
		})
		.then(function(response){
			return response.text()
		})
		.then(function(data){
			//alert(data)
			$("#div1").text(data);
		})
	});
}

$(document).ready(function(){
    $("button").click(function(){	
		var val = transfer();
    });
});

chrome.tabs.getSelected(null,function(tab) {
   	var tablink = tab.url;
	$("#p1").text("Selected Url - "+tablink);
});
