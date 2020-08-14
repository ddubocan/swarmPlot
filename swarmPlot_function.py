import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

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
			markerSize = 0.7
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

			#plot medianlines


