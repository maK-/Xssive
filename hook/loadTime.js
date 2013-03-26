/*
The hook code loads the jquery library from a remote location,
It then polls our attack server for attack code to run.
*/

// Self-invoked function to Load jquery Dynamically!
(function() {
    var start = new Date().getTime();
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
            var end = new Date().getTime();
            var took = end - start;
            window.alert("Attack ID:"+attack_id+" => jQuery is loaded, after "+took+" milliseconds!");
			
        });
    });
})();
