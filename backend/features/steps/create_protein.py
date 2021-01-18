from behave import *
from django.contrib.auth.models import User

use_step_matcher("re")

@given("An authenticated user")
def step_impl(context):
    # sign up
    context.response = context.test.client.post("/api/v1/users/", content_type='application/json', 
                                    data={'username': 'ANA', 'password': 'secret'})
    # sign in
    context.response = context.test.client.post("/api/v1/sessions/", content_type='application/json', 
                                    data={'username': 'ANA', 'password': 'secret'})

@when("I create protein with sequence (?P<seq>.*)")
def step_impl(context, seq):
    organism_json = {'infected': False, 'sex': 'Male', 
                        'organism_mnemonic': 'RAT', 
                        'description': '...'}
    form_data = {
        'sequence': seq,
        'organism': organism_json
    }
    context.response = context.test.client.post('/api/v1/proteins/', 
                                    content_type='application/json', 
                                    data=form_data)

@then("I can see protein with sequence (?P<seq>.*) and status code (?P<status>\d+)")
def step_impl(context, seq, status):
    context.response = context.test.client.get('/api/v1/proteins/')
    code = context.response.status_code
    assert code == int(status), "{0} != {1}".format(code, status)
    assert seq == context.response.data['uninfected'][0]['sequence']