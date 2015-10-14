// INHERITANCE
// http://alexsexton.com/blog/2010/02/using-inheritance-patterns-to-organize-large-jquery-applications/
// We will use John Resig's proposal

// http://pastie.org/517177

// NOTE: missing a destroy function

$.plugin = function(name, object) {
    $.fn[name] = function(options) {
        var args = Array.prototype.slice.call(arguments, 1);
        return this.each(function() {
            var instance = $.data(this, name);
            if (instance) {
                instance[options].apply(instance, args);
            } else {
                instance = $.data(this, name, new object(options, this));
            }
        });
    };
};

// set to either
// * false or undefined or none : no debug
// * true : trace all event calls
// * [ 'in_progress', 'query_done' ] : would only trace to these events
var plugin_debug=false;
plugin_debug = [ 'in_progress', 'query_done' ];

var Plugin = Class.extend({

    init: function(options, element) {
        // Mix in the passed in options with the default options
        this.options = $.extend({}, this.default_options, options);

        // Save the element reference, both as a jQuery
        // reference and a normal reference
        this.element  = element;
        this.$element = $(element);
	// programmatically add specific class for publishing events
	// used in manifold.js for triggering API events
	if ( ! this.$element.hasClass('pubsub')) this.$element.addClass('pubsub');

        // return this so we can chain/use the bridge with less code.
        return this;
    },

    has_query_handler: function() {
        return (typeof this.on_filter_added === 'function');
    },

    // do we need to log API calls ?
    _is_in : function (obj, arr) {
	for(var i=0; i<arr.length; i++) {
            if (arr[i] == obj) return true;
	}
    },
    _deserves_logging: function (event) {
	if ( ! plugin_debug )				return false;
	else if ( plugin_debug === true)		return true;
	else if (this._is_in (event, plugin_debug))	return true;
	return false;
    },

    _query_handler: function(prefix, event_type, data) {
        // We suppose this.query_handler_prefix has been defined if this
        // callback is triggered    
        var event, fn;
        switch(event_type) {
        case FILTER_ADDED:
            event = 'filter_added';
            break;
        case FILTER_REMOVED:
            event = 'filter_removed';
            break;
        case CLEAR_FILTERS:
            event = 'filter_clear';
            break;
        case FIELD_ADDED:
            event = 'field_added';
            break;
        case FIELD_REMOVED:
            event = 'field_removed';
            break;
        case CLEAR_FIELDS:
            event = 'field_clear';
            break;
        default:
            return;
        } // switch
        
        fn = 'on_' + prefix + event;
        if (typeof this[fn] === 'function') {
	    if (this._deserves_logging (event)) {
		var classname=this.classname;
		messages.debug("Plugin._query_handler: calling "+fn+" on "+classname);
	    }
            // call with data as parameter
            // XXX implement anti loop
            this[fn](data);
        }
    },

    _record_handler: function(prefix, event_type, record) {
        // We suppose this.query_handler_prefix has been defined if this
        // callback is triggered    
        var event, fn;
        switch(event_type) {
        case NEW_RECORD:
            event = 'new_record';
            break;
        case CLEAR_RECORDS:
            event = 'clear_records';
            break;
        case IN_PROGRESS:
            event = 'query_in_progress';
            break;
        case DONE:
            event = 'query_done';
            break;
        case FIELD_STATE_CHANGED:
            event = 'field_state_changed';
            break;
        default:
            return;
        } // switch
        
        fn = 'on_' + prefix + event;
        if (typeof this[fn] === 'function') {
	    if (this._deserves_logging (event)) {
		var classname=this.classname;
		messages.debug("Plugin._record_handler: calling "+fn+" on "+classname);
	    }
            // call with data as parameter
            // XXX implement anti loop
            this[fn](record);
        }
    },

    get_handler_function: function(type, prefix) {
        
        return $.proxy(function(e, event_type, record) {
            return this['_' + type + '_handler'](prefix, event_type, record);
        }, this);
    },

    listen_query: function(query_uuid, prefix) {
        // default: prefix = ''
        prefix = (typeof prefix === 'undefined') ? '' : (prefix + '_');

        this.$element.on(manifold.get_channel('query', query_uuid),  this.get_handler_function('query',  prefix));
        this.$element.on(manifold.get_channel('record', query_uuid),  this.get_handler_function('record', prefix));
    },

    default_options: {},

    /* Helper functions for naming HTML elements (ID, classes), with support for filters and fields */

    id: function() {
        var ret = this.options.plugin_uuid;
        for (var i = 0; i < arguments.length; i++) {
            ret = ret + manifold.separator + arguments[i];
        }
        return ret;
    },

    elmt: function() {
        if (arguments.length == 0) {
            return $('#' + this.id());
        } else {
            // We make sure to search _inside_ the dom tag of the plugin
            return $('#' + this.id.apply(this, arguments), this.elmt());
        }
    },

    elts: function(cls) {
        return $('.' + cls, this.elmt());
    },

    id_from_filter: function(filter, use_value) {
        use_value = typeof use_value !== 'undefined' ? use_value : true;

        var key    = filter[0];
        var op     = filter[1];
        var value  = filter[2];
        var op_str = this.getOperatorLabel(op);
        var s      = manifold.separator;

        if (use_value) {
            return 'filter' + s + key + s + op_str + s + value;
        } else {
            return 'filter' + s + key + s + op_str;
        }
    },

    str_from_filter: function(filter) {
        return filter[0] + ' ' + filter[1] + ' ' + filter[2];
    },

    array_from_id: function(id) {
        var ret = id.split(manifold.separator);
        ret.shift(); // remove plugin_uuid at the beginning
        return ret;
    },

    id_from_field: function(field) {
        return 'field' + manifold.separator + field;
    },

    field_from_id: function(id) {
        var array;
        if (typeof id === 'string') {
            array = id.split(manifold.separator);
        } else { // We suppose we have an array ('object')
            array = id;
        }
        // array = ['field', FIELD_NAME]
        return array[1];
    },

    id_from_key: function(key_field, value) {
        
        return key_field + manifold.separator + this.escape_id(value).replace(/\\/g, '');
    },

    // NOTE
    // at some point in time we used to have a helper function named 'flat_id' here
    // the goals was to sort of normalize id's but it turned out we can get rid of that
    // in a nutshell, we would have an id (can be urn, hrn, whatever) and 
    // we want to be able to retrieve a DOM element based on that (e.g. a checkbox)
    // so we did something like <tag id="some-id-that-comes-from-the-db">
    // and then $("#some-id-that-comes-from-the-db")
    // however the syntax for that selector prevents from using some characters in id
    // and so for some of our ids this won't work
    // instead of 'flattening' we now do this instead
    // <tag some_id="then!we:can+use.what$we!want">
    // and to retrieve it
    // $("[some_id='then!we:can+use.what$we!want']")
    // which thanks to the quotes, works; and you can use this with id as well in fact
    // of course if now we have quotes in the id it's going to squeak, but well..

    // escape (read: backslashes) some meta-chars in input
    escape_id: function(id) {
        if( id !== undefined){
            return id.replace( /(:|\.|\[|\])/g, "\\$1" );
        }else{
            return "undefined-id";
        }
    },

    id_from_record: function(method, record) {
        var keys = manifold.metadata.get_key(method);
        if (!keys)
            return;
        if (keys.length > 1)
            return;

        var key = keys[0];
        switch (Object.toType(key)) {
        case 'string':
            if (!(key in record))
                return null;
            return this.id_from_key(key, record[key]);
	    
        default:
            throw 'Not implemented';
        }
    },

    key_from_id: function(id) {
        // NOTE this works only for simple keys

        var array;
        if (typeof id === 'string') {
            array = id.split(manifold.separator);
        } else { // We suppose we have an array ('object')
            array = id;
        }

        // arguments has the initial id but lacks the key field name (see id_from_key), so we are even
        // we finally add +1 for the plugin_uuid at the beginning
        return array[arguments.length + 1];
    },

    // TOGGLE
    // plugin-helper.js is about managing toggled state
    // it would be beneficial to merge it in here
    toggle_on: function () { return this.toggle("true"); },
    toggle_off: function () { return this.toggle("false"); },
    toggle: function (status) {
	plugin_helper.set_toggle_status (this.options.plugin_uuid,status);
    },

    /* SPIN */
    // use spin() to get our default spin settings (called presets)
    // use spin(true) to get spin's builtin defaults
    // you can also call spin_presets() yourself and tweak what you need to, like topmenuvalidation does
    spin: function (presets) {
	var presets = ( presets === undefined ) ? spin_presets() : presets;
	try { this.$element.spin(presets); }
	catch (err) { messages.debug("Cannot turn on spin " + err); }
    },

    unspin: function() {
	try { this.$element.spin(false); }
	catch (err) { messages.debug("Cannot turn off spin " + err); }
    },

    /* TEMPLATE */

    load_template: function(name, ctx) {
        return Mustache.render(this.elmt(name).html(), ctx);
    },

});
