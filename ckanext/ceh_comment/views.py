
from ckan import logic, model
from ckan.common import _, g

def acquired_datasets():
    context = {'auth_user_obj': g.userobj, 'for_view': True, 'model': model, 'session': model.Session, 'user': g.user}
    data_dict = {'user_obj': g.userobj}

    extra_vars = {
        'user_dict': user_dict,
        'acquired_datasets': acquired_datasets,
    }
    return base.render('user/dashboard_acquired.html', extra_vars)


class AcquiredDatasetsControllerUI(base.BaseController):

    def acquired_datasets(self):
        return acquired_datasets()