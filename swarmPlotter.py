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



	def reader(args):
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
		df.rename(columns = {0:'categories', 1:'values'} ,inplace = True)

		# subSettedDict = {category: np.random.choice(df.iloc[df.iloc[:,0] == category], size = min([len(df.iloc[df.iloc[:,0]==category]),1000])) 
		# 				for category in categories}









	# def dictionarySubset 














def main():
	args = Data.arguments()


	Data.reader(args)






main()