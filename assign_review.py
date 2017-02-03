import rest_rand_rev as rrr
import numpy as np
import sys,getopt



def main(argv):
    inargs1 = 'hf:o:r:l'
    snargs1 = inargs1[1:].split(':')
    inargs2 = ['infile','outfile','reviewers','loop'] 

    helpinfo = "assign_review.py is a command line utility which class the class sort_adv"
    helpinfo = helpinfo+"The command line takes four arguments; however, only one is required."
    helpinfo = helpinfo+"The required input is the file with preferences (-f or --infile).\n"
    helpinfo = helpinfo+"python assign_review.py "

    for i in range(len(inargs2)): helpinfo=helpinfo+' -'+snargs1[i]+' <--'+inargs2[i]+'>'
    helpinfo=helpinfo+'\n'


#Descriptive information about each keyword
    argsdes=["A file which you want sorted",
             "The start of the output file (default = matched_people)",
             "The number of people you want reviewing one application (default = 2)",
             "Preferences to loop over separated by commas (default = 1st,2nd)"]

    for i in range(len(inargs2)): helpinfo=helpinfo+' -'+snargs1[i]+' <--'+inargs2[i]+'> :'+argsdes[i]+'\n'

#load user values
    try:
        opts,args = getopt.getopt(argv,inargs1,inargs2)
    except getop.GetoptError:
        print helpinfo
        sys.exit(2)
             

#default output
    outf = "matched_people"
    revs = 2
    loop = "1st,2nd"

    for opt, arg in opts:
        print opt
        if opt == '-h':
            print helpinfo
            sys.exit()

        elif opt in ("-f","--infile"):
            inpf = arg
        elif opt in ("-o","--outfile"):
            outf = arg
        elif opt in ("-r","--reviewers"):
            revs = int(arg)
        elif opt in ("-l","--loop"):
            loop = arg

#    try:
    obj = rrr.sort_adv(filename=inpf,outf=outf,reviewers=revs,loop=loop.split(","))
    obj.run_all()
#    except:
#        print 'Invalid input'
#        print helpinfo






if __name__ == "__main__":
    main(sys.argv[1:])
