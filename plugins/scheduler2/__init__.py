from unfold.plugin import Plugin
import datetime
from datetime import timedelta

class Scheduler2 (Plugin):


    def __init__ (self, query, query_all_resources, query_lease = None, **settings):
        Plugin.__init__ (self, **settings)
        
        self.query=query
        self.query_all_resources = query_all_resources
        self.query_all_resources_uuid = query_all_resources.query_uuid
        self.query_lease = query_lease
        query_lease.query_uuid if query_lease else None

        #granularity in minutes
        granularity = 10
        #self.time_slots = []
        self.time_slots = self.createTimeSlots(granularity)
        self.nodes = [
                        ['Grid Nodes' , ['node016', 'node017', 'node018', 'node019', 'node020', 'node021',  'node029', 'node030', 'node031','node031','node031','node031','node031','node031','node031','node031','node031','node031','node031','node031','node031','node031','node031','node031','node031','node031','node031','node031','node031','node031','node031','node031','node031','node031','node031','node031','node031','node031','node031','node031','node031','node031','node031','node031','node031','node031','node031','node031','node031','node031','node031','node031','node031','node031','node031','node031','node031','node031','node031','node031','node031','node031','node031','node031','node031','node031','node031','node031',]],
                        ['Other Nodes' , ['node022', 'node023', 'node024','node025', 'node026', 'node027', 'node028',]]
                    ]

    def template_file (self):
        return "scheduler.html"

    def requirements (self):
        reqs = {
            'js_files' : [
                'js/scheduler2.js',
                'js/slider/jquery-ui-1.10.3.slider.min.js',
                'js/scheduler-helpers.js',
                'js/table-selector.js',
            ],
            'css_files': [
                'css/scheduler2.css', 
                'css/slider/jquery-ui-1.10.3.slider.min.css', 
            ]
        }
        return reqs

    # the list of things passed to the js plugin
    def json_settings_list (self):
        # query_uuid will pass self.query results to the javascript
        # and will be available as "record" in :
        # on_new_record: function(record)
        return ['plugin_uuid', 'domid', 'query_uuid', 'time_slots', 'nodes', 'query_lease_uuid', 'query_all_resources_uuid']
    

    def export_json_settings (self):
        return True
    
    #Creates an Array with the timespans depending on granularity
    def createTimeSlots (this, granularity):
        #return type
        time_slots = []
        #init times
        time_s = datetime.time(0,00)
        time_f = datetime.time(23,59)
        now = datetime.datetime.now()
        #calc diffs
        dt_s = datetime.datetime.combine(now,time_s)
        dt_f = datetime.datetime.combine(now,time_f)
        #loop
        while (dt_s < dt_f):
            tmp = dt_s
            dt_s =  dt_s + datetime.timedelta(minutes=granularity)
            ts = str(tmp.hour).zfill(2) + ':' + str(tmp.minute).zfill(2) + '<span>-</span>' + str(dt_s.hour).zfill(2) + ':' + str(dt_s.minute).zfill(2)
            time_slots.append(ts)
        #return
        return time_slots
    
