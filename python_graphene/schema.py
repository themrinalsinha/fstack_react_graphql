import graphene
from datetime import datetime

# --------------------------------------------------------
# Now let's say we have some complex data, like user data

class User(graphene.ObjectType):
    id         = graphene.ID()
    username   = graphene.String()
    created_at = graphene.DateTime()

# to pass the limit parameter
class Query(graphene.ObjectType):
    users = graphene.List(User, limit=graphene.Int())
    hello = graphene.String()
    is_admin = graphene.Boolean()

    def resolve_hello(self, info):
        return 'world'

    def resolve_is_admin(self, info):
        return True

    def resolve_users(self, info, limit=None):
        return [
            User(id='1', username='Fred', created_at=datetime.now()),
            User(id='2', username='Jred', created_at=datetime.now()),
            User(id='3', username='Pred', created_at=datetime.now()),
        ][:limit]

schema = graphene.Schema(query=Query, auto_camelcase=False) # disable auto_camelcase or you have to pass is_admin as isAdmin
result = schema.execute(
    '''
    {
        hello
    }
    '''
)
result_1 = schema.execute(
    '''
    {
        is_admin
    }
    '''
)

result_users = schema.execute(
    '''
    {
        users (limit: 2) {
            id
            username
            created_at
        }
    }
    '''
)

print(result.data.items())
# or, we can also convert the above result info json
import json
result_json = dict(result.data.items())
print(json.dumps(result_json, indent=4))

print(result_1.data.items())

print(result_users.data.items())
print(json.dumps(result_users.data, indent=4))


# --------------------------------------------------------------
# eg: say wanted to know if a user was an administrator or not.
# we might have an is admin query.
