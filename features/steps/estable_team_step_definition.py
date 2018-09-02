#!/usr/bin/python3
# -*- coding: utf-8 -*-

from behave import given, when, then
import requests
import json, jmespath

global_general_variables = {}
http_request_header = {}
http_request_body = {}
http_request_url_query_param = {}

@given(u'Set basic teams url is "{teams_url}"')
def step_impl(context, teams_url):
    global_general_variables['teams_URL'] = teams_url
    
@given(u'Set roster json filter as "{api_filter}"')
def step_impl(context, api_filter):
    global_general_variables['api_filter'] = api_filter
    api_teams_roster_id = jmespath.compile(api_filter)
    global_general_variables['api_teams_roster_id'] = api_teams_roster_id

@given(u'Set Montreal Canadiens api endpoint for "{roster_season}" roster')
def step_impl(context, roster_season):
    if roster_season == '2016-2017':
        global_general_variables['GET_api_endpoint'] = "/8?expand=team.roster&season=20162017"
    elif roster_season == '2017-2018':
        global_general_variables['GET_api_endpoint'] = "/8?expand=team.roster&season=20172018"
        
@when(u'Raise "{http_request_type}" HTTP request')
def step_impl(context, http_request_type):
    url_temp = global_general_variables['teams_URL']
    if 'GET' == http_request_type:
        url_temp += global_general_variables['GET_api_endpoint']
        http_request_body.clear()
        global_general_variables['response_full'] = requests.get(url_temp,
                                                                                         headers=http_request_header,
                                                                                         params=http_request_url_query_param,
                                                                                         data=http_request_body)
                                                                                         
@then(u'Valid HTTP response should be received')
def step_impl(context):
    if None in global_general_variables['response_full']:
        assert False, 'Null response received'
        
@then(u'Response http code should be {expected_response_code:d}')
def step_impl(context, expected_response_code):
    global_general_variables['expected_response_code'] = expected_response_code
    actual_response_code = global_general_variables['response_full'].status_code
    if str(actual_response_code) not in str(expected_response_code):
        print (str(global_general_variables['response_full'].json()))
        assert False, '***ERROR: Following unexpected error response code received: ' + str(actual_response_code)
        
@then(u'Response HEADER content type should be "{expected_response_content_type}"')
def step_impl(context, expected_response_content_type):
    global_general_variables['expected_response_content_type'] = expected_response_content_type
    actual_response_content_type = global_general_variables['response_full'].headers['Content-Type']
    if expected_response_content_type not in actual_response_content_type:
        assert False, '***ERROR: Following unexpected error response content type received: ' + actual_response_content_type


@then(u'Response BODY should not be null or empty')
def step_impl(context):
    if None in global_general_variables['response_full']:
        assert False, '***ERROR:  Null or none response body received'

@then(u'Response BODY parsing for "{body_parsing_for}" should be successful')
def step_impl(context, body_parsing_for):
    current_json = (global_general_variables['response_full'].json())
    if '2016_2017_roster' == body_parsing_for:
        global_general_variables['roster_1617'] = (global_general_variables['api_teams_roster_id'].search(current_json))
    elif '2017_2018_roster' == body_parsing_for:
        global_general_variables['roster_1718'] = (global_general_variables['api_teams_roster_id'].search(current_json))
		
@given(u'The first season roster to compare is "{compare_season1}"')
def step_impl(context, compare_season1):
	if compare_season1 == '2016-2017':
		global_general_variables['roster1'] = (global_general_variables['roster_1617'])

@given(u'The second season roster to compare is "{compare_season2}"')
def step_impl(context, compare_season2):
	if compare_season2 == '2017-2018':
		global_general_variables['roster2'] = (global_general_variables['roster_1718'])

@when(u'There are some players in both seasons')
def step_impl(context):
	both_seasons = []
	for player in (global_general_variables['roster1']):
		if player in (global_general_variables['roster2']):
			both_seasons.append(player)
	global_general_variables['both_seasons'] = both_seasons
		
@when(u'The minimum number of players in both seasons is "{min_players}"')
def step_impl(context, min_players):
    global_general_variables['min_players'] = int(min_players)
	
@then(u'We have a stable team')
def step_impl(context):
	if len(global_general_variables['both_seasons']) < (global_general_variables['min_players']):
		assert False, '*** There are less than 10 players in both seasons ***'
	else:
		print 'The max number of players is: ' + str(len(global_general_variables['both_seasons']))

 


