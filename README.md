# NHL_API_testing_Behave

# General
The purpose of this repo is to create a testing framework using Behave framework (BDD) that will help to test the NHL API described in:

- https://gitlab.com/dword4/nhlapi
- https://github.com/erunion/sport-api-specifications/tree/master/nhl

This repo include 4 feature  and one step script.

# Prerequisites
In order to execute the test scripts you need:

- Python3 (https://www.python.org/download/releases/3.0/)
- Behave (https://behave.readthedocs.io/en/latest/index.html)
- jmespath (http://jmespath.org/)

Why jmespath? The API is based in json messages and I found that using jmespath is very simple to gather the data required 
for the tests plus it is very helpful to set json paths in the configuration file for test automation purposes.

The two API functions used are:

- https://statsapi.web.nhl.com/api/v1/teams
- https://statsapi.web.nhl.com/api/v1/people

# How to execute the scripts
After cloning the repo execute the command "behave"

# Test Case 1: A stable team (estable_team.feature)
The purpose of this Test Case is to verify if the number of Montreal Canadiens players in both 2016-2017 and 2017-2018 rosters are at least 10

Test Procedure:
- Find the roster information for both seasons using the teams function
- Compare both rosters and count how many players are in both
- If at least 10 players are in both rosters then Test case will pass

During the execution of the test case I found that 22 players were in both rosters [PASS]

# Test Case 2: Team improvement (team_improvement.feature)
The purpose of this Test Case is to verify that all the  players who played for the Canadiens in the seasons 2016-2017 and 2017-2018
have more points in 2017-2017 than 2016-2017. We want to know as well that the same players as a group scored more points in 
2017-2018 than 2016-2017

Test Procedure 2a: Player improvement
- Find the players that played with the Canadiens in both seasons using the teams function
- Find the points for every player in both seasons using the people function
- Compare the points per player in both seasons

During the execution of the test I found that 10/22 players had more points in 2016-2017 [FAIL]

Test Procedure 2b: Team Improvement
- Same procedure as 2a to gather the points information
- Add all the points from all players in 2016-2017 season and compare them with 2017-2018 season

During the execution of the test I found that the team scored more points in 2016-2017 than 2017-2018 [FAIL]

# Test case 3: Validate teams and people functions (currentTeam.feature and people_team_position.feature)
The purpose of this Test Case is to validate that the teams function returns the same information than the people function for the 2017-2018 roster.

Test Procedure 3a: Current Team from people function should be Montreal Canadiens
- Find the players that were with the Canadiens in the 2017-2018 season using the teams function and collect the current team information
- Use the same roster to find the current team information using the people function
- Compare information from both functions

During the execution of the test I found that some players have no team or a different team using the people function [FAIL]

Test Procedure 3b: Player position from people function should match the player position from the teams function
- Find the players that were with the Canadiens in the 2017-2018 season using the teams function and collect the position information
- Use the same roster to collect the position information using the people function
- Compare information from both functions

During the execution of the test I found that both functions showed the same position for all players [PASS]

# Conclusion
After the execution of this test cases I can conclude that the people function is not alligned with the teams function plus I found incorrect or sometimes no data
for some players.
The teams function seems to be in better shape but more testing is required, some of the tests that can be included are:

- Test different positions and different teams
- Invalid values in the requests
- POST and DELETE requests to update the data structure
