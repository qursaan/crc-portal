import sys
import os.path
import optparse
# xxx warning : this is not taken care of by the debian packaging
# cfgparse seems to be available by pip only (on debian, that is)
# there seems to be another package that might be used to do similar stuff
# python-configglue - Glues together optparse.OptionParser and ConfigParser.ConfigParser
# additionally argumentparser would probably be the way to go, notwithstanding
# xxx Moving this into the parse method so this module can at least be imported
#import cfgparse

from manifold.util.singleton    import Singleton

# http://docs.python.org/dev/library/argparse.html#upgrading-optparse-code

class Options(object):

    __metaclass__ = Singleton

    # We should be able to use another default conf file
    CONF_FILE = '/etc/manifold.conf'
    
    def __init__(self, name = None):
        self._opt = optparse.OptionParser()
        self._defaults = {}
        self._name = name
        self.clear()

    def clear(self):
        self.options  = {}
        self.add_option(
            "-c", "--config", dest = "cfg_file",
            help = "Config file to use.",
            default = self.CONF_FILE
        )
        self.uptodate = True

    def parse(self):
        """
        \brief Parse options passed from command-line
        """
        # add options here

        # if we have a logger singleton, add its options here too
        # get defaults too
        
        # Initialize options to default values
        import cfgparse
        cfg = cfgparse.ConfigParser()
        cfg.add_optparse_help_option(self._opt)

        # Load configuration file
        try:
            cfg_filename = sys.argv[sys.argv.index("-c") + 1]
            try:
                with open(cfg_filename): cfg.add_file(cfg_filename)
            except IOError: 
                raise Exception, "Cannot open specified configuration file: %s" % cfg_filename
        except ValueError:
            try:
                with open(self.CONF_FILE): cfg.add_file(self.CONF_FILE)
            except IOError: pass

        for option_name in self._defaults:
            cfg.add_option(option_name, default = self._defaults[option_name])
            
        # Load/override options from configuration file and command-line 
        (options, args) = cfg.parse(self._opt)
        self.options.update(vars(options))
        self.uptodate = True


    def add_option(self, *args, **kwargs):
        default = kwargs.get('default', None)
        self._defaults[kwargs['dest']] = default
        if 'default' in kwargs:
            # This is very important otherwise file content is not taken into account
            del kwargs['default']
        kwargs['help'] += " Defaults to %r." % default
        self._opt.add_option(*args, **kwargs)
        self.uptodate = False
        
    def get_name(self):
        return self._name if self._name else os.path.basename(sys.argv[0])

    def __repr__(self):
        return "<Options: %r>" % self.options

    def __getattr__(self, key):
        if not self.uptodate:
            self.parse()
        return self.options.get(key, None)

    def __setattr(self, key, value):
        self.options[key] = value
