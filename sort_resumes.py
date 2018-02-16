from astropy.io import ascii
import numpy as np



class stud_resumes:

    def __init__(self,filename='completed_applications_truncated.csv',outf='matched_people',reviewers=2):

        self.fname = filename
        self.oname = outf
        self.advisors = {} #project dictionary that calls lis to advisors
        self.revnumbs = reviewers #number of people reviewing a given resume
        self.alladvis = [] #list of each advisor
        self.classadv = {} #dictionary containing class for each advisor
        self.classreu = {} #dictionary containing class for each reu student

    def read_file(self):

#set up so it reads directly from download (i.e. ignoring none standard characters

        self.fstri = open(self.fname,'r')
        itxt = self.fstri.readlines() #should be all one line due to formating
        otxt = itxt[0].decode("utf-8",'replace').encode("windows-1252",'replace').decode("utf-8",'replace').replace(u'\ufffd','') #decode('utf-8','ignore')
       
       

        self.fdata = ascii.read(otxt,guess=False,delimiter=',')
        self.columns = self.fdata.colnames

    def uniq_projects(self):
        projects = [] # create a projects list
        for i in self.columns[1:]: #skip the first column because I'll assume that is always the reu's name
            for j in self.fdata[i]: projects.append(j)
        self.projects = np.unique(projects) # get all unique projects
        
    def dict_adv(self): #create a dictionary of advisors for a given project
        for i in self.projects: #loop overall projects
            proinfo = i.split('(') # assume advisors names are in parathensis
            #Add replace statements here as needed to include more people for review
            advisor = proinfo[-1].replace('Shen and Raymond','Shen and Raymond and Prchlik').replace(')','').replace('"','') #make advisor list for given project. staticed in replacements 
            advisor = np.array(advisor.split(' and ')) #put advisor text into numpy array

            self.advisors[i] = advisor #have it so projects call advisors from dictionary
            for k in advisor: self.alladvis.append(k) #make a list of advisors,
        self.alladvis = np.unique(self.alladvis) #get all uniq advisors (in the counting sense)

    def make_adv(self): #make advisor class for each advisor 
        for i in self.alladvis: self.classadv[i] = adv(i)

    def make_reu(self): #make reu class for each student
        for j,i in enumerate(self.fdata[self.columns[0]]): self.classreu[i] = reu(i,self.fdata[j],self.revnumbs)

    def run_seperator(self):
        self.read_file()
        self.uniq_projects()
        self.dict_adv()
        self.make_adv()
        self.make_reu()
        



#advisor class which counts number of resumes currently reviewing and whose
class adv:

    def __init__(self,name):
        self.title = name
        self.students = []
        self.reviewing = 0 #Number of students currently reviewing

#add reu student to list
    def add_reu(self,student):
        self.students.append(student)
        self.reviewing += 1

#remove reu student from list
    def rem_reu(self,student):
        self.students.remove(student)
        self.reviewing -= 1

#reu applicant class which states the projects intestest and number of times reviewed
class reu:
    def __init__(self,name,projects,look):
        self.name = name
        self.proj = projects
        self.look = look #number of looks each student gets
        self.revs = [] #list of people reviewing the student

#Add reviewer to reu object and subtract 1 from the number of remaining looks
    def add_rev(self,reviewer):
        self.revs.append(reviewer)
        self.look = self.look-1

#Remove reviewer to reu object and add 1 to the number of remaining looks
    def rem_rev(self,reviewer):
        self.revs.remove(reviewer)
        self.look = self.look+1

