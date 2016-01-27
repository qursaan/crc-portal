// Escape special characters in jQuery Selector
function escape_id( myid ) {
    return "#" + myid.replace( /(:|\.|\[|\])/g, "\\$1" );
}

function getKeySplitId(id,separator){
    // id of elements must respect this rule
    // split_id[0] = plugin_uuid
    // split_id[1] = element
    // split_id[2] = field or key
    
    var split_id = id.split(separator);
    var key = split_id[2];
    
    return key;
}

// Adding startsWith & endsWith to the string prototype
if ( typeof String.prototype.startsWith != 'function' ) {
  String.prototype.startsWith = function( str ) {
    return this.substring( 0, str.length ) === str;
  }
};

if ( typeof String.prototype.endsWith != 'function' ) {
  String.prototype.endsWith = function( str ) {
    return this.substring( this.length - str.length, this.length ) === str;
  }
};
// http://stackoverflow.com/questions/646628/javascript-startswith

function arrays_equal(a,b) { return !(a<b || b<a); }

function arrayInArray(elt,tab){
    var flag=false;
    jQuery.each(tab, function(i,x){
        if(arrays_equal(x,elt)){flag=true;return;}            
    });
    return flag;
}

jQuery.fn.spin = function(opts) {
  this.each(function() {
    var $this = jQuery(this),
        data = $this.data();

    if (data.spinner) {
      data.spinner.stop();
      delete data.spinner;
    }
    if (opts !== false) {
      data.spinner = new Spinner(jQuery.extend({color: $this.css('color')}, opts)).spin(this);
    }
  });
  return this;
};

// FROM Triptych : http://stackoverflow.com/users/43089/triptych
// http://stackoverflow.com/questions/979256/how-to-sort-an-array-of-javascript-objects
// data.sort(sort_by('city', false, function(a){return a.toUpperCase()}));
var sort_by = function(field, reverse, primer){

   var key = function (x) {return primer ? primer(x[field]) : x[field]};
   //var key = primer ? function (x) { return primer(x[field]); } : function (x) { return x[field]; }
   
   return function (a,b) {
       var A = key(a), B = key(b);
       return (A < B ? -1 : (A > B ? 1 : 0)) * [1,-1][+!!reverse];
       //return ((A < B) ? -1 :
       //        (A > B) ? +1 : 0)) * [-1,1][+!!reverse];                  
   }
}
