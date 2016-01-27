// utilities 
function debug_dict_keys (msg, o) {
    var keys=[];
    for (var k in o) keys.push(k);
    messages.debug ("debug_dict_keys: " + msg + " keys= " + keys);
}
function debug_dict (msg, o) {
    for (var k in o) messages.debug ("debug_dict: " + msg + " [" + k + "]=" + o[k]);
}
function debug_value (msg, value) {
    messages.debug ("debug_value: " + msg + " " + value);
}
function debug_query (msg, query) {
    if (query === undefined) messages.debug ("debug_query: " + msg + " -> undefined");
    else if (query == null) messages.debug ("debug_query: " + msg + " -> null");
    else if ('query_uuid' in query) messages.debug ("debug_query: " + msg + query.__repr());
    else messages.debug ("debug_query: " + msg + " query= " + query);
}

// http://javascriptweblog.wordpress.com/2011/08/08/fixing-the-javascript-typeof-operator/
Object.toType = (function toType(global) {
  return function(obj) {
    if (obj === global) {
      return "global";
    }
    return ({}).toString.call(obj).match(/\s([a-z|A-Z]+)/)[1].toLowerCase();
  }
})(this);

/* ------------------------------------------------------------ */

// Constants that should be somehow moved to a plugin.js file
var FILTER_ADDED   = 1;
var FILTER_REMOVED = 2;
var CLEAR_FILTERS  = 3;
var FIELD_ADDED    = 4;
var FIELD_REMOVED  = 5;
var CLEAR_FIELDS   = 6;
var NEW_RECORD     = 7;
var CLEAR_RECORDS  = 8;
var FIELD_STATE_CHANGED = 9;

var IN_PROGRESS    = 101;
var DONE           = 102;

/* Update requests related to subqueries */
var SET_ADD        = 201;
var SET_REMOVED    = 202;

// request
var FIELD_REQUEST_CHANGE  = 301;
var FIELD_REQUEST_ADD     = 302;
var FIELD_REQUEST_REMOVE  = 303;
var FIELD_REQUEST_ADD_RESET = 304;
var FIELD_REQUEST_REMOVE_RESET = 305;
// status
var FIELD_REQUEST_PENDING = 401;
var FIELD_REQUEST_SUCCESS = 402;
var FIELD_REQUEST_FAILURE = 403;

/* Query status */
var STATUS_NONE               = 500; // Query has not been started yet
var STATUS_GET_IN_PROGRESS    = 501; // Query has been sent, no result has been received
var STATUS_GET_RECEIVED       = 502; // Success
var STATUS_GET_ERROR          = 503; // Error
var STATUS_UPDATE_PENDING     = 504;
var STATUS_UPDATE_IN_PROGRESS = 505;
var STATUS_UPDATE_RECEIVED    = 506;
var STATUS_UPDATE_ERROR       = 507;

/* Requests for query cycle */
var RUN_UPDATE     = 601;

/* MANIFOLD types */
var TYPE_VALUE  = 1;
var TYPE_RECORD = 2;
var TYPE_LIST_OF_VALUES = 3;
var TYPE_LIST_OF_RECORDS = 4;


// A structure for storing queries

function QueryExt(query, parent_query_ext, main_query_ext, update_query_ext, disabled) {

    /* Constructor */
    if (typeof query == "undefined")
        throw "Must pass a query in QueryExt constructor";
    this.query                 = query;
    this.parent_query_ext      = (typeof parent_query_ext      == "undefined") ? null  : parent_query_ext;
    this.main_query_ext        = (typeof main_query_ext        == "undefined") ? null  : main_query_ext;
    this.update_query_ext      = (typeof update_query_ext      == "undefined") ? null  : update_query_ext;
    this.update_query_orig_ext = (typeof update_query_orig_ext == "undefined") ? null  : update_query_orig_ext;
    this.disabled              = (typeof update_query_ext      == "undefined") ? false : disabled;
    
    this.status       = null;
    this.results      = null;
    // update_query null unless we are a main_query (aka parent_query == null); only main_query_fields can be updated...
}

