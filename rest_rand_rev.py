import sort_resumes as sr
import numpy as np
from random import randint,shuffle



class sort_adv:

    def __init__(self,filename='completed_applications_truncated.csv',outf='matched_people',reviewers=2,loop=['1st','2nd']):
        self.fname = filename
        self.oname = outf #output file name
        self.revnum = reviewers #number of advisors reviewing each resume
        self.loop = loop
        self.get_info()


    def get_info(self):
        self.obj = sr.stud_resumes(filename=self.fname,outf=self.oname,reviewers=self.revnum)
        self.obj.run_seperator() # run through class which creates advisors and reu students

#loop assignment
    def loop_assign(self):
        for i in self.loop: self.assign(i)



#get list of number of reviews for each advisor
    def rev_count(self,padv):
        countlist = []
        for i in padv: countlist.append(self.obj.classadv[i].reviewing)
        countlist = np.array(countlist)
        return countlist
 

#assign people to their first or second choice (through all loop)
    def assign(self,prior): #prior(ity) of assigning reviewer
         x = np.array(self.obj.classreu.keys())
         ind = np.arange(x.size)
         np.random.shuffle(ind) #shuffles indices in place
         
         x = x[ind] #sort x by shuffled indices

         for i in x: #assign in random order
            proj = self.obj.classreu[i].proj[prior]    
            padv =  self.obj.advisors[proj] #priciple advisiors for REU project

            countlist = self.rev_count(padv) #create list of people each advisor on a project currently reviews

            minrev, = np.where(countlist == np.min(countlist)) # find reviewer with least amount of resumes to review for a given project

            index = randint(0,minrev.size-1) #pick a random number from advisor list who has the least amount of current applicants
            index = minrev[index]

            reviewer = padv[index] 
            self.obj.classreu[i].add_rev(reviewer)
            self.obj.classadv[reviewer].add_reu(self.obj.classreu[i].name)

#redistribute students to make a more even review process
    def res_studs(self):
        alladv = self.obj.alladvis
        countlist = self.rev_count(alladv)

        while np.max(countlist)-np.min(countlist) > 1:

#get the advisors with most and least reviews
            maxrev, =  np.where(countlist == np.max(countlist))
            minrev, =  np.where(countlist == np.min(countlist))

#get random index number from the maximums and the mins
            maxdex = randint(0,maxrev.size-1)
            mindex = randint(0,minrev.size-1)

#get name of old and new reviewer
            oldrev = alladv[maxrev[maxdex]]
            newrev = alladv[minrev[mindex]]
           
#remove last assigned student (will take 2nd choices away fist because order of adding)
            moving_student = self.obj.classadv[oldrev].students[-1]
            self.obj.classadv[oldrev].rem_reu(moving_student)
            self.obj.classreu[moving_student].rem_rev(oldrev)

#assign student to new reviewer
            self.obj.classadv[newrev].add_reu(moving_student)
            self.obj.classreu[moving_student].add_rev(newrev)
         
            countlist = self.rev_count(alladv)

#write matching out to file
    def write_out(self):

        advfile = self.oname+'_advisors.txt'
        reufile = self.oname+'_students.txt'
        
#Reviewer matching
        advout = open(advfile,'w')
        advout.write("{0:25}{1:25}\n".format('advisors','students'))
        for i in self.obj.classadv.keys():
            advout.write("{0:25}".format(i))
            txtadd = ' '
            for j in self.obj.classadv[i].students: txtadd = txtadd+"{0:^25}".format(j)+';' # create string of students
            txtadd = txtadd[:-1]+"\n" # create new line at end of students
            advout.write(txtadd)
        advout.close()

#REU matching
        reuout = open(reufile,'w')
        reuout.write("{1:25}{0:25}\n".format('advisors','students'))
        for i in self.obj.classreu.keys():
            reuout.write("{0:25}".format(i))
            txtadd = ' '
            for j in self.obj.classreu[i].revs: txtadd = txtadd+"{0:^25}".format(j)+';' # create string of reviewers
            txtadd = txtadd[:-1]+"\n" # create new line at end of reviewers
            reuout.write(txtadd)
        reuout.close()
        
           


    def run_all(self):
        self.loop_assign()
        self.res_studs()
        self.write_out()
        



