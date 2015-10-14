function ManifoldQuery(action, object, timestamp, filters, params, fields, unique, query_uuid, aq, sq) {  
    // get, update, delete, create
    var action;
    // slice, user, network... 
    var object; 
    // timestamp, now, latest(cache) : date of the results queried    
    var timestamp;
    // key(field),op(=<>),value
    var filters;
    // todo
    var params;
    // hostname, ip,... 
    var fields;
    // 0,1 : list of element of an object or single object  
    var unique;
    // query_uuid : unique identifier of a query
    var query_uuid;
    // Query : root query (no sub-Query)
    var analyzed_query;
    // {} : Assoc Table of sub-queries ["resources"->subQ1, "users"->subQ2]
    var subqueries;

/*-------------------------------------------------------------
              Query properties are SQL like : 
---------------------------------------------------------------
SELECT fields FROM object WHERE filter;
UPDATE object SET field=value WHERE filter; / returns SELECT 
DELETE FROM object WHERE filter
INSERT INTO object VALUES(field=value)
-------------------------------------------------------------*/
    
    this.__repr = function () {
	res  = "ManifoldQuery ";
//	res += " id=" + this.query_uuid;
	res += " a=" + this.action;
	res += " o=" + this.object;
	res += " ts=" + this.timestamp;
	res += " flts=" + this.filters;
	res += " flds=" + this.fields;
	res += " prms=" + this.params;
	return res;
    }	

    this.clone = function() {
        // 
        var q = new ManifoldQuery();
        q.action     = this.action;
        q.object     = this.object;
        q.timestamp  = this.timestamp;
        q.filters    = this.filters.slice();
        q.fields     = this.fields.slice();
        q.query_uuid = this.query_uuid;

        if (this.analyzed_query)
            q.analyzed_query = this.analyzed_query.clone();
        else
            q.analyzed_query = null;

        if (this.subqueries) {
            q.subqueries = {}
            for (method in this.subqueries)
                q.subqueries[method] = this.subqueries[method].clone();
        }

        // deep extend not working for custom objects
        // $.extend(true, q, this);
        return q;
    }

    this.add_filter = function(key, op, value) {
        this.filters.push(new Array(key, op, value));
    }
    this.update_filter = function(key, op, value) {
        // Need to be improved...
        // remove all occurrences of key if operation is not defined
        if(!op){
            this.filters = jQuery.grep(this.filters, function(val, i) {
                return val[0] != key; 
            });
        // Else remove the key+op filters
        }else{
            this.filters = jQuery.grep(this.filters, function(val, i) {return (val[0] != key || val[1] != op);});
        }
        this.filters.push(new Array(key, op, value));
    }

    this.remove_filter = function (key,op,value) {
        // if operator is null then remove all occurences of this key
        if(!op){
            this.filters = jQuery.grep(this.filters, function(val, i) { 
                return val[0] != key; 
            });
        }else{
            this.filters = jQuery.grep(this.filters, function(val, i) {return (val[0] != key || val[1] != op);});
        }
    }

    // FIXME These functions computing diff's between queries are meant to be shared
    this.diff_fields = function(otherQuery) {
        var f1 = this.fields;
        var f2 = otherQuery.fields;

        /* added elements are the ones in f2 not in f1 */
        var added   = jQuery.grep(f2, function (x) { return jQuery.inArray(x, f1) == -1 }); 
        /* removed elements are the ones in f1 not in f2 */
        var removed = jQuery.grep(f1, function (x) { return jQuery.inArray(x, f2) == -1 }); 
        
        return {'added':added, 'removed':removed};
    }

    // FIXME Modify filter to filters
    this.diff_filter = function(otherQuery) {
        var f1 = this.filters;
        var f2 = otherQuery.filters;
        
        /* added elements are the ones in f2 not in f1 */
        var added   = jQuery.grep(f2, function (x) { return !arrayInArray(x, f1)}); 
        /* removed elements are the ones in f1 not in f2 */
        var removed = jQuery.grep(f1, function (x) { return !arrayInArray(x, f2)}); 
        
        return {'added':added, 'removed':removed};
    } 

    // Callaback received 3 parameters: query, data, parent_query
    this.iter_subqueries = function(callback, data)
    {
        rec = function(query, callback, data, parent_query) {
            callback(query, data, parent_query);
            jQuery.each(query.subqueries, function(object, subquery) {
                rec(subquery, callback, data, query);
            });
        };

        if (this.analyzed_query !== undefined)
            query = this.analyzed_query;
        else
            query = this;

        rec(query, callback, data, null);
    }

    this.select = function(field)
    {
        this.fields.push(field);
    }

    this.unselect = function(field)
    {   
        this.fields = $.grep(this.fields, function(x) { return x != field; });
    }

// we send queries as a json string now 
//    this.as_POST = function() {
//        return {'action': this.action, 'object': this.object, 'timestamp': this.timestamp,
//		'filters': this.filters, 'params': this.params, 'fields': this.fields};
//    }
    this.analyze_subqueries = function() {
        /* adapted from the PHP function in com_tophat/includes/query.php */
        var q = new ManifoldQuery();
        q.query_uuid = this.query_uuid;
        q.action = this.action;
        q.object = this.object;
        q.timestamp = this.timestamp;

        /* Filters */
        jQuery.each(this.filters, function(i, filter) {
            var k = filter[0];
            var op = filter[1];
            var v = filter[2];
            var pos = k.indexOf('.');
            if (pos != -1) {
                var object = k.substr(0, pos);
                var field = k.substr(pos+1);
                if (!q.subqueries[object]) {
                    q.subqueries[object] = new ManifoldQuery();
                    q.subqueries[object].action = q.action;
                    q.subqueries[object].object = object;
                    q.subqueries[object].timestamp = q.timestamp;
                }
                q.subqueries[object].filters.push(Array(field, op, v));
            } else {
                q.filters.push(filter);
            }
        });

        /* Params */
        jQuery.each(this.params, function(param, value) {
            var pos = param.indexOf('.');
            if (pos != -1) {
                var object = param.substr(0, pos);
                var field = param.substr(pos+1);
                if (!q.subqueries[object]) {
                    q.subqueries[object] = new ManifoldQuery();
                    q.subqueries[object].action = q.action;
                    q.subqueries[object].object = object;
                    q.subqueries[object].timestamp = q.timestamp;
                }
                q.subqueries[object].params[field] = value;
            } else {
                q.params[field] = value;
            }
        });

        /* Fields */
        jQuery.each(this.fields, function(i, v) {
            var pos = v.indexOf('.');
            if (pos != -1) {
                var object = v.substr(0, pos);
                var field = v.substr(pos+1);
                if (!q.subqueries[object]) {
                    q.subqueries[object] = new ManifoldQuery();
                    q.subqueries[object].action = q.action;
                    q.subqueries[object].object = object;
                    q.subqueries[object].timestamp = q.timestamp;
                }
                q.subqueries[object].fields.push(field);
            } else {
                q.fields.push(v);
            }
        });
        this.analyzed_query = q;
    }
 
    /* constructor */
    if (typeof action == "undefined")
        this.action = "get";
    else
        this.action = action;
    
    if (typeof object == "undefined")
        this.object = null;
    else
        this.object = object;

    if (typeof timestamp == "undefined")
        this.timestamp = "now";
    else
        this.timestamp = timestamp;

    if (typeof filters == "undefined")
        this.filters = [];
    else
        this.filters = filters;

    if (typeof params == "undefined")
        this.params = {};
    else
        this.params = params;

    if (typeof fields == "undefined")
        this.fields = [];
    else
        this.fields = fields;

    if (typeof unique == "undefined")
        this.unique = false;
    else
        this.unique = unique;

    this.query_uuid = query_uuid;

    if (typeof aq == "undefined")
        this.analyzed_query = null;
    else
        this.analyzed_query = aq;

    if (typeof sq == "undefined")
        this.subqueries = {};
    else
        this.subqueries = sq;
}  
