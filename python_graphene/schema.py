import graphene
from uuid import uuid4
from datetime import datetime

# --------------------------------------------------------
# Now let's say we have some complex data, like user data

class User(graphene.ObjectType):
    id         = graphene.ID(default_value=str(uuid4()))
    username   = graphene.String()
    created_at = graphene.DateTime(default_value=datetime.now())

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

# working/creating mutation
class CreateUser(graphene.Mutation):
    # since, we want to return our entire user.
    user = graphene.Field(User)

    class Arguments:
        username = graphene.String()

    def mutate(self, info, username):
        # user = User(id='3', username=username, created_at=datetime.now())
        user = User(username=username)
        return CreateUser(user=user)

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()



schema = graphene.Schema(query=Query, mutation=Mutation) # disable auto_camelcase or you have to pass is_admin as isAdmin
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
        isAadmin
    }
    '''
)

# result_users = schema.execute(
#     '''
#     {
#         users (limit: 2) {
#             id
#             username
#             created_at
#         }
#     }
#     '''
# ) # with limit

result_users = schema.execute(
    '''
    {
        users {
            id
            username
            createdAt
        }
    }
    '''
)

res_mutate = schema.execute(
    '''
    mutation {
        createUser(username: "Hefner") {
            user {
                id
                username
                createdAt
            }
        }
    }
    '''
)

print(result.data.items())
# or, we can also convert the above result info json
import json
result_json = dict(result.data.items())
print(json.dumps(result_json, indent=4))

# --------------------------------------------------------------
# eg: say wanted to know if a user was an administrator or not.
# we might have an is admin query.

# print(result_1.data.items())

# print(result_users.data.items())
# print(json.dumps(result_users.data, indent=4))


print(json.dumps(res_mutate.data, indent=4))
print('\n------------------------------------------')
print(json.dumps(result_users.data, indent=4))
