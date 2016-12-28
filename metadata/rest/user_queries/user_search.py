"""CherryPy Status Usersearch object class."""
import re
import cherrypy
from cherrypy import tools
from peewee import OP, Expression
from metadata.orm import Users
from metadata.rest.user_queries.query_base import QueryBase


class UserSearch(QueryBase):
    """Retrieves detailed info for a given user."""

    exposed = True

    @staticmethod
    def search_for_user(search_term):
        """Return a dictionary containing information about a given user."""
        terms = re.findall(r'[^+ ,;]+', search_term)
        # if len(terms) == 0:
        #     raise cherrypy.HTTPError(
        #         '400 Invalid Request Options',
        #         QueryBase.compose_help_block_message()
        #     )
        keys = ['first_name', 'last_name', 'network_id', 'email_address', 'id']
        where_clause = Expression(1, OP.EQ, 1)
        for user_term in terms:
            user_term = str(user_term)
            where_clause_part = Expression(1, OP.EQ, 0)
            for k in keys:
                if k == 'id':
                    if re.match('[0-9]+', user_term):
                        where_clause_part |= Expression(
                            Users.id, OP.EQ, user_term)
                else:
                    where_clause_part |= Expression(
                        getattr(Users, k), OP.ILIKE, '%{0}%'.format(user_term))
            where_clause &= (where_clause_part)
        objs = Users.select().where(where_clause)
        # print objs.sql()
        if len(objs) == 0:
            message = "No user entries were retrieved using the terms: '"
            message += '\' and \''.join(terms) + '\''
            raise cherrypy.HTTPError('404 No Valid Users Located', message)

        return [QueryBase.format_user_block(obj) for obj in objs]

    # CherryPy requires these named methods.
    # pylint: disable=invalid-name
    @staticmethod
    @tools.json_out()
    @cherrypy.expose
    def GET(search_term=None):
        """Return the requested user information for a given set of search criteria."""
        if search_term is not None and len(search_term) > 0:
            cherrypy.log.error('search request')
            return UserSearch.search_for_user(search_term)
        else:
            cherrypy.log.error('invalid request')
            raise cherrypy.HTTPError(
                '400 Invalid Request Options',
                QueryBase.compose_help_block_message()
            )
