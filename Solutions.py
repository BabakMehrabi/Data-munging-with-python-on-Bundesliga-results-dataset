import pandas as pd
import numpy as np

df = pd.read_csv('Bundesliga.csv')

def Exercise1(dataset):
	# I change the name of input because the name "df" is more consized 
	df= dataset.copy() 
	del(dataset)

	# For every available HomeTeam we find the sum of HomeGoals over all seasons, 
	# and we then sort the series
	temp= df.groupby('HomeTeam')['HomeGoals'].apply(sum).sort_values()
	name= temp.index[-1]
	goals_num= temp[-1]
	print("""The team which has scored the most homegoals over all seasons is
(with the total number of all HomeGoals):\n""")
	return name, goals_num
################################################################################
"""
How to find the team which has the most consecutive games without conceding a goal:

	1. We create a column for every team, where the cumulative number of conceded goals
		is shown in every row. In the rows where that team has no game, we place a nan.
		We name this column 'team_GoalsConceded'

	2. If we group it by every team_GoalsConceded, it results in a Series for all possible
		levels of  Team_GoalsConceded. We then obtain the size of this Groupby Series, and 
		then apply the max function to it. The result will show the most consecutive games
		with no conceding goal for that specific team. Then we can compare the results for
		all the teams to find out the best team (with the desired criteria).
"""

def Exercise2(dataset):
	# I change the name of input because the name "df" is more consized 
	df= dataset.copy() 
	del(dataset)

	all_teams= df['HomeTeam'].unique()
	for team in all_teams:
		col= team+'_GoalsConceded'
		df[col]= np.nan  

	for team in all_teams:
		col= team+'_GoalsConceded'
		# In case the team is a HomeTeam, the conceded goals are the AwayGoals
		temp= df[ df['HomeTeam']== team ] ['AwayGoals']
		df.loc[temp.index, col]= temp # save the result in the corresponding column

		# In case the team is an AwayTeam, the conceded goals are the HomeGoals
		temp= df[ df['AwayTeam']== team ] ['HomeGoals']
		df.loc[temp.index, col]= temp # save the result in the corresponding column

	columns= df.columns[8:] # 8 is the beginning index of newly created columns
	AllTeamsMaxStreaks= {}
	# For the newly created column showing the conceded goals, overwrite their
	# values by the cumulative sum, and save the biggest streak in a dictionary
	for col in columns: 
		df[ col ]= df[ col ].cumsum() 

		maximum_streak= df.groupby(col).size().max() - 1 # minus 1 because the first 
								# value in the level was created by a conceded goal 
		team_name= col.split('_')[0]
		AllTeamsMaxStreaks[ team_name ]= [ maximum_streak ]

	def keywithmaxval(d):
		# a) create a list of the dict's keys and values; 
		# b) return the key with the max value 
		v=list(d.values())
		m = max(v) [0]
		indices= [i for i, j in enumerate(v) if j == m]
		k=list(d.keys())
		return [ k[ ind ] for ind in indices ][0], m 

	print('The team with the longest streak of not conceding a goal is:\n')
	return keywithmaxval(AllTeamsMaxStreaks)

######################################################################################
"""
How to find the probability that the team with less points (up to the natchday) in the
current season will win the macth?

	1. We create a column for every team, where points collected by that in every season
		is shown. The important point is that if for ex. a team starts the season with 
		a win, its point in that match is still zero. Only in the its second match the 
		obtained 3 points from the first macth is shown.

	2. To find the desired probability, we must find two values. First the number of
		all the cases where two teams competing have 
"""

def Exercise3(dataset):
	# I change the name of input because the name "df" is more consized 
	df= dataset.copy() 
	del(dataset)

	all_teams= df['HomeTeam'].unique()
	for team in all_teams:
		df[team+'_points']= np.nan

	def create_points(season):
		season_teams= season['HomeTeam'].unique() 
		# It could be season['AwatyTeam'].unique() too. The result is the same
		for team in season_teams:
			col= team+'_points'
			season[ col ].loc[ (season['HomeTeam']== team) & \
										(season['HomeGoals'] > season['AwayGoals']) ]= 3
			season[ col ].loc[ (season['HomeTeam']== team) & \
										(season['HomeGoals'] == season['AwayGoals']) ]= 1
			season[ col ].loc[ (season['HomeTeam']== team) & \
										(season['HomeGoals'] < season['AwayGoals']) ]= 0
			season[ col ].loc[ (season['AwayTeam']== team) & \
										(season['HomeGoals'] < season['AwayGoals']) ]= 3
			season[ col ].loc[ (season['AwayTeam']== team) & \
										(season['HomeGoals'] == season['AwayGoals']) ]= 1
			season[ col ].loc[ (season['AwayTeam']== team) & \
										(season['HomeGoals'] > season['AwayGoals']) ]= 0
		return season

	df= df.groupby('Year').apply(create_points)

	# As we descrived in our solution, these points must be shifted one match forward
	def shift_points(season):
		season_teams= season['HomeTeam'].unique()
		for team in season_teams:
			col= team+'_points'
			index_team= season[(season['HomeTeam']== team) | \
								(season['AwayTeam']== team) ].index
			shifted= (pd.Series(season[col], index= index_team)).shift(1)
			shifted.fillna(0, inplace= True)
			season[col]= pd.Series(shifted, index= season[col].index)
		return season
	df= df.groupby('Year').apply(shift_points)

	columns= df.columns[8:]
	df[columns]= df.groupby('Year')[columns].cumsum()

	# After creating the desired points column for every team, we must check two 
	# conditions for every match. First: Are the points of two team equal or not?
	# Second: Did the team with less points manage to beat the team with more points?
	# We can save the results of our findings in two different columns for every possible
	# match. 	

	df['Flag']= 0  # flag with the team with less points wins
	df['PointsComparison']= 0 # a binary variable indicating if two teams have different
								# points
	def check_apply_conditions(row):
		HomeTeam= row['HomeTeam'] 
		AwayTeam= row['AwayTeam'] 
		# When HomeTeam has less points
		if row[ HomeTeam+'_points' ] < row[ AwayTeam+'_points']:
			row['PointsComparison']= 1
			# when HomeTeam manages to win despite having less points
			if row['HomeGoals'] > row['AwayGoals']:
				row['Flag']= 1

		# When HomeTeam has more points        
		if row[ HomeTeam+'_points' ] > row[ AwayTeam+'_points']:
			row['PointsComparison']= 1
			# when AwayTeam manages to win despite having less points
			if row['HomeGoals'] < row['AwayGoals']:
				row['Flag']= 1
		return row

	df= df.apply(check_apply_conditions, axis= 1)
	
	# probability= n_desired / n_total
	probability= len(df[df['Flag']!= 0]) / len(df[df['PointsComparison']!= 0])

	print("""The probability that the a team with less points (up to match day) in a season 
beats the team with more points is: \n""")
	return round(probability, 2)

