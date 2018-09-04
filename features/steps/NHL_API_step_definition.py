#!/usr/bin/python3
# -*- coding: utf-8 -*-

from behave import given, when, then
import requests
import json, jmespath

global_general_variables = {}
http_request_header = {}
http_request_body = {}
http_request_url_query_param = {}

@given(u'Set teams url is "{teams_url}"')
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
    elif 'position' == body_parsing_for:
	    global_general_variables['teams_position'] = (global_general_variables['api_stats_filter'].search(current_json))
		
@given(u'The first season roster to compare is "{compare_season1}"')
def step_impl(context, compare_season1):
	if compare_season1 == '2016-2017':
		global_general_variables['roster1'] = (global_general_variables['roster_1617'])

@when(u'The second season roster to compare is "{compare_season2}"')
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

# Test Case2

@given(u'Set people url is "{people_url}"')
def step_impl(context, people_url):
    global_general_variables['people_URL'] = people_url
	
@given(u'The roster is for both 2016-2017 and 2017-2018 seasons')
def step_impl(context):
	global_general_variables['roster_season'] = (global_general_variables['both_seasons'])

@given(u'Set season stats api endpoint for "{season_stats}" roster')
def step_impl(context, season_stats):
    if season_stats == '2016-2017':
        global_general_variables['GET_api_endpoint'] = "/stats?stats=statsSingleSeason&season=20162017"
    elif season_stats == '2017-2018':
        global_general_variables['GET_api_endpoint'] = "/stats?stats=statsSingleSeason&season=20172018"	
		
@given(u'Set json filter as "{stats_filter}"')
def step_impl(context, stats_filter):
	global_general_variables['stats_filter'] = stats_filter
	api_stats_filter = jmespath.compile(stats_filter)
	global_general_variables['api_stats_filter'] = api_stats_filter

		
@then(u'Collect stat "{stats_parameter}" for the roster')
def step_impl(context, stats_parameter):
	people_url = global_general_variables['people_URL']
	roster_season = global_general_variables['roster_season']
	global_general_variables['stats_parameter'] = stats_parameter
	global_general_variables['stat_values'] = []
	for player in roster_season:
		if ('currentTeam' == stats_parameter or 'position' == stats_parameter):
			url_temp = people_url + str(player)
		else:
			url_temp = people_url + str(player) + global_general_variables['GET_api_endpoint']
		http_request_body.clear()
		global_general_variables['response_full'] = requests.get(url_temp,
                                                                             headers=http_request_header,
                                                                             params=http_request_url_query_param,
                                                                             data=http_request_body)
		current_json = (global_general_variables['response_full'].json())
		global_general_variables['stat_values'].append((global_general_variables['api_stats_filter'].search(current_json)))

@then(u'The data collected is cleaned')
def step_impl(context):
	nested_list = global_general_variables['stat_values']
	single_list = []
	empty = False
	for element in nested_list:
		if len(element) == 0:
			element.append('N/A')
		for points in element:
			single_list.append(points)
	global_general_variables['clean_stat_values'] = single_list

@then(u'The stats for season "{season}" are collected')
def step_impl(context,season):
	if '2016-2017' == season:
		global_general_variables['stat_1617'] = global_general_variables['clean_stat_values']
	elif '2017-2018' == season:
		global_general_variables['stat_1718'] = global_general_variables['clean_stat_values']
		
@given(u'The players data points for season "{season}"')
def step_impl(context,season):
	if '2016-2017' == season:
		global_general_variables['compare_stat1'] = global_general_variables['stat_1617']
	elif '2017-2018' == season:
		global_general_variables['compare_stat2'] = global_general_variables['stat_1718']	
			
@then(u'Compare player stats')
def step_impl(context):
	global_general_variables['improve_count'] = 0
	global_general_variables['noImprove_count'] = 0
	counter = len(global_general_variables['compare_stat1']) - 1
	while counter >= 0:
		if type(global_general_variables['compare_stat1'][counter]) and type(global_general_variables['compare_stat2'][counter])  == int:
			if global_general_variables['compare_stat1'][counter] < global_general_variables['compare_stat2'][counter]:
				global_general_variables['improve_count'] = global_general_variables['improve_count'] + 1
			else:
				global_general_variables['noImprove_count'] = global_general_variables['noImprove_count'] + 1
		counter = counter - 1

@then(u'The players should have more points in the season 2017-2018')
def step_impl(context):
	if global_general_variables['noImprove_count'] > 0:
		assert False, '*** ' + str(global_general_variables['noImprove_count']) + ' players had more points in season 2016-2017 ***'
		
@given(u'The team data points for season "{season}"')
def step_impl(context,season):
	team_points = 0
	if '2016-2017' == season:
		points_list = global_general_variables['stat_1617']
	elif '2017-2018' == season:
		points_list = global_general_variables['stat_1718']
	for points in points_list:
		if type(points) == int:
			team_points = team_points + points
			if '2016-2017' == season:
				global_general_variables['team_stat1'] = team_points
			elif '2017-2018' == season:
				global_general_variables['team_stat2'] = team_points
				
@then(u'Compare team stats')
def step_impl(context):
	global_general_variables['team_improvement'] = False
	if global_general_variables['team_stat2'] > global_general_variables['team_stat1']:
		global_general_variables['team_improvement'] = True
		
@then(u'The team should have more points in the season 2017-2018')
def step_impl(context):
	if global_general_variables['team_improvement'] == False:
		assert False, '*** The team did not improve, more points in season 2016-2017 ***'
		
# Test 3

@given(u'The Montreal Canadiens roster for "{season}" season')
def step_impl(context,season):
	if '2017-2018' == season:
		global_general_variables['roster_season'] = (global_general_variables['roster_1718'])

@given(u'The players currentTeam for season "{season}"')
def step_impl(context,season):
	if '2017-2018' == season:
		global_general_variables['currentTeam'] = global_general_variables['stat_1718']

@then(u'All the players currentTeam should be "{team}"')
def step_impl(context,team):
	not_canadien = 0
	for player in global_general_variables['currentTeam']:
		if team not in player:
			not_canadien = not_canadien + 1
	if not_canadien !=0:
		assert False, '*** Some players have different or no team in people currentTeam ***'
		
@given(u'The position information with "{function}" function')
def step_impl(context, function):
	if 'people' == function:
		global_general_variables['people_position'] = global_general_variables['stat_1718']
	elif 'teams' == function:
		global_general_variables['teams_position']
		
@then(u'Compare both functions')
def step_impl(context):
	global_general_variables['not_same_team'] = 0
	counter = len(global_general_variables['teams_position']) - 1
	while counter >= 0:
		if global_general_variables['teams_position'][counter] != global_general_variables['people_position'][counter]:
			global_general_variables['not_same_team'] += global_general_variables['not_same_team']
		counter = counter - 1

@then(u'Both should have the same team')
def step_impl(context):
	if global_general_variables['not_same_team'] != 0:
		assert False, '*** There are differences in positions between the two functions ***'