function QueryStore() {

    this.main_queries     = {};
    this.analyzed_queries = {};

    /* Insertion */

    this.insert = function(query) {
        // We expect only main_queries are inserted
        
        /* If the query has not been analyzed, then we analyze it */
        if (query.analyzed_query == null) {
            query.analyze_subqueries();
        }

        /* We prepare the update query corresponding to the main query and store both */
        /* Note: they have the same UUID */

        // XXX query.change_action() should become deprecated
        update_query = query.clone();
        update_query.action = 'update';
        update_query.analyzed_query.action = 'update';
        update_query.params = {};
        update_query_ext = new QueryExt(update_query);

        /* We remember the original query to be able to reset it */
        update_query_orig_ext = new QueryExt(update_query.clone());


        /* We store the main query */
        query_ext = new QueryExt(query, null, null, update_query_ext, update_query_orig_ext, false);
        manifold.query_store.main_queries[query.query_uuid] = query_ext;
        /* Note: the update query does not have an entry! */


        // The query is disabled; since it is incomplete until we know the content of the set of subqueries
        // XXX unless we have no subqueries ???
        // we will complete with params when records are received... this has to be done by the manager
        // SET_ADD, SET_REMOVE will change the status of the elements of the set
        // UPDATE will change also, etc.
        // XXX We need a proper structure to store this information...

        // We also need to insert all queries and subqueries from the analyzed_query
        // XXX We need the root of all subqueries
        query.iter_subqueries(function(sq, data, parent_query) {
            if (parent_query)
                parent_query_ext = manifold.query_store.find_analyzed_query_ext(parent_query.query_uuid);
            else
                parent_query_ext = null;
            // XXX parent_query_ext == false
            // XXX main.subqueries = {} # Normal, we need analyzed_query
            sq_ext = new QueryExt(sq, parent_query_ext, query_ext)
            manifold.query_store.analyzed_queries[sq.query_uuid] = sq_ext;
        });

        // XXX We have spurious update queries...
    }

    /* Searching */

    this.find_query_ext = function(query_uuid) {
        return this.main_queries[query_uuid];
    }

    this.find_query = function(query_uuid) {
        return this.find_query_ext(query_uuid).query;
    }

    this.find_analyzed_query_ext = function(query_uuid) {
        return this.analyzed_queries[query_uuid];
    }

    this.find_analyzed_query = function(query_uuid) {
        return this.find_analyzed_query_ext(query_uuid).query;
    }
}

/*!
 * This namespace holds functions for globally managing query objects
 * \Class Manifold
 */
