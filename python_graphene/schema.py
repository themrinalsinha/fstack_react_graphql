import graphene

class Query(graphene.ObjectType):
    hello = graphene.String()
    is_admin = graphene.Boolean()

    def resolve_hello(self, info):
        return 'world'

    def resolve_is_admin(self, info):
        return True

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

print(result.data.items())
# or, we can also convert the above result info json
import json
result_json = dict(result.data.items())
print(json.dumps(result_json, indent=4))

print(result_1.data.items())

# --------------------------------------------------------------
# eg: say wanted to know if a user was an administrator or not.
# we might have an is admin query.
