# a set of utilities to help make the global layout consistent across views

def the_user(request):
    "retrieves logged in user's email, or empty string"
    if not request.user.is_authenticated:
        return ''
    else:
        return request.user.email


# dropdowns are kind of ad hoc for now, and limited to one level
# [
# ### a regular first-level button
# {'label':...,'href':..., ['domid':.., 'disabled':...]},
# ### a dropdown
# { 'label': ..., 'href'=..., 'dropdown':True, 'contents': [ { 'label':.., 'href'} ] }
# , ..]

# see also templates/widget-topmenu.html for how these items are put together
# and plugins/topmenuvalidation for how this hident button is turned on when necessary



# current: the beginning of the label in the menu that you want to outline
def topmenu_items_static(current, request):
    has_user = request.user.is_authenticated
    result = []
    print(request.user)
    if has_user:
        result.append({'label':'Dashboard', 'href': '/portal/dashboard/'})
        result.append({'label':'Request a slice', 'href': '/portal/slice_request/'})
        # always create a disabled button for validation, and let the
        # topmenuvalidation plugin handle that asynchroneously, based on this domid
        result.append({'label':'Validation', 'href': '/portal/validate/', 'domid':'topmenu-validation', 'disabled':True})
        dropdown = []
        dropdown.append({'label': 'Platforms', 'href': '/portal/platforms/'})
        dropdown.append({'label': 'My Account', 'href': '/portal/account/'})
        dropdown.append({'label': 'Contact Support', 'href': '/portal/contact/'})
        result.append({'label': 'More', 'href':"#", 'dropdown':True, 'contents':dropdown})
    else:
        result.append({'label':'Home', 'href': '/login'})
        # looks like this is accessible to non-logged users
        result.append({'label':'Platforms', 'href': '/portal/platforms/'})
        result.append({'label':'Register', 'href': '/portal/register/'})
        result.append({'label':'Join us', 'href': '/portal/join/'})
        result.append({'label':'Contact Support', 'href': '/portal/contact/'})

    # mark active if the provided 'current', even if shorter, matches the beginning of d['label']
    if current is not None:
        current=current.lower()
        curlen=len(current)
        def mark_active(d,up=None):
            if d['label'][:curlen].lower() == current:
                d['is_active']=True
                if up is not None: up['is_active']=True
        for d in result:
            mark_active(d)
            if 'dropdown' in d:
                for dd in d['contents']: mark_active(dd,d)
    return result

# tmp - transition phase
def topmenu_items (current, request):
    #TODO: @qursaan removed
    # print "WARNING -- please now use topmenu_items_live (label, page) toplevel_items is deprecated -- WARNING"
    return topmenu_items_static(current, request)

# @qursaan
# from manifold.core.query import Query
from plugins.topmenuvalidation import TopmenuValidation
# integrated helper function for an animated menu
from portal.models import PendingUser


### this is now the 'live' version, that has plugins
# for asynchronous management of topmenu
def topmenu_items_live(current, page):
    request = page.request
    # @qursaan: comments
    query_pi_auths = PendingUser.objects.filter(authority_hrn='$user_hrn' )
    #query_pi_auths = Query.get('user').filter_by('user_hrn', '==', '$user_hrn' ).select('pi_authorities')
    #page.enqueue_query(query_pi_auths)
#        # even though this plugin does not have any html materialization, the corresponding domid
#        # must exist because it is searched at init-time to create the JS plugin
#        # so we simply piggy-back the target button created in the topmenu
    topmenuvalidation = TopmenuValidation(
        page=page,
        # see above
        domid='topmenu-validation',
        # @qursaan: comments
        query=query_pi_auths,
        # this one is the target for a $.show() when the query comes back
        button_domid="topmenu-validation")
    # although the result does not matter, rendering is required for the JS init code to make it in the page
    topmenuvalidation.render(request)

    return topmenu_items_static(current, request)

