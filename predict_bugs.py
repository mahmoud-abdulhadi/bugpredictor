from tkinter import * 

from tkinter import ttk 

from tkinter import filedialog

import bugspot

from tkinter import messagebox

class BugPredictor():

	def __init__(self,master):

		self.header_frame = ttk.Frame(master)

		self.limit_opt = 10 
		self.branch_opt = 'master'

		self.days_opt = 0
		self.path_opt = '.'
		self.num_fix_commits = 0
		master.configure(background = '#4588B2')
		self.style = ttk.Style()
		self.style.configure('TFrame',background = '#4588B2')
		self.style.configure('TLabel',background = '#4588B2')
		self.style.configure('TLabel',font = ('Georgia',14),foreground = 'white')
		self.style.configure('Header.TLabel',font = ('Arial',20))
		self.input_frame = ttk.Frame(master)

		self.options_frame = ttk.Frame(master)

		self.output_frame = ttk.Frame(master)

		self.commands_frame = ttk.Frame(master)

		self.logo = PhotoImage(file = 'bug_fix.gif').subsample(4,4)
		#--Fill Header Frame 

		self.header_frame.pack(anchor = 'n',padx = 5 , pady =10)

		ttk.Label(self.header_frame,image = self.logo).grid(row = 0,column = 0,rowspan = 2)
		ttk.Label(self.header_frame, text = 'Hotspot Finder',style = 'Header.TLabel').grid(row = 0 , column = 1,padx = 5,pady = 10)

		ttk.Label(self.header_frame , text = 'This program Gives a list of bug-prone files in a git repository').grid(row = 1 , column = 1,padx = 5,pady = 10 )






		#Fill Input Frame 

		self.input_frame.pack(anchor = 'w',padx = 5,pady =10)
		ttk.Label(self.input_frame,text = 'Path: ').grid(row =0,column = 0,padx = 5,pady = 10)

		
		self.path_var = StringVar()

		path = ttk.Entry(self.input_frame,width = 40, textvariable = self.path_var ).grid(row = 0,column = 1 , columnspan = 2,sticky = 'w',padx = 10)


		ttk.Button(self.input_frame,text = 'Browse',command = self.browse).grid(row = 0 , column = 3,padx = 10)

		# -- Fill Options Frame -- 


		self.options_frame.pack(anchor = 'w',padx = 10,pady = 10)

		ttk.Label(self.options_frame,text = '---------------------------------------options------------------------------------------------').grid(row = 0 , column = 0,columnspan = 6) 

		ttk.Label(self.options_frame,text = 'Limit : ').grid(row = 1,column = 0,sticky = 'w',padx=5,pady = 10)
		

		self.limit_var = StringVar()

		self.limit = ttk.Entry(self.options_frame,textvariable = self.limit_var,width  = 4)


		self.limit.grid(row = 1,column = 1,sticky = 'w',padx = 5,pady = 10)
		ttk.Label(self.options_frame,text = 'Days:').grid(row = 1,column = 2,padx = 5,pady = 10)

		self.days_var = StringVar()

		self.days = ttk.Entry(self.options_frame,textvariable = self.days_var,width = 4)
		self.days.grid(row = 1,column = 3,padx  = 5,pady = 10)
		ttk.Label(self.options_frame,text = 'Branch:').grid(row = 1,column = 4,padx = 5,pady = 10)

		self.branch_var = StringVar()

		self.branch = ttk.Entry(self.options_frame,textvariable = self.branch_var)
		self.branch.grid(row = 1,column  =5,padx = 5,pady = 10)
		
		#Fill output Frame --- 
		self.output_frame.pack(anchor = 'w',fill = BOTH , expand = True,padx = 5,pady = 10)
		#Log Frame 

		self.log_frame = ttk.Frame(self.output_frame)

		self.log_frame.pack(anchor = 'w')

		self.log_var = StringVar()

		self.log_var.set('Scanning Repo..')

		self.log_label = ttk.Label(self.log_frame,text = self.log_var.get())
		self.log_label.pack(anchor = 'w')

		self.file_tree_frame = ttk.Frame(self.output_frame)
		self.file_tree_frame.pack(anchor = 'w',fill = BOTH,expand = True)

		self.results = ttk.Treeview(self.file_tree_frame)

		self.results.pack(fill = BOTH , expand = True,padx = 5,pady = 10)

		self.results['columns'] = ('file_name','score','last_commit')

		self.results.heading('#0',text = '#',anchor='w')

		self.results.column("#0", anchor="w",width = 10)

		self.results.heading('file_name', text = 'File Name')

		self.results.column('file_name',anchor = 'w' , width = 200)

		self.results.heading('score',text = 'Score')

		self.results.column('score',anchor = 'w',width = 50)

		self.results.heading('last_commit',text = 'Last Commit')

		self.results.column('last_commit',anchor = 'w',width = 100)
		#Fill commands Frame -- 

		self.commands_frame.pack()

		ttk.Button(self.commands_frame,text = 'Predict',command = self.predict).pack(side = LEFT , anchor = 'w',padx = 5,pady = 10)

		ttk.Button(self.commands_frame,text = 'Reset',command  = self.clear).pack(side = LEFT , anchor = 'e',padx = 5,pady = 10)

		


	def browse(self):
		file = filedialog.askdirectory()

		self.path_var.set(file)

	def clear(self):

		self.path_var.set('')
		self.limit_var.set('')
		self.branch_var.set('')
		self.days_var.set('')

	def predict(self):

		
		for i in self.results.get_children():
			self.results.delete(i)
		if len(self.days_var.get()) > 0 : 
			self.days_opt = int(self.days_var.get())

		if len(self.limit_var.get()) > 0 : 
			self.limit_opt = int(self.limit_var.get())

		if len(self.branch_var.get()) > 0 : 
			self.branch_opt = self.branch_var.get()


		if len(self.path_var.get()) > 0:
			self.path_opt = self.path_var.get()

		try:
			vcs = bugspot.get_vcs(self.path_opt)
		except :
			messagebox.showinfo(title = 'Sorry for Unconvenience' , message = 'Can\'t find a git repository in the specified path')
		
		self.num_fix_commits = len(bugspot.get_fix_commits(vcs,self.branch_opt,self.days_opt))
		self.log_var.set('Scanning %s , Branch = %s\nFound %d bugfix commits in the last %d days'%(self.path_opt,self.branch_opt,self.num_fix_commits,self.days_opt))
		self.log_label.config(text = self.log_var.get())
	
		try : 
			i = 1
			for file_name,score,last_commit in bugspot.get_code_hotspots(vcs,self.days_opt,self.branch_var,self.limit_opt):

				self.results.insert('','end',text = i,values = (file_name,'%0.6f'%(score),last_commit)) 
				i += 1

		except : 
			messagebox.showinfo(title = 'Sorry for Unconvenience' , message = 'No Commits found to satisfy the search Criteria')








def main():

	master = Tk()


	BugPredictor(master)



	master.mainloop()

if __name__ == '__main__' : 
	main()
