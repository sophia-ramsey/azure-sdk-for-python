# originally copied from azure-ai-inference 

# # ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
import os
import json
import azure.ai.assistants as sdk

from model_assistants_test_base import (
    ModelClientTestBase,
    ServicePreparerAssistantClient
)
from azure.core.pipeline.transport import RequestsTransport
from devtools_testutils import recorded_by_proxy
from azure.core.exceptions import AzureError, ServiceRequestError
from azure.core.credentials import AzureKeyCredential

'''
    general questions:
     do i need a test_base.py file? 
        I think I will for more complex tests -- would starting with azure-ai-inference/tests/model_inference_test_base.py and then adding/deleting for assistant functions be a good start? 
     should print statements be left in tests for debugging purposes? 
     should I keep looking at properties directly or should I write a function to get them 
        func(assistant.name)
            vs
        name = get_name(assistant)
        func(name)
     should I keep assert statements from previous parts of the process? 
    '''
# TODO finish model_assistants_test_base type of file (based on model_inference_test_base) and figure out how to upload credentials and things 

# The test class name needs to start with "Test" to get collected by pytest
class TestModelClient(ModelClientTestBase):

    # **********************************************************************************
    #
    #                               UNIT TESTS
    #
    # **********************************************************************************

    # #  TODO figure out how to correctly pass in endpoint, credential, api version
    # @ServicePreparerAssistantClient()
    # # @recorded_by_proxy
    # def test_credentials(self, **kwargs):
        
    #     print('here1')
    #     print(kwargs)
    #     print('here2')
    #     endpoint, credential, api_version = self._load_assistant_client_credentials(**kwargs)
    #     print(endpoint)
    #     assert 1 == 0
    

    # # **********************************************************************************
    # #
    # #                      HAPPY PATH SERVICE TESTS - Assistant APIs
    # #
    # # **********************************************************************************
    
    # test client creation
    # @ServicePreparerAssistantClient()
    # @recorded_by_proxy
    def test_create_client(self, **kwargs):
        # create client
        client = sdk.AssistantsClient(**kwargs)
        assert isinstance(client, sdk.AssistantsClient)
       
        # TODO question: does other information need to be verified? 
        # close client
        client.close()

    # test assistant creation and deletion
    # @ServicePreparerAssistantClient()
    # @recorded_by_proxy
    def test_create_delete_assistant(self, **kwargs):
        # create client
        client = sdk.AssistantsClient(**kwargs)
        assert isinstance(client, sdk.AssistantsClient)

        # create assistant
        assistant = client.create_assistant(model="gpt-4o", name="my-assistant", instructions="You are helpful assistant")
        assert assistant.id
        print("Created assistant, assistant ID", assistant.id)

        # TODO question: do we need to do anything else with the id/assistant
        
        # delete assistant and close client
        client.delete_assistant(assistant.id)
        print("Deleted assistant")
        client.close()

    # @ServicePreparerAssistantClient()
    # @recorded_by_proxy
    def test_update_assistant(self, **kwargs):
        # create client
        client = sdk.AssistantsClient(**kwargs) 
        assert isinstance(client, sdk.AssistantsClient)

        # create assistant
        assistant = client.create_assistant(model="gpt-4o", name="my-assistant", instructions="You are helpful assistant")
        assert assistant.id

        # update assistant and confirm changes went through
        assistant.update(name="my-assistant2", instructions="You are helpful assistant")
        assert assistant.name
        assert assistant.name == "my-assistant2"

        # delete assistant and close client
        client.delete_assistant(assistant.id)
        print("Deleted assistant")
        client.close()

    # @ServicePreparerAssistantClient()
    # @recorded_by_proxy
    def test_assistant_list(self, **kwargs):
        # create client and ensure there are no previous assistants
        client = sdk.AssistantsClient(**kwargs)
        assert client.list_assistants().data.__len__() == 0

        # create assistant and check that it appears in the list
        assistant = client.create_assistant(model="gpt-4o", name="my-assistant", instructions="You are helpful assistant")
        assert client.list_assistants().data.__len__() == 1
        assert client.list_assistants().data[0].id == assistant.id 

        # create second assistant and check that it appears in the list
        assistant2 = client.create_assistant(model="gpt-4o", name="my-assistant2", instructions="You are helpful assistant")
        assert client.list_assistants().data.__len__() == 2
        assert client.list_assistants().data[0].id == assistant.id or client.list_assistants().data[1].id == assistant.id 

        # delete assistants and close client
        client.delete_assistant(assistant.id)
        client.delete_assistant(assistant2.id)
        print("Deleted assistants")
        client.close()

    # # **********************************************************************************
    # #
    # #                      HAPPY PATH SERVICE TESTS - Thread APIs
    # #
    # # **********************************************************************************

    # # **********************************************************************************
    # #
    # #                      HAPPY PATH SERVICE TESTS - Thread APIs
    # #
    # # **********************************************************************************
    

    # # **********************************************************************************
    # #
    # #                      HAPPY PATH SERVICE TESTS - Run APIs
    # #
    # # **********************************************************************************


    # # **********************************************************************************
    # #
    # #                      HAPPY PATH SERVICE TESTS - Synchronous / Asynchronous TODO maybe a separate file since it'll be the same tests
    # #
    # # **********************************************************************************


    # # **********************************************************************************
    # #
    # #                      HAPPY PATH SERVICE TESTS - Streaming APIs
    # #
    # # **********************************************************************************

    
    # # **********************************************************************************
    # #
    # #                       NEGATIVE TESTS - TODO 
    # #
    # # **********************************************************************************

    # # **********************************************************************************
    # #
    # #                            ERROR TESTS - 
    # #
    # # **********************************************************************************

