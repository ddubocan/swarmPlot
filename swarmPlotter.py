import pandas as pd
import argparse
import numpy as np 
import sys
import matplotlib.pyplot as plt




class Data:
	'''Handles inputting and sifting through data into a simpler data structure for plotting. Read in tsc, csv, or excel file
		and optional arguments. Given the two columns of interest, wrangle and parse data into a dictionary subsampled to default 1000 
		numerical values unless different value is specified. '''
	def arguments():
		'''Takes in input arguments from user. Required arguments including providing input file and 
			categories/numerical columns arguments(-c, -n). Input may be tsv, csv, or excel file. 
			Return args object to allow access to different variables downstream.'''
		parser = argparse.ArgumentParser()

		parser.add_argument('file', metavar = 'data file', type=str, help='File containing categorical data. Accepted formats: csv, tst, excel file')

		parser.add_argument('-c', '--categoriesColumn', metavar = 'Categorical variable column', type = int, 
			help = '1 indexed position of the column containing the categorical variable')

		parser.add_argument('-n', '--numericalColumn', metavar = 'Continuous or numerical value column', type = int, 
			help = '1 indexed positio of the column containing the continous or numerical variable')

		parser.add_argument('-type', '--filetype', metavar = 'File type for data. Accepted formats: csv, tsv, excel file', 
			choices = ['tsv', 'csv', 'excel'], type = str, help ='File type. Acceptable options include: tsv, csv, excel')

		parser.add_argument('-sheet', '--sheetIndex', metavar = 'Excel sheetname', default = 0, 
			type =str, help ='Sheetname of choice for plotting, if not entered program will default to plotting data on the first sheet')

		args = parser.parse_args() 
		if args.sheetIndex:
			if args.sheetIndex.isdigit():
				sheetIndex = int(args.sheetIndex)


		return args



	def readFile(args):
		'''Read in data file given options provided by the user. '''
		print('Reading file {}, using column number {} for categories and column number {} for numerical variables...'.format((args.file), str(args.categoriesColumn), str(args.numericalColumn)))
		data = args.file
		catCol = args.categoriesColumn
		numCol = args.numericalColumn

		if args.filetype == 'csv':
			df  = pd.read_csv(data)
			df = df.iloc[:, np.r_[catCol-1, numCol-1]]


		if args.filetype == 'tsv':
			df = pd.read_table(data, delim_whitespace = True)
			df = df.iloc[:, np.r_[catCol-1, numCol-1]]



		if args.filetype == 'excel':
			df = pd.read_excel(data, sheet_name = args.sheetIndex, usecols = [catCol,numCol], dtype = {catCol: str, numCol: np.float64})


		df.dropna(inplace = True)

		categories = df.iloc[:,0].unique()
		# cleanedDf = df.rename(columns = {1:'group', 8:'values'})
		df.columns = ['group', 'values']

		subsettedDict = {}
		for category in categories:
			subsample = np.random.choice(df[df['group']==category]['values'], size = min(len(df[df['group']==category]['values']), 1000))

		
			subsettedDict[category] = subsample


		return subsettedDict







class BeeSwarm():

	def __init__(self, args):
		self.data = datDict 
		self.args = args



	def swarmer(panel, binDictionary, panelWidth, panelHeight, x_range, y_range, color):
		'''Plot the swarm plot. Iterate through every bin number, representing number of raw read support. Subsample 1000 points from 
		the bin number. Iterate through each point in the subsample and plot point if it does not overlap. If it overlaps with a point
		jitter it right, then left, iteratively increasing distance, until it does not overlap.'''
		i = 1
		labelList = []
		for binNumber in binDictionary:
			print('Plotting {}...'.format(binNumber))
			labelList.append(binNumber)
			subsample = binDictionary[binNumber][np.random.choice(binDictionary[binNumber].shape[0], 1000)]
			#subsample a 1000 points from each bin 
			markerSize = 0.8
			#set a markersize that will be used for later calculations
			y = list(subsample) 
			x = [i] * len(y)

			pt_diamater = markerSize* (1/85)
			x_distance, y_distance = (pt_diamater/panelWidth) * x_range, (pt_diamater/panelHeight) * y_range
			#calculate the step distance for the y and x axis that needs to be checked for overlap

			plotted_points = []
			
			for x_value, y_value in zip(x,y): 
				#scale q to calculate color 

				y_overlap = [pt for pt in plotted_points if pt[1] > y_value - y_distance and pt[1] < y_value + y_distance]
				#generate list to check for overlap based on distance calculated from scaled point size

				if not y_overlap:		 
					panel.plot([x_value], [y_value], marker='o', markersize= markerSize, markeredgewidth = 0, 
						mfc=color, linewidth=0, zorder=4, alpha = 1)
					plotted_points.append((x_value,y_value))
					#if no overlap plot and continue
					continue
				else:
					overlap=True 
					n = 1
					#n counter is an iterative counter that represents how far from center do we need to go to plot
					while overlap:
						#keep on looping until plottable
						x_right = x_value + (n*x_distance)
						#how far we have to move to the right
						right_subbin = [pt for pt in plotted_points if pt[0] == x_right]
						overlap_right = [pt for pt in right_subbin if pt[1] > y_value - y_distance and pt[1] < y_value + y_distance]
						#check for points that are overlapping along the new x-coordinate
						if not overlap_right:
							panel.plot([x_right], [y_value], marker='o', markersize=markerSize, markeredgewidth = 0, 
								mfc=color, linewidth=0, zorder=4, alpha = 1)
							plotted_points.append((x_right, y_value))
							#if no overlap, plot
							break
						else:
							#if overlapping on the right side, try plotting on the left side
							x_left = x_value - (n*x_distance)
							left_subbin = [pt for pt in plotted_points if pt[0] == x_left]
							overlap_left = [pt for pt in left_subbin if pt[1] > y_value - y_distance and pt[1] < y_value + y_distance]
							#generate list for overlapping points on the left side
							if not overlap_left:
								panel.plot([x_left], [y_value], marker='o', markersize=markerSize, markeredgewidth = 0, 
									mfc=color,  linewidth=0, zorder=4, alpha = 1)
								plotted_points.append((x_left, y_value))
								#if no overlap, plot
								break
							else:
								#if overlapping on the left side, increase the coefficient to multiply the x-axis shift by 1
								n += 1
								continue

			median = np.median(binDictionary[binNumber])
			#median for each bin of raw read support
			xLow, xHigh = i-0.425, i+0.425
			#x values for plotting median
			panel.plot([xLow, xHigh], [median, median],markersize = 1, linewidth = 1, color='red', zorder=5)
			i += 1
		return panel, labelList











def main():
	args = Data.arguments()


	dataDict = Data.readFile(args)
	BeeSwarm(args, dataDict)





main()