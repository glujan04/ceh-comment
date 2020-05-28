import logging
import base64
import hashlib
import hmac
import simplejson
import time

from ckan.common import request
from ckan.lib.helpers import url_for_static_or_external
import ckan.plugins as p

log = logging.getLogger(__name__)

class CommentPlugin(p.SingletonPlugin):
    
    p.implements(p.IConfigurable)
    p.implements(p.IConfigurer)
    p.implements(p.ITemplateHelpers)

    # IConfigurer

    def update_config(self, config_):
        p.toolkit.add_template_directory(config_, 'templates')
        p.toolkit.add_public_directory(config_, 'ceh_comment/public')
        p.toolkit.add_resource('ceh_comment/resources', 'ceh_comment')

    def configure(self, config):
    ##    '''
    ##    Called upon CKAN setup, will pass current configuration dict to the
    ##    plugin to read custom options.  To implement Disqus Single Sign On,
    ##    you must have your secret and public key in the ckan config file. For
    ##    more info on Disqus SSO see:
    ##    https://help.disqus.com/customer/portal/articles/236206-integrating-single-sign-on
    ##    '''
        ceh_name = config.get('ceh.comment.name', None)
    ##    disqus_secret_key = config.get('disqus.secret_key', None)
    ##    disqus_public_key = config.get('disqus.public_key', None)
        ceh_url = config.get('ceh.comment.url', None)
        site_url = config.get('ckan.site_url', None)
        site_title = config.get('ckan.site_title', None)
        if ceh_name is None:
            log.warn("No forum name is set. Please set \
                'ceh.comment.name' in your .ini!")
    ##    config['pylons.app_globals'].has_commenting = True

    ##    disqus_developer = p.toolkit.asbool(config.get('disqus.developer',
    ##                                                   'false'))
    ##    disqus_developer = str(disqus_developer).lower()
    ##    # store these so available to class methods
    ##    self.__class__.disqus_developer = disqus_developer
        self.__class__.ceh_name = ceh_name
    ##    self.__class__.disqus_secret_key = disqus_secret_key
    ##    self.__class__.disqus_public_key = disqus_public_key
        self.__class__.ceh_url = ceh_url
        self.__class__.site_url = site_url
        self.__class__.site_title = site_title

    @classmethod
    def ceh_comments(cls):
        '''Add Comments to the page.'''

        c = p.toolkit.c

        # Get user info to send for Disqus SSO

        # Set up blank values
        message = 'blank'
        sig = 'blank'
        timestamp = 'blank'

        # Get the user if they are logged in.
        user_dict = {}
        try:
            user_dict = p.toolkit.get_action('user_show')({'keep_email': True},
                                                          {'id': c.user})

        # Fill in blanks for the user if they are not logged in.
        except:
            user_dict['id'] = ''
            user_dict['name'] = ''
            user_dict['email'] = ''

        # Create the SSOm data.
        SSOdata = simplejson.dumps({
            'id': user_dict['id'],
            'username':  user_dict['name'],
            'email': user_dict['email'],
            })

        message = base64.b64encode(SSOdata)
        # generate a timestamp for signing the message
        timestamp = int(time.time())
        # generate our hmac signature
        sig = ''
        ##if cls.disqus_secret_key is not None:
        ##    sig = hmac.HMAC(cls.disqus_secret_key, '%s %s' %
        ##                    (message, timestamp), hashlib.sha1).hexdigest()

        # we need to create an identifier
        try:
            identifier = c.controller
            if identifier == 'package':
                identifier = 'dataset'
            if c.current_package_id:
                identifier += '::' + c.current_package_id
            elif c.id:
                identifier += '::' + c.id
            else:
                # cannot make an identifier
                identifier = ''
            # special case
            if c.action == 'resource_read':
                identifier = 'dataset-resource::' + c.resource_id
        except:
            identifier = ''
        data = {'identifier': identifier,
                ##'developer': cls.disqus_developer,
                ##'language': cls.language(),
                'ceh_shortname': cls.ceh_name,

                # start Koebrick change
                'site_url': cls.site_url,
                'site_title': cls.site_title,
                'message': message,
                ##'sig': sig,
                'timestamp': timestamp}
                ##'pub_key': cls.disqus_public_key}

        return p.toolkit.render_snippet('ceh_comments.html', data)

    @classmethod
    def ceh_recent(cls, num_comments=5):
        '''Add recent comments to the page. '''
        data = {'ceh_shortname': cls.ceh_name,
                'ceh_num_comments': num_comments}
        return p.toolkit.render_snippet('ceh_recent.html', data)

    @classmethod
    def current_ceh_url(cls, ):
        '''If `ceh_comment.url` is defined, return a fully qualified url for
        the current page with `ceh_comment.url` as the base url,'''

        if cls.ceh_url is None:
            return None

        return url_for_static_or_external(request.environ['CKAN_CURRENT_URL'],
                                          qualified=True, host=cls.ceh_url)

    def get_helpers(self):
        return {'ceh_comments': self.ceh_comments,
                'ceh_recent': self.ceh_recent,
                'current_ceh_url': self.current_ceh_url}
