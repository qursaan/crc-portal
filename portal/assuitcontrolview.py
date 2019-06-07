

import os, time
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from portal.models import PhysicalNode, MyUser
from howdy.models import Node_Phy_Details,Variable, Values


def the_user(request):
    "retrieves logged in user's email, or empty string"
    if not request.user.is_authenticated():
        return ''
    else:
        return request.user.id


def simple_upload(request):
    if request.user.is_authenticated:
        if request.session['node_id']:
            print('from upload' + request.session['node_id'])

        if request.method == 'POST' and request.FILES['myfile']:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            dev_id = int(request.session['node_id'])
            p = Node_Phy_Details.objects.filter(deviceID=dev_id)[0]
            acmsport = p.devicePort
            baudrate = p.deviceBaud
            localRemote = p.DevType
            deviceRbAddress=p.deviceRbAddress
            if localRemote=='R':
                #./manage.py client ACM0 115200 172.31.149.53 /root/crc-portal/crc-portal/howdy/management/commands/test.hex
                #0x1e9801
                os.system(
                    './manage.py client ' + str(dev_id) + ' ' + baudrate + ' ' + deviceRbAddress + ' /root/crc-portal/crc-portal' + uploaded_file_url)

                print( './manage.py client ' + str(dev_id) + ' ' + baudrate + ' ' + deviceRbAddress + ' /root/crc-portal/crc-portal' + uploaded_file_url)

            else:
                os.system(
                    "/usr/share/arduino/hardware/tools/avrdude -C/usr/share/arduino/hardware/tools/avrdude.conf  -patmega2560 -cwiring -P/dev/tty" + acmsport + " -b" + baudrate + " -D -V -Uflash:w:/root/crc-portal/crc-portal" + uploaded_file_url + ":i")

               # cmd = "/usr/share/arduino/hardware/tools/avrdude -C/usr/share/arduino/hardware/tools/avrdude.conf  -patmega2560 -cwiring -P/dev/tty" + acmsport + " -b" + baudrate + " -D -V"

               # p1 = subprocess.check_output([cmd],stderr=subprocess.STDOUT,shell=True)
            # output, error = p1.communicate()
               # print('____________________________________________________')
            #print (p1)
               # out2 = p1.split("=")
                #deviceSignture = out2[1][0:10]
                #print("Device signture as obtained is by ali hussein is:" +deviceSignture )
               # print('____________________________________________________')



            return render(request, 'mytemp.html', {'uploaded_file_url': uploaded_file_url})
        else:
            return render(request, 'mytemp.html')


def manage_variables_user(request):
    if request.POST.get('del_var'):
        Variable.objects.filter(id=request.POST.get('del_var')).delete()
        Values.objects.filter(usernameID=the_user(request) ,deviceID = request.session['node_id_for_vars_session']).delete()
        return HttpResponseRedirect('/portal/Manage_Varaibles_user/')
    if request.POST.get('varnametoadd'):
        device = PhysicalNode.objects.filter(id=str(request.session['node_id_for_vars_session']))[0]
        user = MyUser.objects.filter(id=the_user(request))[0]
        x =Variable(varName = request.POST.get('varnametoadd'),deviceID=device,usernameID=user)
        x.save()
        return HttpResponseRedirect('/portal/Manage_Varaibles_user/')

    if request.user.is_authenticated:
        var_list = Variable.objects.filter(usernameID=the_user(request) ,deviceID = request.session['node_id_for_vars_session'])
        return render(request, 'newtemp_user.html',
                    {'node_user_id1': str(request.session['node_id_for_vars_session']),
                    'node_user_id2': str(the_user(request)),'var_list':var_list})  # return render_to_response('newtemp_user.html',{'nodeid':request.session['node_id_for_vars_session']})


def manage_variables(request):
    # page = Page(self.request)
    # page.add_js_files(["js/jquery.validate.js", "js/my_account.register.js", "js/my_account.edit_profile.js"])
    # page.add_css_files(["css/onelab.css", "css/account_view.css", "css/plugin.css"])

    if request.user.is_authenticated:
        print(request.session['username'])
        if request.session['vars']:
            print('from upload' + request.session['vars'])
        phenomena_DEVID = request.session['vars']
        extra_serie = {}
        user = MyUser.objects.filter(email=request.session['username'])[0]
        p = Values.objects.filter(deviceID=phenomena_DEVID.split("_")[1], varname=phenomena_DEVID.split("_")[0],
                                  usernameID=user)

        print('deviceID=' + phenomena_DEVID.split("_")[1] + ',varname=' + phenomena_DEVID.split("_")[0])
        x_data = p.values_list('timestamp', flat=True)
        # print(x_data)
        xdata = []
        for datetimee in x_data:
            xdata.append(
                time.mktime(datetimee.timetuple()) * 1000)  # xdata.append(int(time.mktime(datetimee.timetuple()))*1000)
        # (int(datetimee.strftime("%s")))
        # print(xdata)
        ydata = p.values_list('varValue')

        tooltip_date = "%H:%M:%S %p"
        # extra_serie1 = {"tooltip": {"y_start": "", "y_end": " cal"}, "date_format": tooltip_date, }
        chartdata = {'x': xdata, 'name1': phenomena_DEVID, 'y1': ydata, 'kwargs1': {'color': '#a4c639'}, }

        charttype = "lineChart"
        chartcontainer = 'linechart_container'  # container name
        data = {'charttype': charttype, 'chartdata': chartdata, 'chartcontainer': chartcontainer,
                'extra': {'x_is_date': True, 'x_axis_format': '%H:%M:%S %p', 'reduceXTicks': False,
                          'tag_script_js': True, 'jquery_on_ready': False, }}

        #   chartdata = {'x': xdata, 'name1': 'Temp', 'y1': ydata, 'extra1': extra_serie, }
        #  charttype = "lineChart"
        # chartcontainer = 'linechart_container'  # container name
        # data = {'charttype': charttype, 'chartdata': chartdata, 'chartcontainer': chartcontainer,
        #       'extra': {'x_is_date': True,  'x_axis_format': '%d-%m-%Y-%H-%M-%S', 'tag_script_js': True, 'jquery_on_ready': False, }}
        return render(request,'newTempVar.html', data)  # return render(request, 'newTempVar.html')
    else:
        render(request, 'newTempVar.html')