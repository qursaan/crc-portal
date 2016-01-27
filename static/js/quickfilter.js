/**
 * Description: editing search filters
 * Copyright (c) 2012 UPMC Sorbonne Universite - INRIA
 * License: GPLv3
 */
// global metadata from js/metadata.js
( function($){

    var debug=false;
    //debug=true;

    $.fn.QuickFilter = function( method ) {
        /* Method calling logic */
        if ( methods[method] ) {
            return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        } else if ( typeof method === 'object' || ! method ) {
            return methods.init.apply( this, arguments );
        } else {
            $.error( 'Method ' +  method + ' does not exist on $.QuickFilter' );
        }    
    };


    var methods = {

	init : function( options ) {
	    return this.each(function(){
		
		var $this = $(this),
		data = $this.data('QuickFilter'), QuickFilter = $('<div />', {text : $this.attr('title')});
		
		if ( ! data ) {
		    
		    data = $(this).data();

		    /* Subscribe to selection updates published by the resource display plugins */
		    //$.subscribe('selected', {instance: $this}, resource_selected);
		    $.subscribe('/query/' + options.query_uuid + '/changed', {instance: $this}, query_changed);


		    /* End of plugin initialization */

		    $(this).data('QuickFilter', {
			plugin_uuid: options.plugin_uuid,
			query_uuid: options.query_uuid,
			target : $this,
			QuickFilter : QuickFilter
		    });

		    $(this).data('current_query', null);

		    initialize_plugin($(this).data());
		    
		    function update_options(e, rows){
			var d = data;
			var availableTags={};
			$.each (rows, function(index, obj) {
			    $.each(obj,function(key,value){                       
				value = unfold.get_value(value);
				if(!availableTags.hasOwnProperty(key)){availableTags[key]=new Array();}
				//availableTags[key].push(value);
				var currentArray=availableTags[key];
				if(value!=null){
				    if($.inArray(value,currentArray)==-1){availableTags[key].push(value);}
				}
			    });                    
			});                
			$.each(availableTags, function(key, value){
			    value.sort();
			    if($("#"+options.plugin_uuid+"-select_"+key).length>0){
				$.each(value, function(k, optValue){
				    $("#"+options.plugin_uuid+"-select_"+key).append('<option>'+optValue+'</option>');
				});
			    }                    
			    if($("#QuickFilter-string-"+key).length>0){
				$("#QuickFilter-string-"+key).autocomplete({
                                    source: value,
                                    minLength: 0, // allows to browse items with no value typed in
                                    select: function(event, ui) {
                                        //var key=getKeySplitId(this.id,"-");
                                        var op='=';
                                        var val=ui.item.value;

                                        query=d.current_query;
                                        query.update_filter(key,op,val);
                                        // Publish the query changed, the other plugins with subscribe will get the changes
                                        $.publish('/query/' + query.query_uuid + '/changed', query);
                                        //add_ActiveFilter("#QuickFilter-string-"+key,ui.item.value,d);
                                    }
				});
			    }
			});   
			
			
		    }     
		    
		    /* Subscribe to results in order to redraw the table when updates arrive */
		    $.subscribe('/results/' + options.query_uuid + '/changed', {instance: $this}, update_options);
		}

	    });
	},
	destroy : function( ) {

            return this.each(function(){
		var $this = $(this), data = $this.data('QuickFilter');
		$(window).unbind('QuickFilter');
		data.QuickFilter.remove();
		$this.removeData('QuickFilter');
            })

		},
	update : function( content ) { 
	},
    };

    /* Private methods */

    function query_changed(e, query) {
        //panos: this takes a lot of time!
        data = e.data.instance.data();
        var plugin_uuid=data.QuickFilter.plugin_uuid;
        
        /* Compare current and advertised query to get added and removed fields */
        var previous_query=data.current_query;
        /* Save the query as the current query */
        data.current_query=query;
        
        // XXX can we modify data directly ?
        //$(data.QuickFilter.target).data('current_query', query);

        if(previous_query!=null){
            // If query has changed in another plugin
            // set the value on each filter that exists in QuickFilter plugin          
            if (typeof(previous_query) != 'undefined') {
                var tmp=previous_query.diff_filter(query);
                // Remove first to clean up select boxes
                var removed_filters = tmp.removed;
                $.each(removed_filters, function(i,filter){
                    messages.debug(filter[0]);
                    allowedValues=metadata.property('resource', filter[0], 'allowed_values');
                    if (allowedValues!='' && allowedValues!="N/A") {
			//if(MANIFOLD_METADATA[filter[0]]['allowed_values']!=''){
                        $('#QuickFilter_select_field').val("#");
                        $('#QuickFilter_select_value').children().remove().end();
                        $('#QuickFilter_select_value_container').hide();
                    }
                    if($('#'+plugin_uuid+'-select_'+filter[0]).length>0 && filter[1]=="="){
                        $('#'+plugin_uuid+'-select_'+filter[0]).val(null);
                    }
                    if($("#QuickFilter-string-"+filter[0]).length>0 && filter[1]=="="){
                        $("#QuickFilter-string-"+filter[0]).val(null); 
                    }
                });
                // Then Add filters
                var added_filters = tmp.added;
                $.each(added_filters, function(i,filter){
                    if($('#'+plugin_uuid+'-select_'+filter[0]).length>0 && filter[1]=="="){
                        $('#'+plugin_uuid+'-select_'+filter[0]).val(filter[2]);
                    }
                    if($("#QuickFilter-string-"+filter[0]).length>0 && filter[1]=="="){
                        $("#QuickFilter-string-"+filter[0]).val(filter[2]); 
                    }
                });
            }
            $.publish('debug', "Quick Filter received fields: " + query.fields+" - filter = "+query.filter);
        }
    }
    
    function initialize_plugin(data) {

        $('#QuickFilter_select_value_div').hide();
        $('#QuickFilter_string_value_div').hide();
        $('#QuickFilter_int_value_div').hide();

        $('#QuickFilter_only_visible').click( function () {

            var only_visible = this.checked;
            // Clear all options in the select box, Then add None option
            $('#QuickFilter_select_field').children().remove().end().append("<option value='#'>None</option>");
            
            // Get the current query (ONLY AFTER THE PLUGIN HAS BEEN INITIALIZED)
            var query = data.current_query;
            // iterate to remove each active filter
            if (only_visible) {
                if (typeof(query.fields) != 'undefined') {
                    $.each (query.fields, function(index, value) {
                        $('#QuickFilter_select_field').append("<option>"+value+"</option>");  
                    });            
                }
            }else{
                headers=metadata.fields('resource');
                $.each (headers, function (key, value) {
                    $('#QuickFilter_select_field').append("<option>"+value['column']+"</option>");
                });
            }
        });

        $('#QuickFilter_select_field').change( function () {
            var field = $(this).val();
            messages.debug(field);
            $('input[id^="QuickFilter-string-"]').hide();
            $('#QuickFilter_int_value_div').hide();
            if(field=="#"){
                $('#QuickFilter_select_value_container').hide();
            }else{
                $('#QuickFilter_select_value_container').show();
                $.publish('debug','field selected = '+field);
                valType=metadata.property('resource', field, 'value_type');
                if (valType == 'string' || valType=="N/A") {
                    // If this key has predefined values, build a select with each allowed values as options
                    allowedValues=metadata.property('resource', field, 'allowed_values');
                    if (allowedValues!='' && allowedValues!="N/A") {
                        $('#QuickFilter_string_value_div').hide();
                        $('#QuickFilter_int_value_div').hide();
                        $('#QuickFilter_select_value_div').show();
                        $('#QuickFilter_select_value').show();
                        $('#QuickFilter_select_value').children().remove().end().append("<option value=''>all</option>");
			// @TODO: define seperator as ;
                        allowed_values = allowedValues.split(",");
                        $.each (allowed_values, function (key, value) {
                            $('#QuickFilter_select_value').append("<option>"+value+"</option>");
                        });
			// Else build an autocomplete based on the values of result query
                    }else{
                        $('#QuickFilter_select_value_div').hide();
                        $('#QuickFilter_string_value_div').show();
                        $('.QuickFilter-filter-value').hide();
                        $('#QuickFilter-string-'+field).show();
                        $('#QuickFilter_int_value_div').hide();
                    }
                }
                else if (valType == 'int') {
                    $('#QuickFilter_select_value_div').hide();
                    $('#QuickFilter_string_value_div').hide();
                    $('#QuickFilter_int_value_div').show();
                }
            }
        });

        $('.QuickFilter-filter-value').change( function () {
            var query = data.current_query;

            var filter_value = $(this).val();
            var filter_field = $('#QuickFilter_select_field').val();

            query.update_filter(filter_field, '=', filter_value);
            $.publish('/query/' + query.query_uuid + '/changed', query);
        });
        
        $('.QuickFilter_select').change( function() {
            messages.debug(this.id);
            var query = data.current_query;
	    var f_value = $(this).val();
            
            var key = this.id.split("_");

            // jordan ???
	    /*            
			  if (f_value == "Network")
			  f_value = "";
	    */
            if(typeof(key[1])!="undefined"){
                messages.debug(key[1]+'='+f_value);
                if(f_value==""){
                    query.remove_filter(key[1],"","");
                }else{
                    query.update_filter(key[1], '=', f_value);
                }
            }
            $.publish('/query/' + query.query_uuid + '/changed', query);
        });

    }

})( jQuery );
