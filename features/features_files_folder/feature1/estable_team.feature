Feature: Estable team feature

Background: 
	Given Set basic teams url is "https://statsapi.web.nhl.com/api/v1/teams/"
	   And Set roster json filter as "teams[].roster.roster[].person.id"

Scenario: Request roster 2016-2017
  Given Set Montreal Canadiens api endpoint for "2016-2017" roster
	When Raise "GET" HTTP request
  Then Valid HTTP response should be received
	And Response http code should be 200 
	And Response HEADER content type should be "application/json" 
	And Response BODY should not be null or empty 
	And Response BODY parsing for "2016_2017_roster" should be successful 
	
Scenario: Request roster 2017-2018
  Given Set Montreal Canadiens api endpoint for "2017-2018" roster
	When Raise "GET" HTTP request
  Then Valid HTTP response should be received
	And Response http code should be 200 
	And Response HEADER content type should be "application/json" 
	And Response BODY should not be null or empty 
	And Response BODY parsing for "2017_2018_roster" should be successful 
	
Scenario: Find the number of players in both seasons
  Given The first season roster to compare is "2016-2017" 
    And The second season roster to compare is "2017-2018"
	When There are some players in both seasons
	And The minimum number of players in both seasons is "10"
  Then We have a stable team