import os
import dialogflow_v2 as dialogflow
project_id=os.environ['DIALOGFLOW_PROJECT_ID']

# [START dialogflow_list_contexts]
def list_contexts(project_id, session_id):
    contexts_client = dialogflow.ContextsClient()

    session_path = contexts_client.session_path(project_id, session_id)

    contexts = contexts_client.list_contexts(session_path)

    print('Contexts for session {}:\n'.format(session_path))
    for context in contexts:
        print('Context name: {}'.format(context.name))
        print('Lifespan count: {}'.format(context.lifespan_count))
        print('Fields:')
        for field, value in context.parameters.fields.items():
            if value.string_value:
                print('\t{}: {}'.format(field, value))
# [END dialogflow_list_contexts]


# [START dialogflow_create_context]
def create_context(project_id, session_id, context_id, lifespan_count):
    contexts_client = dialogflow.ContextsClient()

    session_path = contexts_client.session_path(project_id, session_id)
    context_name = contexts_client.context_path(
        project_id, session_id, context_id)

    context = dialogflow.types.Context(
        name=context_name, lifespan_count=lifespan_count)

    response = contexts_client.create_context(session_path, context)

    print('Context created: \n{}'.format(response))
# [END dialogflow_create_context]

# [START dialogflow_delete_context]
def delete_context(project_id, session_id, context_id):
    contexts_client = dialogflow.ContextsClient()

    context_name = contexts_client.context_path(
        project_id, session_id, context_id)

    contexts_client.delete_context(context_name)
# [END dialogflow_delete_context]

if __name__ == '__main__':
    session_id = '+13106997821' 
    context_id="female"
    lifespan_count=3
    list_contexts(project_id, session_id)
