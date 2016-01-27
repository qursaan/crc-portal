/**
 * Description: display messages in a dedicated area, with buttons for filtering on level
 * Copyright (c) 2012 UPMC Sorbonne Universite - INRIA
 * License: GPLv3
 */

( function($) {

    var Messages = Plugin.extend ({

	init: function (options, element) {
	    classname="messages";
	    this._super (options, element);
	    // subscribe to the various messages channels
	    var self=this;
	    for (level in options.levels)
		(function (l) {
		    $.subscribe("/messages/"+l, function (e, msg){ self.display_message (msg,l)});
		})(level);
	    // kind of patchy, notify the convenience functions that somebody is listening...
	    try {messages.ready=true;}
	    catch (err) { console.log("Could not set messages.ready");}
	    // this happens very early - even before the document is loaded
	    // so it won't show right away; no big deal though
            $.publish ("/messages/info", 'Subscribed to all 5 message channels');

	    this.initialize();
	},

	initialize: function () {
	    var self=this;
	    this.elmt().find("div.messages-buttons>input").each(
		function (i,input) {
		    self.init_button (input, self.options.levels);
		    self.arm_button (input, self.toggle_handler);
		}
	    );
	},
	
	init_button: function (input,levels) {
	    /* set initial 'checked' state for that input from global 'levels' above */
	    var level=input.name;
	    if (levels[level]) $(input).attr('checked','checked');
	},

	arm_button: function (input,handler) {
	    $(input).click (handler);
	},
	
	is_active: function (level) { 
	    return this.elmt().find("div.messages-buttons>input[name="+level+"]").attr('checked');
	},
	    
	display_message: function (incoming, level) {
	    var domid=this.elmt().attr('id');
	    var html="";
	    html += "<li class='" + level +"'"; 
	    if ( ! this.is_active(level) ) html += " style='display:none'";
	    html += ">";
	    html += "<span class='messages-fixed'>";
	    html += "<span class='messages-level'>" + level + "</span>";
	    html += "<span class='messages-date'>";
	    html += "</html>";
	    d=new Date();
	    html += d.getHours() + ":" +d.getMinutes() + ":" + d.getSeconds() + "--" + d.getMilliseconds();
	    html += "</span>";
	    //	html += "[" + domid + "]";
	    html += " " + incoming + "</li>";
	    $("ul#"+domid+".messages").append(html);
	},

	/* as an event handler toggle_handler will see the DOM <input> as 'this' */
	toggle_handler : function (e) {
	    var $this=$(this);
	    // toggle the state of the checkbox
	    if ($this.attr('checked')) $this.removeAttr('checked');
	    else $this.attr('checked',true);
	    // turn messages on or off
	    var level=this.name;
	    var display = $this.attr('checked') ? "list-item" : "none";
	    var elmt=$this.closest("div.Messages");
	    elmt.find("li."+level).css("display",display);
	},
	
    });

    $.plugin('Messages', Messages);

})(jQuery);

/* turn this on for an auto-test on startup
var messages_test = {
    // set this to 0 to disable
    counter : 2,
    period : 1000,
    sample : function () { 
	$.publish("/messages/fatal","a fatal message (" + messages_test.counter + " runs to go)");
	$.publish("/messages/error","an error message");
	$.publish("/messages/warning","a warning message");
	$.publish("/messages/info","an info message");
	$.publish("/messages/debug","a debug message");
	messages_test.counter -= 1;
	if (messages_test.counter == 0)
	    window.clearInterval (messages_test.interval_id);
    },
    run: function () {
	messages_test.interval_id=window.setInterval(messages_test.sample , messages_test.period);
    }
}
messages_test.run()
*/
