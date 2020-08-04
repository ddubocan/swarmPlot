import pandas as pd
import argparse
import numpy as np 
import sys
import matplotlib.pyplot as plt




class Data:
	def arguments():
		'''Take as input each sqanti gtf file for each technology type.'''
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
		print('Reading file {}, using column number {} for categories and column number {} for numerical variables...'.format((args.file), str(args.categoriesColumn), str(args.numericalColumn)))
		data = args.file
		catCol = args.categoriesColumn
		numCol = args.numericalColumn

		if args.filetype == 'csv':
			df  = pd.read_csv(data)
			df = df.iloc[:, np.r_[catCol-1, numCol-1]]
			df.dropna(inplace = True)

		if args.filetype == 'tsv':
			df = pd.read_table(data, delim_whitespace = True)
			df = df.iloc[:, np.r_[catCol-1, numCol-1]]
			df.dropna(inplace = True)
			print(df.head)


		if args.filetype == 'excel':
			df = pd.read_excel(data, sheet_name = args.sheetIndex, usecols = [catCol,numCol], dtype = {catCol: str, numCol: np.float64})










def main():
	args = Data.arguments()


	Data.reader(args)






main()