// messages runtime -- convenience functions messages.debug and the like
// in addition, messages can get lost if the UI is not ready to accept them
// so we use console.log in this case
var messages = {
    ready : false,
    levels : ['fatal','error','warning','info','debug'],
    handler : function (level,msg) {
	if (messages.ready) $.publish("/messages/"+level,msg);
	else console.log("/messages/"+level+"/: "+msg);
    },
};
for (var i in messages.levels) { 
    var level=messages.levels[i]; 
    (function (level) { messages[level]=function (msg) {messages.handler (level,msg)};})(level);
}
// messages.ready is set by the messages plugin once it is ready to listen on the 5 channels
// this way messages don't get lost if the view does not have a messages instance
//$(function(){messages.ready=true;})
    

