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
    p.implements(p.IRoutes, inherit=True)
    p.implements(p.IConfigurer, inherit=True)
    p.implements(p.IPackageController, inherit=True)
    p.implements(p.ITemplateHelpers, inherit=True)
    p.implements(p.IActions, inherit=True)
    p.implements(p.IAuthFunctions, inherit=True)

    # IConfigurer

    def update_config(self, config_):
        p.toolkit.add_template_directory(config_, "templates")
        p.toolkit.add_public_directory(config_, 'public')
        p.toolkit.add_resource('fanstatic', 'ckanext_comment')

    def configure(self, config):
        ceh_name = config.get('ceh.comment.name', None)
        ceh_url = config.get('ceh.comment.url', None)
        site_url = config.get('ckan.site_url', None)
        site_title = config.get('ckan.site_title', None)
        if ceh_name is None:
            log.warn("No forum name is set. Please set \
                'ceh.comment.name' in your .ini!")
        self.__class__.ceh_name = ceh_name
        self.__class__.ceh_url = ceh_url
        self.__class__.site_url = site_url
        self.__class__.site_title = site_title


    @classmethod
    def ceh_manager_comments(cls):
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

        return p.toolkit.render_snippet('ceh_manager_comments.html', data)

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
    def ceh_notify(cls):
        '''Icono de notificacion para el usuario logueado'''
        data = {'userid':''}
        return p.toolkit.render_snippet('ceh_notify.html', data)

    @classmethod
    def _new_comments(cls):
        '''Cantidad de comentarios nuevos'''
        import ckan.model as model
        from ckan.logic import get_action
        approval = 'pending'
        count = get_action('comment_count')({'model': model}, {'approval': approval})
        return count

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
                'new_comments': self._new_comments,
                'ceh_notify': self.ceh_notify,
                'ceh_manager_comments': self.ceh_manager_comments,
                'current_ceh_url': self.current_ceh_url,
                'get_comment_thread': self._get_comment_thread,
                'get_comment_count_for_dataset': self._get_comment_count_for_dataset}

    def get_actions(self):
        from ckanext.ceh_comment.logic.action import get, create, delete, update

        return {
            "comment_create": create.comment_create,
            "thread_show": get.thread_show,
            "comment_update": update.comment_update,
            "comment_show": get.comment_show,
            "comment_delete": delete.comment_delete,
            "comment_count": get.comment_count
        }

    def get_auth_functions(self):
        from ckanext.ceh_comment.logic.auth import get, create, delete, update

        return {
            'comment_create': create.comment_create,
            'comment_update': update.comment_update,
            'comment_show': get.comment_show,
            'comment_delete': delete.comment_delete,
            "comment_count": get.comment_count
        }

    # IPackageController

    def before_view(self, pkg_dict):
        # TODO: append comments from model to pkg_dict
        return pkg_dict

    # IRoutes

    def before_map(self, map):
        """
            /dataset/NAME/comments/reply/PARENT_ID
            /dataset/NAME/comments/add
        """
        controller = 'ckanext.ceh_comment.controller:CommentController'
        map.connect('/dataset/{dataset_id}/comments/add', controller=controller, action='add')
        map.connect('/dataset/{dataset_id}/comments/{comment_id}/edit', controller=controller, action='edit')
        map.connect('/dataset/{dataset_id}/comments/{parent_id}/reply', controller=controller, action='reply')
        map.connect('/dataset/{dataset_id}/comments/{comment_id}/delete', controller=controller, action='delete')
        return map

    def _get_comment_thread(self, dataset_name):
        import ckan.model as model
        from ckan.logic import get_action
        url = '/dataset/%s' % dataset_name
        return get_action('thread_show')({'model': model, 'with_deleted': True}, {'url': url})

    def _get_comment_count_for_dataset(self, dataset_name):
        import ckan.model as model
        from ckan.logic import get_action
        url = '/dataset/%s' % dataset_name
        count = get_action('comment_count')({'model': model}, {'url': url})
        return count
