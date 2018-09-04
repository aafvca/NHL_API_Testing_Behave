Feature: Team improvement feature

Background: 
	Given Set people url is "https://statsapi.web.nhl.com/api/v1/people/"

Scenario: Request points information for season 2016-2017
  Given The roster is for both 2016-2017 and 2017-2018 seasons
	And Set season stats api endpoint for "2016-2017" roster
	And Set json filter as "stats[].splits[].stat.points"
  Then Collect stat "points" for the roster
    And The data collected is cleaned
	And The stats for season "2016-2017" are collected

Scenario: Request points information for season 2017-2018
  Given The roster is for both 2016-2017 and 2017-2018 seasons
	And Set season stats api endpoint for "2017-2018" roster
	And Set json filter as "stats[].splits[].stat.points"
  Then Collect stat "points" for the roster
    And The data collected is cleaned
	And The stats for season "2017-2018" are collected	  
	  
Scenario: Find out if the players improve from one season to the other
  Given The players data points for season "2016-2017"
    And The players data points for season "2017-2018"
  Then Compare player stats
    And The players should have more points in the season 2017-2018
	  
Scenario: Find out if the team improve from one season to the other
  Given The team data points for season "2016-2017"
    And The team data points for season "2017-2018"
  Then Compare team stats
    And The team should have more points in the season 2017-2018