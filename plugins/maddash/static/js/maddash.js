/**
 * MyPlugin:    MadDash
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
var SVG='http://www.w3.org/2000/svg';
var instance = this;
var colorscale = d3.scale.category10().range(["green", "yellow", "red", "orange", "gray"]);

/* XXX */
/**
 * Class: MaDDashGrid
 * Description: Widget that displays grid of checks. Uses
 *   d3 and jQuery to draw the grid.
 * Parameters:
 *      parentId: id string of the container element
 *      legendId: id string of the legend element
 */

(function($){

    var MadDash = Plugin.extend({

        /** XXX to check
         * @brief Plugin constructor
         * @param options : an associative array of setting values
         * @param element : 
         * @return : a jQuery collection of objects on which the plugin is
         *     applied, which allows to maintain chainability of calls
         */
        init: function(options, element) {
            // Call the parent constructor, see FAQ when forgotten
	    this.classname="maddash";
            this._super(options, element);


            /* Member variables */
            //this.canvas = this.id('canvas');
            this._legend = this.id('legend'); //legendId;
            this._labels = Array(
                'un', 'deux', 'trois', 'quatre'
            )

            this._cellsize = 13;
            this._cellpadding = 2;
            this._text_block_size = 130;

            this._map_elements = {};
            this._num_elements = 0;

            this._max_width_elements  = 50;
            this._max_height_elements = 30;

            this._buffer_key_list = new Buffer(this._process_key_list, this);
            this._buffer_records  = new Buffer(this._process_records, this);

            /* Pointers */
            this._canvas       = d3.select("#" + options.plugin_uuid + '__canvas')
                .style("width", this._max_width_elements * (this._cellsize + 2*this._cellpadding) + 110 + this._text_block_size)
                .style("height", this._max_height_elements * (this._cellsize + 2*this._cellpadding) + 110 + this._text_block_size)
            this._left_element = null;
            this._top_element  = null;
            this._row_element  = Array();
            this._grid_element = null;
            


            /* Buffered input */
//            this._buffer = Array();
//            this._update_interval = 1000; /* ms to wait, 1000 = 1 second */
//            setInterval(function(){
//                var tmp = buffer; /* Switch the buffer out quickly so we aren't scrambled 
//                                     if you addToBuffer in the middle of this */
//                buffer = Array();
//                $thisdocument.getElementById(htmlId).innerHTML = tmp.join("");
//                //document.getElementById(htmlId).innerHTML = tmp.join("");
//            }, wait);
//
//addToBuffer = function(html){
//    buffer.push(html);
//};

            /* Plugin events */

            /* Setup query and record handlers */

            // Explain this will allow query events to be handled
            // What happens when we don't define some events ?
            // Some can be less efficient
            this.listen_query(options.query_uuid);
            this.listen_query(options.query_all_uuid, 'all');

            /* GUI setup and event binding */
            // call function
            this._display_legends();
            this._init_top();
            this._init_left();
            this._init_grid();
            //this._test();

        },

        _test: function()
        {
            data = {
                "name":"OWAMP",
                "statusLabels":[
                    "Loss is 0",null,"Loss is greater than 0","Unable to retrieve data","Check has not yet run"
                ],
                "lastUpdateTime":1385376538,
                "rows":[
                    {"name":"200.128.79.100","uri":"/maddash/grids/OWAMP/200.128.79.100"},
                    {"name":"ata.larc.usp.br","uri":"/maddash/grids/OWAMP/ata.larc.usp.br"},
                    {"name":"mon-lt.fibre.cin.ufpe.br","uri":"/maddash/grids/OWAMP/mon-lt.fibre.cin.ufpe.br"}
                ],
                "columnNames":[
                    "200.128.79.100","ata.larc.usp.br","mon-lt.fibre.cin.ufpe.br"
                ],
                "checkNames": ["Loss","Loss Reverse"],
                "grid": [
                    [
                        /* First line */
                        null,
                        [{
                            "message":" No one-way delay data returned for direction where src=200.128.79.100 dst=ata.larc.usp.br",
                            "status":3,
                            "prevCheckTime":1385376238,
                            "uri":"/maddash/grids/OWAMP/200.128.79.100/ata.larc.usp.br/Loss"
                        },{
                            "message":" No one-way delay data returned for direction where src=ata.larc.usp.br dst=200.128.79.100",
                            "status":2,"prevCheckTime":1385376178,
                            "uri":"/maddash/grids/OWAMP/200.128.79.100/ata.larc.usp.br/Loss+Reverse"
                        }],[{
                            "message":" Loss is 100.000% ",
                            "status":2,
                            "prevCheckTime":1385374877,
                            "uri":"/maddash/grids/OWAMP/200.128.79.100/mon-lt.fibre.cin.ufpe.br/Loss"
                        },{
                            "message":" Loss is 100.000% ",
                            "status":2,
                            "prevCheckTime":1385375498,
                            "uri":"/maddash/grids/OWAMP/200.128.79.100/mon-lt.fibre.cin.ufpe.br/Loss+Reverse"
                        }]
                    ],[
                        /* Second line */
                        [{
                            "message":" Unable to contact MA. Please check that the MA is running and the URL is correct.",
                            "status":3,
                            "prevCheckTime":1385376037,
                            "uri":"/maddash/grids/OWAMP/ata.larc.usp.br/200.128.79.100/Loss"
                        }, {
                            "message":" Unable to contact MA. Please check that the MA is running and the URL is correct.",
                            "status":3,
                            "prevCheckTime":1385376117,
                            "uri":"/maddash/grids/OWAMP/ata.larc.usp.br/200.128.79.100/Loss+Reverse"
                        }],
                        null,
                        [{
                            "message":" Unable to contact MA. Please check that the MA is running and the URL is correct.",
                            "status":3,
                            "prevCheckTime":1385376117,
                            "uri":"/maddash/grids/OWAMP/ata.larc.usp.br/mon-lt.fibre.cin.ufpe.br/Loss"
                        }, {
                            "message":" Unable to contact MA. Please check that the MA is running and the URL is correct.",
                            "status":3,
                            "prevCheckTime":1385376017,
                            "uri":"/maddash/grids/OWAMP/ata.larc.usp.br/mon-lt.fibre.cin.ufpe.br/Loss+Reverse"
                        }]
                    ],[
                        /* Third line */
                        [{
                            "message":" Loss is 100.000% ",
                            "status":2,
                            "prevCheckTime":1385376478,
                            "uri":"/maddash/grids/OWAMP/mon-lt.fibre.cin.ufpe.br/200.128.79.100/Loss"
                        },{
                            "message":" Loss is 100.000% ",
                            "status":2,
                            "prevCheckTime":1385375958,
                            "uri":"/maddash/grids/OWAMP/mon-lt.fibre.cin.ufpe.br/200.128.79.100/Loss+Reverse"
                        }], [{
                            "message":" No one-way delay data returned for direction where src=mon-lt.fibre.cin.ufpe.br dst=ata.larc.usp.br",
                            "status":3,
                            "prevCheckTime":1385376538,
                            "uri":"/maddash/grids/OWAMP/mon-lt.fibre.cin.ufpe.br/ata.larc.usp.br/Loss"
                        },{
                            "message":" No one-way delay data returned for direction where src=ata.larc.usp.br dst=mon-lt.fibre.cin.ufpe.br",
                            "status":3,
                            "prevCheckTime":1385376358,
                            "uri":"/maddash/grids/OWAMP/mon-lt.fibre.cin.ufpe.br/ata.larc.usp.br/Loss+Reverse"
                        }],
                        null
                    ]
                ]
            }
            this._render(data);
        },

        /* ------------------------------------------------------------------ */
        /* Accessors                                                          */
        /* ------------------------------------------------------------------ */

        setClickHandler: function(f)
        {
            this._handleClick = f;
        },

        setCellSize: function(value)
        {
            this._cellSize = value;
        },

        setCellPadding: function(value)
        {
            this._cellPadding = value;
        },

        setTextBlockSize: function(value)
        {
            this._textBlockSize = value;
        },


        

        /* PLUGIN EVENTS */
        // on_show like in querytable


        /* GUI EVENTS */

        // a function to bind events here: click change
        // how to raise manifold events


        /* GUI MANIPULATION */

        /* XXX */


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
        on_all_new_record: function(record)
        {
            var key_value = record['hrn'];
            if (!(this._map_elements.hasOwnProperty(key_value))) {
                /* Add the key_value to the buffer to be drawn */
                this._buffer_key_list.add(key_value);
                /* Assign coordinates */
                this._map_elements[key_value] = this._num_elements++;
            }
            /* Add the record to the buffer to be drawn */
            this._buffer_records.add(record);
        },

        /* INTERNAL FUNCTIONS */

        _render: function(data)
        {
            //TODO: Set title
            //d3.select("#dashboard_name").html(dashboard.name + " Dashboard");
            // XXX OLD XXX d3.select("#" + this.parent).html("");
            //this.elmt().html('')

            this.display_component(data);
        },

        _init_left: function()
        {
            var self = this;
            this._left_element = this._canvas.append("div")
              .attr("class", "gleft")
                .style("overflow-y", "scroll")
                .style("height", "400px")
              .append("svg:svg")
                .attr("width", self._text_block_size)
                .attr("height", self._max_height_elements * (self._cellsize + 2*self._cellpadding) + 1000)

        },

        _process_left: function(key_list)
        {
            var self = this;

            this._left_element = this._left_element
              .selectAll(".rname")
                .data(key_list)
                .enter()
                  .append("g")
                  .attr("class", function(d,i){return "grow" + i})
                  .attr("transform", function(d,i){return "translate(0,"+(i*(self._cellsize+2*self._cellpadding))+")"})
      
            this._left_element.append("svg:rect")
              .attr("class", function(d,i){return "grow" + i})
              .attr("x",0).attr("y",0)
              .attr("width",this._text_block_size).attr("height",(this._cellsize+2*this._cellpadding))
      
            this._left_element.append("svg:text")
              .attr("class", "gtext")
              .attr("transform", "translate("+ (this._text_block_size-5) +",0)")
              .text(function(d,i){return d}) //strdata.rows[i].name})
              .attr("text-anchor", "end")
              .attr("dy", "1.1em")

            // XXX Let's generate fake records to create all rows
            var records = Array();
            for(var i = 0; i < key_list.length; i++) {
                for(var j = 0; j < key_list.length; j++) {
                    records.push({
                        'source': key_list[i],
                        'destination': key_list[j],
                        'value': Math.floor(Math.random()*4) /* 0 1 2 3 */
                    });
                }
            }

            // Create the rows
            this._row_element = this._grid_element.selectAll(".grow")
              .data(key_list)
              .enter()
                .append("div")
                .attr("class", function(d,i){return "grow grow" + i})
                .style("width", "100%")
                .style("z-index", 1000)
                // jordan
                .style('position', 'absolute')
/*
            var cells = this._row_element.selectAll('.gcell')
                  .data(records) //function(d,r){ return d.map(function(d,i){ return {celldata:d, row:r}}) }, function(d) { return d['source'] + '--' + d['destination']; })
                  .enter()
                    .append("div")
                    .attr("class", "gcell")
                    .style("height", self._cellsize +"px")
                    .style("width", self._cellsize +"px")
                    .style("margin", (self._cellpadding) +"px")
          
                    .on("mouseover", function(d,i){
                      selected_row = d.row; // We could find the row from the _map_elements
                      selected_col = i;
                      if(d.celldata){
                        d3.select(this).style("margin", (self._cellpadding-1) +"px");
                        d3.select(this).classed("shadow", true);
                      }
                      this._canvas.selectAll(".gcol"+ i).classed("gactive", true);
                      this._canvas.selectAll(".grow"+ d.row).classed("gactive", true);
                    })
                    .on("mouseout", function(d,i){
                      // d3.select(this).classed("shadow", false);
                      // d3.select(this).style("background-color", color.brighter());
                      d3.select(this).style("margin", (self._cellpadding) +"px");
                      d3.select(this).classed("shadow", false);
                      this._canvas.selectAll(".gcol"+ i).classed("gactive", false);
                      this._canvas.selectAll(".grow"+ d.row).classed("gactive", false);
                    })
*/
        },

        _init_top: function()
        {
            var self = this;
            this._top_element = this._canvas.append("div")
                .attr("class", "gtop")
                .style("margin-left", self._text_block_size + "px")
                .style("float", "left")
                .style("overflow-x", "scroll")
                .style("width", "960px")
                .append("svg:svg")
                    .attr("height", self._text_block_size)
                    .attr("width", self._max_width_elements * (self._cellsize + 2*self._cellpadding) + 90 + 1000)

        },


        _process_top: function(key_list)
        {
            var self = this;

            this._top_element = this._top_element
                .selectAll(".rname")
                    .data(key_list)
                    .enter()
                        .append("g")
                        .attr("class", function(d,i){return "gcol" + i})
                        .attr("transform", function(d,i){ return "translate("+(i*(self._cellsize+2*self._cellpadding))+",0)"})

            this._top_element.append("svg:rect")
                .attr("class", function(d,i){return "gcol" + i})
                .attr("x",0).attr("y",0)
                .attr("transform", "rotate(45,0,"+ self._text_block_size +") translate (-0.5,3)")
                .attr("height",self._text_block_size).attr("width",(self._cellsize+self._cellpadding))
                //.attr("transform", "rotate(35,"+ (this._cellsize+this._cellpadding)/2  + "," + this._text_block_size/2 + ")")


            this._top_element.append("svg:text")
                .attr("class", "gtext")
                .attr("text-anchor", "start")
                .attr("dy", "1.5em")
                .attr("dx", "1em")
                .attr("transform", "rotate(-45,0,"+ self._text_block_size +")  translate(0,"+ (self._text_block_size-5) + ")")
                .text(function(d,i){return d})

            // Create the columns... 
            var cols = this._grid_element.selectAll(".gcol")
              .data(key_list)
              .enter()
                .append("div")
                .attr("class", function(d,i){return "gcol gcol" + i})
                .style("width", (self._cellsize+2*self._cellpadding) + "px")
                .style("height", "100%")
                .style("left", function(d,i){return (i*(self._cellsize+2*self._cellpadding)) + "px"})
        },

        _process_key_list: function()
        {
            console.log("process key list");
            var key_list = this._buffer_key_list.get();
            this._process_top(key_list);
            this._process_left(key_list);
            console.log("process key list done");
        },

        _display_legends: function()
        {
            // Color scale = the number of different statuses
            colorscale.domain(d3.range(0, this._labels.length));

            // Labels
            var legendsdata = this._labels
                .map(function(d,i){ return {label:d, color:colorscale(i)} })
                //.filter(function(d,i){return d.label === null ? false : true})

            // Clear and redraw legend
            d3.select("#"+this._legend).html("")

            var legends = d3.select("#"+this._legend)
                .selectAll(".legend")
                .data(legendsdata)
                .enter()
                .append("div").attr("class", "legend");
            legends.append("div")
                .attr("class", "lsymbol")
                .style("background", function(d,i){return d.color})
                .style("display", function(d,i){return d.label === null ? "none" : "block"})
            legends.append("div")
                .attr("class", "ltext")
                .text(function(d,i){return d.label})
                .style("display", function(d,i){return d.label === null ? "none" : "block"})
        },

        _init_grid: function()
        {
            this._grid_element = this._canvas
                .style("width", this._ncols * (this._cellsize + 2*this._cellpadding) + 110 + this._text_block_size)
                .append("div")
                    .attr("class", "ggrid")
                    // jordan
                    .style('top', '165px')
                    .style('left', '145px')
                    .style('float', 'none')
                    .style('width', '2000px')
                    .style('height', '1000px')
            
        },

        _process_records: function()
        {
            var self = this;
            var records = this._buffer_records.get();
            console.log("processing records");

            // XXX Let's generate fake records instead... NxN
            var _records = Array();
            for(var i = 0; i < records.length; i++) {
                for(var j = 0; j < records.length; j++) {
                    if (Math.random() < 0.2) { /* one out of 5 */
                        _records.push({
                            'source': records[i]['hrn'],
                            'destination': records[j]['hrn'],
                            'value': Math.floor(Math.random()*4) /* 0 1 2 3 */
                        })
                    }
                }
            }

            //

            // Rows and columns have been created

            var color = "";
            var selected_row = 0;
            var selected_col = 0;
            var cells = this._row_element.selectAll(".gcell")
              /* Not sure to understand this part of the code */
              //uses data.grid initially... this is not good anymore
              .data(_records, function(d) { return d['source'] + '--' + d['destination']; })
              .style("background", function(d,i){
                return colorscale(parseInt(d.value));
              })

            // Associate a tooltip to each cell thanks to tipsy
            /*
            this.elmt().find(".gcell").each(function(i,d){
              var data = d3.select(this).data()[0];
              if(data.celldata!=null){
                var html = "<div class='tooltip'><div class='top-tip'>" + (data.celldata[0]? data.celldata[0].message : "") + "</div><div class='bottom-tip'>" + (data.celldata[1]? data.celldata[1].message : "") + "</div></div>";
                $(this).tipsy({
                  html :true,
                  opacity: 0.9,
                  title : function(){
                  return html
                }})
              }
            })
            */
      
            // This seems to create the coloured subcells
            var temp = cells.selectAll(".gsubcell")
              .data(function(d,i){return d.celldata===null? [] : d.celldata })
              .enter()
                .append("div");
            temp
              .style("height", this._cellsize/2 +"px")
              .style("background", function(d,i){
                return colorscale(parseInt(d.status));
              })
              .on("click", function(d,i){ //CHANGE FROM PORTAL
                  var that = this;
                  if(d!=null && d.uri!=null && self.handleClick != null){
                    self.handleClick(d);
                  }
                })
            console.log("processing records done");
        },

        display_component: function(data) 
        {
            this._display_grid_container(data);
        },

        _handleClick: function(d)
        {
            var uri = d.uri;
            $.getJSON(uri, function(data) {
                    var href = data['history'][0].returnParams.graphUrl.replace("https", "http");
                     window.open( href, "Graph", "menubar=0,location=0,height=700,width=700" );
             })

        }


    });

    /* Plugin registration */
    $.plugin('MadDash', MadDash);

    // TODO Here use cases for instanciating plugins in different ways like in the pastie.

})(jQuery);