var manifold = {

    /************************************************************************** 
     * Helper functions
     **************************************************************************/ 

    separator: '__',

    get_type: function(variable) {
        switch(Object.toType(variable)) {
            case 'number':
            case 'string':
                return TYPE_VALUE;
            case 'object':
                return TYPE_RECORD;
            case 'array':
                if ((variable.length > 0) && (Object.toType(variable[0]) === 'object'))
                    return TYPE_LIST_OF_RECORDS;
                else
                    return TYPE_LIST_OF_VALUES;
        }
    },

    /************************************************************************** 
     * Metadata management
     **************************************************************************/ 

     metadata: {

        get_table: function(method) {
            var table = MANIFOLD_METADATA[method];
            return (typeof table === 'undefined') ? null : table;
        },

        get_columns: function(method) {
            var table = this.get_table(method);
            if (!table) {
                return null;
            }

            return (typeof table.column === 'undefined') ? null : table.column;
        },

        get_key: function(method) {
            var table = this.get_table(method);
            if (!table)
                return null;

            return (typeof table.key === 'undefined') ? null : table.key;
        },


        get_column: function(method, name) {
            var columns = this.get_columns(method);
            if (!columns)
                return null;

            $.each(columns, function(i, c) {
                if (c.name == name)
                    return c
            });
            return null;
        },

        get_type: function(method, name) {
            var table = this.get_table(method);
            if (!table)
                return null;

            return (typeof table.type === 'undefined') ? null : table.type;
        }

     },

    /************************************************************************** 
     * Query management
     **************************************************************************/ 

    query_store: new QueryStore(),

    // XXX Remaining functions are deprecated since they are replaced by the query store

    /*!
     * Associative array storing the set of queries active on the page
     * \memberof Manifold
     */
    all_queries: {},

    /*!
     * Insert a query in the global hash table associating uuids to queries.
     * If the query has no been analyzed yet, let's do it.
     * \fn insert_query(query)
     * \memberof Manifold
     * \param ManifoldQuery query Query to be added
     */
    insert_query : function (query) { 
        // NEW API
        manifold.query_store.insert(query);

        // FORMER API
        if (query.analyzed_query == null) {
            query.analyze_subqueries();
        }
        manifold.all_queries[query.query_uuid]=query;
    },

    /*!
     * Returns the query associated to a UUID
     * \fn find_query(query_uuid)
     * \memberof Manifold
     * \param string query_uuid The UUID of the query to be returned
     */
    find_query : function (query_uuid) { 
        return manifold.all_queries[query_uuid];
    },

    /************************************************************************** 
     * Query execution
     **************************************************************************/ 

    // trigger a query asynchroneously
    proxy_url : '/manifold/proxy/json/',

    // reasonably low-noise, shows manifold requests coming in and out
    asynchroneous_debug : true,
    // print our more details on result publication and related callbacks
    pubsub_debug : false,

    /**
     * \brief We use js function closure to be able to pass the query (array)
     * to the callback function used when data is received
     */
    success_closure: function(query, publish_uuid, callback) {
        return function(data, textStatus) {
            manifold.asynchroneous_success(data, query, publish_uuid, callback);
        }
    },

    run_query: function(query, callback) {
        // default value for callback = null
        if (typeof callback === 'undefined')
            callback = null; 

        var query_json = JSON.stringify(query);

        /* Nothing related to pubsub here... for the moment at least. */
        //query.iter_subqueries(function (sq) {
        //    manifold.raise_record_event(sq.query_uuid, IN_PROGRESS);
        //});

        $.post(manifold.proxy_url, {'json': query_json} , manifold.success_closure(query, null, callback));
    },

    // Executes all async. queries - intended for the javascript header to initialize queries
    // input queries are specified as a list of {'query_uuid': <query_uuid> }
    // each plugin is responsible for managing its spinner through on_query_in_progress
    asynchroneous_exec : function (query_exec_tuples) {
        
        // Loop through input array, and use publish_uuid to publish back results
        $.each(query_exec_tuples, function(index, tuple) {
            var query=manifold.find_query(tuple.query_uuid);
            var query_json=JSON.stringify (query);
            var publish_uuid=tuple.publish_uuid;
            // by default we publish using the same uuid of course
            if (publish_uuid==undefined) publish_uuid=query.query_uuid;
            if (manifold.pubsub_debug) {
                messages.debug("sending POST on " + manifold.proxy_url + query.__repr());
            }

            query.iter_subqueries(function (sq) {
                manifold.raise_record_event(sq.query_uuid, IN_PROGRESS);
            });

            // not quite sure what happens if we send a string directly, as POST data is named..
            // this gets reconstructed on the proxy side with ManifoldQuery.fill_from_POST
            $.post(manifold.proxy_url, {'json':query_json}, 
                   manifold.success_closure(query, publish_uuid, tuple.callback));
        })
    },

    /**
     * \brief Forward a query to the manifold backend
     * \param query (dict) the query to be executed asynchronously
     * \param callback (function) the function to be called when the query terminates
     */
    forward: function(query, callback) {
        var query_json = JSON.stringify(query);
        $.post(manifold.proxy_url, {'json': query_json} , 
               manifold.success_closure(query, query.query_uuid, callback));
    },

    /*!
     * Returns whether a query expects a unique results.
     * This is the case when the filters contain a key of the object
     * \fn query_expects_unique_result(query)
     * \memberof Manifold
     * \param ManifoldQuery query Query for which we are testing whether it expects a unique result
     */
    query_expects_unique_result: function(query) {
        /* XXX we need functions to query metadata */
        //var keys = MANIFOLD_METADATA[query.object]['keys']; /* array of array of field names */
        /* TODO requires keys in metadata */
        return true;
    },

    /*!
     * Publish result
     * \fn publish_result(query, results)
     * \memberof Manifold
     * \param ManifoldQuery query Query which has received results
     * \param array results results corresponding to query
     */
    publish_result: function(query, result) {
        if (typeof result === 'undefined')
            result = [];

        // NEW PLUGIN API
        manifold.raise_record_event(query.query_uuid, CLEAR_RECORDS);
        if (manifold.pubsub_debug)
            messages.debug(".. publish_result (1) ");
        var count=0;
        $.each(result, function(i, record) {
            manifold.raise_record_event(query.query_uuid, NEW_RECORD, record);
            count += 1;
        });
        if (manifold.pubsub_debug) 
            messages.debug(".. publish_result (2) has used NEW API on " + count + " records");
        manifold.raise_record_event(query.query_uuid, DONE);
        if (manifold.pubsub_debug) 
            messages.debug(".. publish_result (3) has used NEW API to say DONE");

        // OLD PLUGIN API BELOW
        /* Publish an update announce */
        var channel="/results/" + query.query_uuid + "/changed";
        if (manifold.pubsub_debug) 
            messages.debug(".. publish_result (4) OLD API on channel" + channel);

        $.publish(channel, [result, query]);

        if (manifold.pubsub_debug) 
            messages.debug(".. publish_result (5) END q=" + query.__repr());
    },

    /*!
     * Recursively publish result
     * \fn publish_result_rec(query, result)
     * \memberof Manifold
     * \param ManifoldQuery query Query which has received result
     * \param array result result corresponding to query
     *
     * Note: this function works on the analyzed query
     */
    publish_result_rec: function(query, result) {
        /* If the result is not unique, only publish the top query;
         * otherwise, publish the main object as well as subqueries
         * XXX how much recursive are we ?
         */
        if (manifold.pubsub_debug)
            messages.debug (">>>>> publish_result_rec " + query.object);
        if (manifold.query_expects_unique_result(query)) {
            /* Also publish subqueries */
            $.each(query.subqueries, function(object, subquery) {
                manifold.publish_result_rec(subquery, result[0][object]);
                /* TODO remove object from result */
            });
        }
        if (manifold.pubsub_debug) 
            messages.debug ("===== publish_result_rec " + query.object);

        manifold.publish_result(query, result);

        if (manifold.pubsub_debug) 
            messages.debug ("<<<<< publish_result_rec " + query.object);
    },

    setup_update_query: function(query, records) {
        // We don't prepare an update query if the result has more than 1 entry
        if (records.length != 1)
            return;
        var query_ext = manifold.query_store.find_query_ext(query.query_uuid);

        var record = records[0];

        var update_query_ext = query_ext.update_query_ext;
        var update_query = update_query_ext.query;
        var update_query_ext = query_ext.update_query_ext;
        var update_query_orig = query_ext.update_query_orig_ext.query;

        // Testing whether the result has subqueries (one level deep only)
        // iif the query has subqueries
        var count = 0;
        var obj = query.analyzed_query.subqueries;
        for (method in obj) {
            if (obj.hasOwnProperty(method)) {
                var key = manifold.metadata.get_key(method);
                if (!key)
                    continue;
                if (key.length > 1)
                    continue;
                key = key[0];
                var sq_keys = [];
                var subrecords = record[method];
                if (!subrecords)
                    continue
                $.each(subrecords, function (i, subrecord) {
                    sq_keys.push(subrecord[key]);
                });
                update_query.params[method] = sq_keys;
                update_query_orig.params[method] = sq_keys.slice();
                count++;
            }
        }

        if (count > 0) {
            update_query_ext.disabled = false;
            update_query_orig_ext.disabled = false;
        }
    },

    process_get_query_records: function(query, records) {
        this.setup_update_query(query, records);

        /* Publish full results */
        var tmp_query = manifold.find_query(query.query_uuid);
        manifold.publish_result_rec(tmp_query.analyzed_query, records);
    },

    /**
     * 
     * What we need to do when receiving results from an update query:
     * - differences between what we had, what we requested, and what we obtained
     *    . what we had : update_query_orig (simple fields and set fields managed differently)
     *    . what we requested : update_query
     *    . what we received : records
     * - raise appropriate events
     *
     * The normal process is that results similar to Get will be pushed in the
     * pubsub mechanism, thus repopulating everything while we only need
     * diff's. This means we need to move the publish functionalities in the
     * previous 'process_get_query_records' function.
     */
    process_update_query_records: function(query, records) {
        // First issue: we request everything, and not only what we modify, so will will have to ignore some fields
        var query_uuid        = query.query_uuid;
        var query_ext         = manifold.query_store.find_analyzed_query_ext(query_uuid);
        var update_query      = query_ext.main_query_ext.update_query_ext.query;
        var update_query_orig = query_ext.main_query_ext.update_query_orig_ext.query;
        
        // Since we update objects one at a time, we can get the first record
        var record = records[0];

        // Let's iterate over the object properties
        for (var field in record) {
            switch (this.get_type(record[field])) {
                case TYPE_VALUE:
                    // Did we ask for a change ?
                    var update_value = update_query[field];
                    if (!update_value)
                        // Not requested, if it has changed: OUT OF SYNC
                        // How we can know ?
                        // We assume it won't have changed
                        continue;

                    var result_value = record[field];
                    if (!result_value)
                        throw "Internal error";

                    data = {
                        request: FIELD_REQUEST_CHANGE,
                        key   : field,
                        value : update_value,
                        status: (update_value == result_value) ? FIELD_REQUEST_SUCCESS : FIELD_REQUEST_FAILURE,
                    }
                    manifold.raise_record_event(query_uuid, FIELD_STATE_CHANGED, data);

                    break;
                case TYPE_RECORD:
                    throw "Not implemented";
                    break;

                case TYPE_LIST_OF_VALUES:
                    // Same as list of records, but we don't have to extract keys
                    var result_keys  = record[field]
                    
                    // The rest of exactly the same (XXX factorize)
                    var update_keys  = update_query_orig.params[field];
                    var query_keys   = update_query.params[field];
                    var added_keys   = $.grep(query_keys, function (x) { return $.inArray(x, update_keys) == -1 });
                    var removed_keys = $.grep(update_keys, function (x) { return $.inArray(x, query_keys) == -1 });


                    $.each(added_keys, function(i, key) {
                        if ($.inArray(key, result_keys) == -1) {
                            data = {
                                request: FIELD_REQUEST_ADD,
                                key   : field,
                                value : key,
                                status: FIELD_REQUEST_FAILURE,
                            }
                        } else {
                            data = {
                                request: FIELD_REQUEST_ADD,
                                key   : field,
                                value : key,
                                status: FIELD_REQUEST_SUCCESS,
                            }
                        }
                        manifold.raise_record_event(query_uuid, FIELD_STATE_CHANGED, data);
                    });
                    $.each(removed_keys, function(i, key) {
                        if ($.inArray(key, result_keys) == -1) {
                            data = {
                                request: FIELD_REQUEST_REMOVE,
                                key   : field,
                                value : key,
                                status: FIELD_REQUEST_SUCCESS,
                            }
                        } else {
                            data = {
                                request: FIELD_REQUEST_REMOVE,
                                key   : field,
                                value : key,
                                status: FIELD_REQUEST_FAILURE,
                            }
                        }
                        manifold.raise_record_event(query_uuid, FIELD_STATE_CHANGED, data);
                    });


                    break;
                case TYPE_LIST_OF_RECORDS:
                    // example: slice.resource
                    //  - update_query_orig.params.resource = resources in slice before update
                    //  - update_query.params.resource = resource requested in slice
                    //  - keys from field = resources obtained
                    var key = manifold.metadata.get_key(field);
                    if (!key)
                        continue;
                    if (key.length > 1) {
                        throw "Not implemented";
                        continue;
                    }
                    key = key[0];

                    /* XXX should be modified for multiple keys */
                    var result_keys  = $.map(record[field], function(x) { return x[key]; });

                    var update_keys  = update_query_orig.params[field];
                    var query_keys   = update_query.params[field];
                    var added_keys   = $.grep(query_keys, function (x) { return $.inArray(x, update_keys) == -1 });
                    var removed_keys = $.grep(update_keys, function (x) { return $.inArray(x, query_keys) == -1 });


                    $.each(added_keys, function(i, key) {
                        if ($.inArray(key, result_keys) == -1) {
                            data = {
                                request: FIELD_REQUEST_ADD,
                                key   : field,
                                value : key,
                                status: FIELD_REQUEST_FAILURE,
                            }
                        } else {
                            data = {
                                request: FIELD_REQUEST_ADD,
                                key   : field,
                                value : key,
                                status: FIELD_REQUEST_SUCCESS,
                            }
                        }
                        manifold.raise_record_event(query_uuid, FIELD_STATE_CHANGED, data);
                    });
                    $.each(removed_keys, function(i, key) {
                        if ($.inArray(key, result_keys) == -1) {
                            data = {
                                request: FIELD_REQUEST_REMOVE,
                                key   : field,
                                value : key,
                                status: FIELD_REQUEST_SUCCESS,
                            }
                        } else {
                            data = {
                                request: FIELD_REQUEST_REMOVE,
                                key   : field,
                                value : key,
                                status: FIELD_REQUEST_FAILURE,
                            }
                        }
                        manifold.raise_record_event(query_uuid, FIELD_STATE_CHANGED, data);
                    });


                    break;
            }
        }
        
        // XXX Now we need to adapt 'update' and 'update_orig' queries as if we had done a get
        this.setup_update_query(query, records);
    },

    process_query_records: function(query, records) {
        if (query.action == 'get') {
            this.process_get_query_records(query, records);
        } else if (query.action == 'update') {
            this.process_update_query_records(query, records);
        }
    },

    // if set callback is provided it is called
    // most of the time publish_uuid will be query.query_uuid
    // however in some cases we wish to publish the result under a different uuid
    // e.g. an updater wants to publish its result as if from the original (get) query
    asynchroneous_success : function (data, query, publish_uuid, callback) {
        // xxx should have a nicer declaration of that enum in sync with the python code somehow
        
        var start = new Date();
        if (manifold.asynchroneous_debug)
            messages.debug(">>>>>>>>>> asynchroneous_success query.object=" + query.object);

        if (data.code == 2) { // ERROR
            // We need to make sense of error codes here
            alert("Your session has expired, please log in again");
            window.location="/logout/";
            if (manifold.asynchroneous_debug) {
                duration=new Date()-start;
                messages.debug ("<<<<<<<<<< asynchroneous_success " + query.object + " -- error returned - logging out " + duration + " ms");
            }
            return;
        }
        if (data.code == 1) { // WARNING
            messages.error("Some errors have been received from the manifold backend at " + MANIFOLD_URL + " [" + data.description + "]");
            // publish error code and text message on a separate channel for whoever is interested
            if (publish_uuid)
                $.publish("/results/" + publish_uuid + "/failed", [data.code, data.description] );

        }

        // If a callback has been specified, we redirect results to it 
        if (!!callback) { 
            callback(data); 
            if (manifold.asynchroneous_debug) {
                duration=new Date()-start;
                messages.debug ("<<<<<<<<<< asynchroneous_success " + query.object + " -- callback ended " + duration + " ms");
            }
            return; 
        }

        if (manifold.asynchroneous_debug) 
            messages.debug ("========== asynchroneous_success " + query.object + " -- before process_query_records [" + query.query_uuid +"]");

        // once everything is checked we can use the 'value' part of the manifoldresult
        var result=data.value;
        if (result) {
            /* Eventually update the content of related queries (update, etc) */
            this.process_query_records(query, result);

            /* Publish results: disabled here, done in the previous call */
            //tmp_query = manifold.find_query(query.query_uuid);
            //manifold.publish_result_rec(tmp_query.analyzed_query, result);
        }
        if (manifold.asynchroneous_debug) {
            duration=new Date()-start;
            messages.debug ("<<<<<<<<<< asynchroneous_success " + query.object + " -- done " + duration + " ms");
        }

    },

    /************************************************************************** 
     * Plugin API helpers
     **************************************************************************/ 

    raise_event_handler: function(type, query_uuid, event_type, value) {
	if (manifold.pubsub_debug)
	    messages.debug("raise_event_handler, quuid="+query_uuid+" type="+type+" event_type="+event_type);
        if ((type != 'query') && (type != 'record'))
            throw 'Incorrect type for manifold.raise_event()';
        // xxx we observe quite a lot of incoming calls with an undefined query_uuid
        // this should be fixed upstream in manifold I expect
        if (query_uuid === undefined) {
            messages.warning("undefined query in raise_event_handler");
            return;
        }

        // notify the change to objects that either listen to this channel specifically,
        // or to the wildcard channel
        var channels = [ manifold.get_channel(type, query_uuid), manifold.get_channel(type, '*') ];

        $.each(channels, function(i, channel) {
            if (value === undefined) {
		if (manifold.pubsub_debug) messages.debug("triggering [no value] on channel="+channel+" and event_type="+event_type);
                $('.pubsub').trigger(channel, [event_type]);
            } else {
		if (manifold.pubsub_debug) messages.debug("triggering [value="+value+"] on channel="+channel+" and event_type="+event_type);
                $('.pubsub').trigger(channel, [event_type, value]);
            }
        });
    },

    raise_query_event: function(query_uuid, event_type, value) {
        manifold.raise_event_handler('query', query_uuid, event_type, value);
    },

    raise_record_event: function(query_uuid, event_type, value) {
        manifold.raise_event_handler('record', query_uuid, event_type, value);
    },


    raise_event: function(query_uuid, event_type, value) {
        // Query uuid has been updated with the key of a new element
        query_ext    = manifold.query_store.find_analyzed_query_ext(query_uuid);
        query = query_ext.query;

        switch(event_type) {
            case FIELD_STATE_CHANGED:
                // value is an object (request, key, value, status)
                // update is only possible is the query is not pending, etc
                // SET_ADD is on a subquery, FIELD_STATE_CHANGED on the query itself
                // we should map SET_ADD on this...

                // 1. Update internal query store about the change in status

                // 2. Update the update query
                update_query      = query_ext.main_query_ext.update_query_ext.query;
                update_query_orig = query_ext.main_query_ext.update_query_orig_ext.query;

                switch(value.request) {
                    case FIELD_REQUEST_CHANGE:
                        if (update_query.params[value.key] === undefined)
                            update_query.params[value.key] = Array();
                        update_query.params[value.key] = value.value;
                        break;
                    case FIELD_REQUEST_ADD:
                        if ($.inArray(value.value, update_query_orig.params[value.key]) != -1)
                            value.request = FIELD_REQUEST_ADD_RESET;
                        if (update_query.params[value.key] === undefined)
                            update_query.params[value.key] = Array();
                        update_query.params[value.key].push(value.value);
                        break;
                    case FIELD_REQUEST_REMOVE:
                        if ($.inArray(value.value, update_query_orig.params[value.key]) == -1)
                            value.request = FIELD_REQUEST_REMOVE_RESET;

                        var arr = update_query.params[value.key];
                        arr = $.grep(arr, function(x) { return x != value.value; });
                        if (update_query.params[value.key] === undefined)
                            update_query.params[value.key] = Array();
                        update_query.params[value.key] = arr;

                        break;
                    case FIELD_REQUEST_ADD_RESET:
                    case FIELD_REQUEST_REMOVE_RESET:
                        // XXX We would need to keep track of the original query
                        throw "Not implemented";
                        break;
                }

                // 3. Inform others about the change
                // a) the main query...
                manifold.raise_record_event(query_uuid, event_type, value);

                // b) subqueries eventually (dot in the key)
                // Let's unfold 
                var path_array = value.key.split('.');
                var value_key = value.key.split('.');

                var cur_query = query;
                if (cur_query.analyzed_query)
                    cur_query = cur_query.analyzed_query;
                $.each(path_array, function(i, method) {
                    cur_query = cur_query.subqueries[method];
                    value_key.shift(); // XXX check that method is indeed shifted
                });
                value.key = value_key;

                manifold.raise_record_event(cur_query.query_uuid, event_type, value);

                // XXX make this DOT a global variable... could be '/'
                break;

            case SET_ADD:
            case SET_REMOVED:
    
                // update is only possible is the query is not pending, etc
                // CHECK status !

                // XXX we can only update subqueries of the main query. Check !
                // assert query_ext.parent_query == query_ext.main_query
                // old // update_query = query_ext.main_query_ext.update_query_ext.query;

                // This SET_ADD is called on a subquery, so we have to
                // recontruct the path of the key in the main_query
                // We then call FIELD_STATE_CHANGED which is the equivalent for the main query

                var path = "";
                var sq = query_ext;
                while (sq.parent_query_ext) {
                    if (path != "")
                        path = '.' + path;
                    path = sq.query.object + path;
                    sq = sq.parent_query_ext;
                }

                main_query = query_ext.main_query_ext.query;
                data = {
                    request: (event_type == SET_ADD) ? FIELD_REQUEST_ADD : FIELD_REQUEST_REMOVE,
                    key   : path,
                    value : value,
                    status: FIELD_REQUEST_PENDING,
                };
                this.raise_event(main_query.query_uuid, FIELD_STATE_CHANGED, data);

                // old //update_query.params[path].push(value);
                // old // console.log('Updated query params', update_query);
                // NOTE: update might modify the fields in Get
                // NOTE : we have to modify all child queries
                // NOTE : parts of a query might not be started (eg slice.measurements, how to handle ?)

                // if everything is done right, update_query should not be null. 
                // It is updated when we received results from the get query
                // object = the same as get
                // filter = key : update a single object for now
                // fields = the same as get
                manifold.raise_query_event(query_uuid, event_type, value);

                break;

            case RUN_UPDATE:
                manifold.run_query(query_ext.main_query_ext.update_query_ext.query);
                break;

            case FILTER_ADDED: 
// Thierry - this is probably wrong but intended as a hotfix 
// http://trac.myslice.info/ticket/32
//                manifold.raise_query_event(query_uuid, event_type, value);
                break;
            case FILTER_REMOVED:
                manifold.raise_query_event(query_uuid, event_type, value);
                break;
            case FIELD_ADDED:
                main_query = query_ext.main_query_ext.query;
                main_update_query = query_ext.main_query_ext.update_query;
                query.select(value);

                // Here we need the full path through all subqueries
                path = ""
                // XXX We might need the query name in the QueryExt structure
                main_query.select(value);

                // XXX When is an update query associated ?
                // XXX main_update_query.select(value);

                manifold.raise_query_event(query_uuid, event_type, value);
                break;

            case FIELD_REMOVED:
                query = query_ext.query;
                main_query = query_ext.main_query_ext.query;
                main_update_query = query_ext.main_query_ext.update_query;
                query.unselect(value);
                main_query.unselect(value);

                // We need to inform about changes in these queries to the respective plugins
                // Note: query & main_query have the same UUID
                manifold.raise_query_event(query_uuid, event_type, value);
                break;
        }
        // We need to inform about changes in these queries to the respective plugins
        // Note: query, main_query & update_query have the same UUID
        manifold.raise_query_event(query_uuid, event_type, value);
        // We are targeting the same object with get and update
        // The notion of query is bad, we should have a notion of destination, and issue queries on the destination
        // NOTE: Editing a subquery == editing a local view on the destination

        // XXX We might need to run the new query again and manage the plugins in the meantime with spinners...
        // For the time being, we will collect all columns during the first query
    },

    /* Publish/subscribe channels for internal use */
    get_channel: function(type, query_uuid) {
        if ((type !== 'query') && (type != 'record'))
            return null;
        return '/' + type + '/' + query_uuid;
    },

}; // manifold object
/* ------------------------------------------------------------ */

