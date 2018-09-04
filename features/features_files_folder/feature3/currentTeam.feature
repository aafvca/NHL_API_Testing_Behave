Feature: currentTeam

Background: 
	Given Set teams url is "https://statsapi.web.nhl.com/api/v1/teams/"
	  And Set people url is "https://statsapi.web.nhl.com/api/v1/people/"
	  
Scenario: Request Montreal Canadiens roster 2017-2018
  Given Set Montreal Canadiens api endpoint for "2017-2018" roster
	When Raise "GET" HTTP request
  Then Valid HTTP response should be received
	And Response http code should be 200 
	And Response HEADER content type should be "application/json" 
	And Response BODY should not be null or empty 
	And Response BODY parsing for "2017_2018_roster" should be successful 
	
Scenario: Collect current team information with people function
  Given The Montreal Canadiens roster for "2017-2018" season
    And Set json filter as "people[].currentTeam.name"
  Then Collect stat "currentTeam" for the roster
    And The data collected is cleaned
	And The stats for season "2017-2018" are collected
	
Scenario: Find if the currentTeam is Montreal Canadiens
  Given The players currentTeam for season "2017-2018"
  Then All the players currentTeam should be "Montréal Canadiens"
 
