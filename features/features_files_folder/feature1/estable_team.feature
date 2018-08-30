Feature: Estable team feature

Background: 
	Given Set basic teams url is "https://statsapi.web.nhl.com/api/v1/teams/"
	   And Set roster json filter as "teams[].roster.roster[].person.id"

Scenario: GET request roster 2016-2017
  Given Set Montreal Canadiens api endpoint for "2016-2017" roster
    When Set HEADER param request content type as "application/json"
	And Set HEADER param response accept type as "application/json" 
	And Set Query param as "empty" 
	And Raise "GET" HTTP request
  Then Valid HTTP response should be received
	And Response http code should be 200 
	And Response HEADER content type should be "application/json" 
	And Response BODY should not be null or empty 
	And Response BODY parsing for "2016_2017_roster" should be successful 
	
Scenario: GET request roster 2017-2018
  Given Set Montreal Canadiens api endpoint for "2017-2018" roster
    When Set HEADER param request content type as "application/json"
	And Set HEADER param response accept type as "application/json" 
	And Set Query param as "empty" 
	And Raise "GET" HTTP request
  Then Valid HTTP response should be received
	And Response http code should be 200 
	And Response HEADER content type should be "application/json" 
	And Response BODY should not be null or empty 
	And Response BODY parsing for "2017_2018_roster" should be successful 