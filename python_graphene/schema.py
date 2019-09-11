import graphene

class Query(graphene.ObjectType):
    hello = graphene.String()

    def resolve_hello(self, info):
        return 'world'

schema = graphene.Schema(query=Query)
result = schema.execute(
    '''
    {
        hello
    }
    '''
)

print(result.data.items())
# or, we can also convert the above result info json
import json
result_json = dict(result.data.items())
print(json.dumps(result_json, indent=4))
