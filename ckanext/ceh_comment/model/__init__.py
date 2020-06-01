import logging
import datetime

from sqlalchemy import event
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import types
from sqlalchemy import Index
from sqlalchemy.engine.reflection import Inspector
from sqlalchemy.orm import backref, relation
from sqlalchemy.exc import InvalidRequestError

from ckan import model
from ckan.model.meta import metadata, mapper, Session
from ckan.model.types import make_uuid
from ckan.model.domain_object import DomainObject
from ckan.model.package import Package

log = logging.getLogger(__name__)


__all__ = [
    'CehComment', 'ceh_comment_table'
]


ceh_comment_table = None


def init_db():

    if ceh_comment_table is None:
        define_comment_tables()
        log.debug('Ceh Comment tables defined in memory')

    if not model.package_table.exists():
        log.debug('Ceh Comment tables creation deferred')
        return

    if not ceh_comment_table.exists():

        # Create table individually rather than
        # using metadata.create_all()
        ceh_comment_table.create()

        log.debug('Ceh Comment tables created')
    else:
        from ckan.model.meta import engine
        log.debug('Ceh Comment tables already exist')
        # Check if existing tables need to be updated
        inspector = Inspector.from_engine(engine)

        # Check if ceh_comment table exist
        if 'ceh_comment' not in inspector.get_table_names():
            ceh_comment_table.create()


class CehCommentDomainObject(DomainObject):
    '''Convenience methods for searching objects
    '''
    key_attr = 'id'

    @classmethod
    def get(cls, key, default=None, attr=None):
        '''Finds a single entity in the register.'''
        if attr is None:
            attr = cls.key_attr
        kwds = {attr: key}
        o = cls.filter(**kwds).first()
        if o:
            return o
        else:
            return default

    @classmethod
    def filter(cls, **kwds):
        query = Session.query(cls).autoflush(False)
        return query.filter_by(**kwds)


class CehComment(CehCommentDomainObject):
    '''CehComment object
    '''
    pass


def define_comment_tables():

    global ceh_comment_table

    # New table
    ceh_comment_table = Table(
        'ceh_comment',
        metadata,
        Column('id', types.UnicodeText, primary_key=True, default=make_uuid),
        # The guid is the 'identity' of the dataset.
        Column('guid', types.UnicodeText, default=u''),
        Column('name', types.UnicodeText, nullable=False),
        Column('email', types.UnicodeText, nullable=False),
        Column('message', types.UnicodeText, nullable=False),
        Column('created', types.DateTime, default=datetime.datetime.utcnow),
        # If comment is active for show on forum list
        Column('active', types.Boolean, default=False),
        # If the record is a response to a comment
        Column('ref_id', types.UnicodeText, nullable=True),
        # The user id who activated or deactivated the registration in the forum list
        Column('pub_userid', types.UnicodeText, nullable=True),
        # The date of activation or deactivation of the registration in the forum list
        Column('pub_date', types.DateTime, nullable=True),
        # If the user has been notified
        Column('notify_alert', types.Integer),
    )

    mapper(
        CehComment,
        ceh_comment_table,
    )


def clean_db():

    if ceh_comment_table is None:
        define_comment_tables()
        log.debug('Ceh Comment tables defined in memory')

    try:
        if ceh_comment_table.exists():
           ceh_comment_table.drop()
    except InvalidRequestError:
        log.error('An error occurred while trying to remove ceh_comment table')

    log.info('ceh_comment table removed successfully')