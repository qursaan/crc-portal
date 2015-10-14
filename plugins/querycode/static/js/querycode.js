/**
 * Description: display code for a target query in python or ruby
 * Copyright (c) 2012 UPMC Sorbonne Universite - INRIA
 * License: GPLv3
 */

(function($) {
  
    var debug=false;
    //debug=true;

    $.fn.QueryCode = function( method ) {
        /* Method calling logic */
        if ( methods[method] ) {
            return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        } else if ( typeof method === 'object' || ! method ) {
            return methods.init.apply( this, arguments );
        } else {
            $.error( 'Method ' +  method + ' does not exist on jQuery.QueryCode' );
        }    
    };

    var methods = {
	init : function (options) {
	    if (debug) messages.debug("SyntaxHighlighter.all ...");
            SyntaxHighlighter.all();
	    return this.each(function() {
		var $this=$(this);
		var data=$this.data('QueryCode');
		if ( ! data ) {
		    // Subscribe to query updates
		    var channel='/results/' + options.query_uuid + '/updated';
		    /* passing $this as 2nd arg: callbacks will retrieve $this as e.data */
		    $.subscribe(channel, $this, update_plugin);
		    if (debug) messages.debug('subscribing to ' + channel);
		    $this.data('QueryCode', {options: options});
		    // react to changes to the language selector
		    $this.find(".querycode-lang").change(change_language);
		    // publish so we refresh ourselves
		    $.publish(channel,"please_init_yourself");
		}
	    });


	}, 

//	destroy : function( ) {
//	    if (debug) messages.debug("QueryCode.destroy...");
//	},
//	update : function( content ) { 
//	    if (debug) messages.debug("QueryCode.update...");
//	},
	
    } // methods
			  
    // we retrieve the plugindiv as e.data - cf the 2nd arg to subscribe
    // in fact we don't really read the published message
    function update_plugin (e, _) {
	var $plugindiv=e.data;
	do_update ($plugindiv);
    }

    // linked to 'change' on the selector; this=the selector dom
    function change_language (e) {
	var $plugindiv = $(this).closest(".plugin");
	do_update($plugindiv);
    }
 
    function do_update ($plugindiv) {

	var lang=$plugindiv.find(".querycode-lang").val();
	var dom=$plugindiv.find(".querycode-viz");
	var query_uuid = $plugindiv.data().QueryCode.options.query_uuid;
	var query=manifold.find_query(query_uuid);
	funname="translate_query_as_" + lang;
	fun=eval(funname);
	if (! fun) {
	    messages.debug("Cannot find translator function for lang " + lang);
	    return;
	}
	html_code=fun(query);
	dom.html(html_code);
	if (debug) messages.debug("SyntaxHighlighter.highlight");
	SyntaxHighlighter.highlight()
    }


    // private stuff
    function translate_query_as_ruby (query) {
	var output = '# Connection to XMLRPC server\n';
	output += 'require "xmlrpc/client"\n';
	output += 'require "pp"\n';
	output += '\n';
	output += 'XMLRPC::Config.module_eval do\n';
	output += '  remove_const :ENABLE_NIL_PARSER\n';
	output += '  const_set :ENABLE_NIL_PARSER, true\n';
	output += 'end\n';
	output += 'srv = XMLRPC::Client.new2("' + MANIFOLD_URL + '")\n';
	output += '\n';
	output += '# Authentication token\n';
	output += 'auth = {"AuthMethod" => "password", "Username" => "guest", "AuthString" => "guest"}\n';
	output += '\n';

	ifs = '';
	$.each(query.filters, function(i, value) {
            if (ifs != '') ifs += ', ';
            ifs += '"';
            if (value[1] != "=")
		ifs += value[1];
            ifs += value[0] + '" => "' + value[2] + '"';
	});
	ifs = '{' + ifs + '}';
	
	ofs = '';
	$.each(query.fields, function(index, value) {
            if (ofs != '')
		ofs += ', ';
            ofs += '"' + value + '"';
	});
	ofs = '[' + ofs + ']';

	output += 'pp srv.call("' + mixed_case(query.action) +'", auth, "' + query.object + '", "' + query.timestamp + '", ' + ifs + ', ' + ofs + ')';

	var output = '<pre class="brush: ruby; toolbar: false;">' + output + "</pre>";
	return output;

    }

    function translate_query_as_python (query) {
	var output = '# Connection to XMLRPC server\n';
	output += 'import xmlrpclib\n';
	output += 'srv = xmlrpclib.ServerProxy("' + MANIFOLD_URL + '", allow_none=True)\n\n';
	output += '# Authentication token\n';
	output += 'auth = {"AuthMethod": "password", "Username": "name.surname@domain.name", "AuthString": "mypassword"}\n\n';

	ifs = '';
	$.each(query.filters, function(i, value) {
            if (ifs != '')
		ifs += ', ';
            //ifs += '"'
            //if (value[1] != "=")
            //    ifs += value[1];
            ifs += '["' + value[0] + '", "' + value[1] + '", "' + value[2] + '"]';
	});
	ifs = '[' + ifs + ']';
	
	ofs = '';
	$.each(query.fields, function(index, value) {
            if (ofs != '')
		ofs += ', ';
            ofs += '"' + value + '"';
	});
	ofs = '[' + ofs + ']';

	output += 'srv.' + mixed_case(query.action) + '(auth, "' + query.object + '", ' + ifs + ', {}, ' + ofs + ')';
	var output = '<pre class="brush: python; toolbar: false;">' + output + "</pre>";
	return output;
    }

    function mixed_case (txt){ return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();}
    
})(jQuery); // end closure wrapper

