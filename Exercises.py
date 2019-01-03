import pandas as pd
import numpy as np
import datetime


# Loads Bundesliga results dataset. 
df = pd.read_csv('https://raw.githubusercontent.com/vincentarelbundock/Rdatasets/master/csv/vcd/Bundesliga.csv')

def Exercise1(dataset):
	'''
	From the Bundesliga results dataset defined above, calculate which team has scored 
	the most homegoals over all seasons.
	'''

	# return (team_with_most_homegoals_string, number_of_homegoals_int)
	
def Exercise2(dataset):
	''' From the Bundesliga results dataset calculate which team has had the 
	most consecutive games without conceding (over all seasons)any goals and how many
	games that streak lasted.
	'''

	# return (team_with_longest_streak_string, length_of_streak_int)

def Exercise3(dataset):
	'''
	In football, every win awards the team 3 points, every tie awards 1 point 
	and a loss 0 points. Considering this, return the probability (as a float in the
	interval [0,1])	that the team with less points in the current SEASON (up to matchday)
	wins the match.	Round to 2 decimals	using the built-in function round().
	Note that this is NOT a forecasting problem. Note that you should NOT return the 
	probability per season.
	''' 

	# return probability_float