(function($) {

    // OLD PLUGIN API: extend jQuery/$ with pubsub capabilities
    // https://gist.github.com/661855
    var o = $({});
    $.subscribe = function( channel, selector, data, fn) {
      /* borrowed from jQuery */
      if ( data == null && fn == null ) {
          // ( channel, fn )
          fn = selector;
          data = selector = undefined;
      } else if ( fn == null ) {
          if ( typeof selector === "string" ) {
              // ( channel, selector, fn )
              fn = data;
              data = undefined;
          } else {
              // ( channel, data, fn )
              fn = data;
              data = selector;
              selector = undefined;
          }
      }
      /* </ugly> */
  
      /* We use an indirection function that will clone the object passed in
       * parameter to the subscribe callback 
       * 
       * FIXME currently we only clone query objects which are the only ones
       * supported and editable, we might have the same issue with results but
       * the page load time will be severely affected...
       */
      o.on.apply(o, [channel, selector, data, function() { 
          for(i = 1; i < arguments.length; i++) {
              if ( arguments[i].constructor.name == 'ManifoldQuery' )
                  arguments[i] = arguments[i].clone();
          }
          fn.apply(o, arguments);
      }]);
    };
  
    $.unsubscribe = function() {
      o.off.apply(o, arguments);
    };
  
    $.publish = function() {
      o.trigger.apply(o, arguments);
    };
  
}(jQuery));

/* ------------------------------------------------------------ */

//http://stackoverflow.com/questions/5100539/django-csrf-check-failing-with-an-ajax-post-request
//make sure to expose csrf in our outcoming ajax/post requests
$.ajaxSetup({ 
     beforeSend: function(xhr, settings) {
         function getCookie(name) {
             var cookieValue = null;
             if (document.cookie && document.cookie != '') {
                 var cookies = document.cookie.split(';');
                 for (var i = 0; i < cookies.length; i++) {
                     var cookie = jQuery.trim(cookies[i]);
                     // Does this cookie string begin with the name we want?
                 if (cookie.substring(0, name.length + 1) == (name + '=')) {
                     cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                     break;
                 }
             }
         }
         return cookieValue;
         }
         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             // Only send the token to relative URLs i.e. locally.
             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         }
     } 
});
