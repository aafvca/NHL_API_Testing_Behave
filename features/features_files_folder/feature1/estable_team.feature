Feature: Estable team feature

Scenario: Search for the number of players in both seasons
	Given I send a request to get the roster1
	And I send a request to get the roster2
	When I find the players in both seasons
	Then At least 10 players should be in both seasons
