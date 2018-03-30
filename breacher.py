import requests #module for making request to a webpage
import threading #module for multi-threading
import argparse #module for parsing command line arguments
parser = argparse.ArgumentParser() #defines the parser
#Arguements that can be supplied
parser.add_argument("--path", help="custom path prefix", dest='prefix')
parser.add_argument("--type", help="set the type i.e. html, asp, php", dest='type')
parser.add_argument("--fast", help="uses multithreading", dest='fast', action="store_true")
args = parser.parse_args() #arguments to be parsed
fo = open('output.txt', 'w')
fi = open('domainlist.txt', 'r')
for line in fi:
    print line
    target = line #Gets tarfet from argument
    fo.write("\n\n\n\n\n--------------------------------------------------------------------------\n\n")
    fo.write(line)
    fo.write("-------------------------------------------------------------------------\n\n")
    target = target.replace('https://', '') #Removes https://
    target = target.replace('http://', '') #and http:// from the url
    target = target.replace('/', '') #removes / from url so we can have example.com and not example.com/
    target = 'http://' + target #adds http:// before url so we have a perfect URL now
    if args.prefix != None:
        target = target + args.prefix
    target=target.strip('\n')
    print target
    try:
            r = requests.get(target + '/robots.txt') #Requests to example.com/robots.txt
            if '<html>' in r.text: #if there's an html error page then its not robots.txt
                fo.write( ' Robots.txt not found\n')
            else: #else we got robots.txt
                fo.write( ' Robots.txt found. Check for any interesting entry\n')
                fo.write( r.text)
    except: #if this request fails, we are getting robots.txt
            fo.write( 'Robots.txt not found\n')
            fo.write( "--------------------------------------------------------------------------\n")

    def scan(links):
        sitescan=1
        for link in links: #fetches one link from the links list

         try:
            link = target + link # Does this--> example.com/admin/
            print link

            r = requests.get(link) #Requests to the combined url
            http = r.status_code #Fetches the http response code
            if http == 200: #if its 200 the url points to valid resource i.e. admin panel
                fo.write( '----->>>Admin panel found: %s'% link+'\n')
            elif http == 404: #404 means not found
                fo.write( '%s'% link+'\n')
            elif http == 302: #302 means redirection
                fo.write( '----->>>Potential EAR vulnerability found : ' + link+'\n')
            else:
                fo.write( '%s'% link+'\n')
         except:
             print 'site error'
             sitescan=sitescan+1
             if sitescan>5:
                 return;


    paths = [] #list of paths
    def get_paths(type):
        try:
            with open('paths.txt','r') as wordlist: #opens paths.txt and grabs links according to the type arguemnt
                for path in wordlist: #too boring to describe
                    path = str(path.replace("\n",""))
                    try:
                        if 'asp' in type:
                            if 'html' in path or 'php' in path:
                                pass
                            else:
                                paths.append(path)
                        if 'php' in type:
                            if 'asp' in path or 'html' in path:
                                pass
                            else:
                                paths.append(path)
                        if 'html' in type:
                            if 'asp' in path or 'php' in path:
                                pass
                            else:
                                paths.append(path)
                    except:
                        paths.append(path)
        except IOError:
            fo.write("\Wordlist not found!")
            quit()

    if args.fast == True: #if the user has supplied --fast argument
                    type = args.type #gets the input from --type argument
                    get_paths(type) #tells the link grabber to grab links according to user input like php, html, asp
                    paths1 = paths[:len(paths)/2] #The path/links list gets
                    paths2 = paths[len(paths)/2:] #divided into two lists
                    def part1():
                        links = paths1 #it is the first part of the list
                        scan(links) #calls the scanner
                    def part2():
                        links = paths2 #it is the second part of the list
                        scan(links) #calls the scanner
                        t1 = threading.Thread(target=part1) #Calls the part1 function via a thread
                        t2 = threading.Thread(target=part2) #Calls the part2 function via a thread
                        t1.start() #starts thread 1
                        t2.start() #starts thread 2
                        t1.join() #Joins both
                        t2.join() #of the threads
    else: #if --fast isn't supplied we go without threads
                        type = args.type
                        get_paths(type)
                        links = paths
                        scan(links)
fi.close()
fo.close()
