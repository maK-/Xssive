var module_name = 'matrix.js'

$('body').replaceWith('<canvas id=q />');

//Matrix code from reddit
//http://www.reddit.com/r/programming/comments/1ag0c3/someone_posted_an_htmljavascript_implementation/

var q=document.getElementById('q'),s=window.screen,w=q.width=s.width,h=q.height=s.height,p=Array(256).join(1).split(''),c=q.getContext("2d"),m=Math,r=m.random;setInterval(function(){c.fillStyle="rgba(0,0,0,0.05)";c.fillRect(0,0,w,h);c.fillStyle="rgba(0,255,0,1)";p=p.map(function(v,i){c.fillText(String.fromCharCode(m.floor(2720+r()*33)),i*10,v);v+=10;if(v>768+r()*1e4)v=0;return v})},33)
