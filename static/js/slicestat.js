/**
 * MyPlugin:    demonstration plugin
 * Version:     0.1
 * Description: Template for writing new plugins and illustrating the different
 *              possibilities of the plugin API.
 *              This file is part of the Manifold project 
 * Requires:    js/plugin.js
 * URL:         http://www.myslice.info
 * Author:      Jordan Augé <jordan.auge@lip6.fr>
 * Copyright:   Copyright 2012-2013 UPMC Sorbonne Universités
 * License:     GPLv3
 */

(function($){

    var SliceStat = Plugin.extend({

        /** XXX to check
         * @brief Plugin constructor
         * @param options : an associative array of setting values
         * @param element : 
         * @return : a jQuery collection of objects on which the plugin is
         *     applied, which allows to maintain chainability of calls
         */
        init: function(options, element) {
	    this.classname="slicestat";
            // Call the parent constructor, see FAQ when forgotten
            this._super(options, element);			 
			
			
            /* Member variables */

            /* Plugin events */

            /* Setup query and record handlers */

            // Explain this will allow query events to be handled
            // What happens when we don't define some events ?
            // Some can be less efficient
            this.listen_query(options.query_uuid);
			
            /* GUI setup and event binding */
            // call function
			if (typeof options.slicename != 'undefined') {
        		options.slicename = options.slicename.replace("ple.","").replace(".","_");
        	}
        	if (typeof options.o == 'undefined') {
        		//options.o = 'cpu';
        	}
        	
        	this.elmt().on('show', options, this.on_show);
        },

        /* PLUGIN EVENTS */
        // on_show like in querytable


        /* GUI EVENTS */

        // a function to bind events here: click change
        // how to raise manifold events


        /* GUI MANIPULATION */

        // We advise you to write function to change behaviour of the GUI
        // Will use naming helpers to access content _inside_ the plugin
        // always refer to these functions in the remaining of the code

        show_hide_button: function() 
        {
            // this.id, this.el, this.cl, this.elts
            // same output as a jquery selector with some guarantees
        },
		
		on_show: function(ev) 
		{
            console.log('slicestat show triggered');
			$('iframe#' + ev.target.id + '-iframe').attr('src','http://plestats.planet-lab.eu/nodes.php?slice='+ev.data.slicename+'&order='+ev.data.o);
		},
        /* TEMPLATES */

        // see in the html template
        // How to load a template, use of mustache

        /* QUERY HANDLERS */

        // How to make sure the plugin is not desynchronized
        // He should manifest its interest in filters, fields or records
        // functions triggered only if the proper listen is done

        // no prefix

        on_filter_added: function(filter)
        {

        },

        // ... be sure to list all events here

        /* RECORD HANDLERS */
        on_new_record: function(record)
        {
        	$('iframe#' + this.elmt().attr('id') + '-iframe').attr('src','http://plestats.planet-lab.eu/node.php?node='+record.hostname);            
        },

        /* INTERNAL FUNCTIONS */
        _dummy: function() {
            // only convention, not strictly enforced at the moment
        },

    });

    /* Plugin registration */
    $.plugin('SliceStat', SliceStat);

    // TODO Here use cases for instanciating plugins in different ways like in the pastie.

})(jQuery);
