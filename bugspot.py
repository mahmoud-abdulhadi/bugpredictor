from vcstools import vcs_abstraction 
import re
import pprint
import datetime
import math

import sys

#Regular expression to find bug fixes in Git Commits
fix_regex = re.compile("^.*([B|b]ug)s?|([f|F]ix(es|ed)?|[c|C]lose(s|d)?).*$")


#Get Instance of Git  Version Control system for the sepecifid path
def get_vcs(path = "."):
	vcs = vcs_abstraction.get_vcs('git')
	#Check if there is a git repository in the specified path 
	if vcs.static_detect_presence(path):
		return vcs(path)

	raise Exception("Not Found a valid Git Repository")


#Get Commits that contains bug fixes since days_ago specified 
def get_fix_commits(vcs,branch = 'master',days = 0):
	#vcs = get_vcs()

	def getChanges(days):
			current_branch = vcs.get_current_version_label()
			print(current_branch)
	
	
			#For each commit In the Log ,get The message and The id and The date of the commit
			for log in vcs.get_log():
				(id,message,date) = (log['id'] , log['message'] , log['date'])

				commit_date = date.replace(tzinfo=None)
				#Get The commits that dates are after specified days 
				#And just the commits that matches the regular expresssion of bug fixes
				if commit_date >= days and fix_regex.search(message):
					yield((message,commit_date,vcs.get_affected_files(id)[4:]))

	days_ago = (datetime.datetime.now() - datetime.timedelta(days = days))
	#Return those fixes as list 
	fixes = [] 
	for change in getChanges(days_ago):
		fixes.append(change)

	pprint.pprint(fixes)

	return fixes

#This function returns the difference between two dates in seconds
def time_diff(date1 , date2):
	time_delta = date1 - date2 

	return float(time_delta.minutes+ time_delta.seconds / 1e6)



#Returns a generator of the files that are predicted to be bug prones
def get_code_hotspots(vcs,days = 0,branch = 'master',limit = 10):

	
	commits = get_fix_commits(vcs,branch , days)

	if not commits : 
		print('Not Found comits matching the search cretiria')
		sys.exit(1)

	#Get The Recent commit
	(last_message,last_date,last_files) = commits[-1]
	#Get The current moment 
	current_date = datetime.datetime.now()


	#Dictionary that contains files with scores and dates
	#dictionary key is filename and values are tuples of
	#score and last date of bug fix commit on that file
	hotspots = {}

	for message,date,files in commits : 
		#Difference between current moment and date of commit 
		this_commit_diff = time_diff(current_date,date)
		#print(this_commit_diff)
		#Difference between current moment and the Recent date of commit
		last_commit_diff = time_diff(current_date , last_date)
		#print(last_commit_diff)
		
		#this serves as time stamp of each commit 
		factor = this_commit_diff / last_commit_diff

		#make the old commits gets close to 0 
		factor = 1 - factor

		for file_name in files : 
			
			if file_name not in hotspots : 
				hotspots[file_name] = (0,date) 

			#The Score given to each file based on the timestamp of the commit
			hotspot_factor = 1/(1+math.exp((-12 * factor) + 12))

			old_score = hotspots[file_name][0]
			#Accumulate The scores of each commit on that file
			hotspots[file_name] = (old_score + hotspot_factor,hotspots[file_name][1])

	#print(hotspots)
		#for key in hotspots : 

		#	print('%s : %s'%(key , hotspots[key]))

	#Sort The results Descendantly by The score of each file
	sorted_hotspots  = sorted(hotspots , key = hotspots.get , reverse = True)

	print('\nHotspots\n%s\n' %('-' *80))

	for key in sorted_hotspots[:limit] : 
		#print('%s 	: %.5f : 	%s'%(key,hotspots[key][0],hotspots[key][1]))
		yield(key,hotspots[key][0],hotspots[key][1])



#Print The Results 
#Parameters 
#limit : how many files to display in the list 
#days : specify how many days to go back 
#branch : which version of the software , the default is master
def print_code_hotspots(days,branch ='master',limit = 10):
	vcs = get_vcs()
	for file_name,score,last_date in get_code_hotspots(vcs,days):
		print('%s 	: %.5f : 	%s'%(file_name,score,last_date))




if __name__ == '__main__' : 
	print_code_hotspots(days = 30)



#get_fix_commits(days = 25)

#get_code_hotspots(days = 25)


#vcs = get_vcs()


#current_branch = vcs.get_current_version_label()

#print(current_branch)


#for log in vcs.get_log():
#	(message,id,date) = (log['message'],log['id'],log['date'])

#	files = vcs.get_affected_files(id)

#pprint.pprint(files)



#def get_evens(n):
#	for i in range(n):
#		if i % 2 == 0 : 
#			yield(i)


#for num in get_evens(10):
#	print(num)













