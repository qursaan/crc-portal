(function($){
  var SensLabMap = Plugin.extend({
    init: function(options, element) {
	this.classname="senslabmap";
      this._super(options, element);
      
      this.elmt().on('show', this, this.on_show);

      var query = manifold.query_store.find_analyzed_query(options.query_uuid);
      this.method = query.object;
      this.key = manifold.metadata.get_key(this.method);
      
      /* Setup query and record handlers */
      this.listen_query(options.query_uuid);
      this.listen_query(options.query_all_uuid, 'all');

      this.sites = [];
      this.nodes = {};
    },
    
    on_show: function(e) {
      e.data.refresh();
    },
    
    on_all_new_record: function(node) {
      Senslab.normalize(node);
      if (node.normalized) {
        var site = node.site;
        if ($.inArray(site, this.sites) == -1) {
          this.sites.push(site);
          this.nodes[site] = [];
        }
        this.nodes[site].push(node);
      } else {
// xxx would need a smarter way to report these only on nodes that deserve it
// these messages are all over the place in a PL setup and tend to hide helpful signal
//        console.warn("node has no site:");
//        console.warn(node);
      }
    },
    
    on_all_query_done: function() {
      var uuid = this.options.query_uuid;
      var key = this.key
      
      Senslab.createMaps($("#maps-container"), this.sites, this.nodes);
      Senslab.notify = function(node) {
        manifold.raise_event(uuid, node.selected ? SET_ADD : SET_REMOVED, node[key]);
      }
    }
  });
  $.plugin('SensLabMap', SensLabMap);
})(jQuery);
