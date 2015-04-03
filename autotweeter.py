__author__ = 'leahscott'
import twitter, datetime, sqlite3, os, time
user = 81448449
#get my creds for the twitter authentication
file = open("TwitterCredentials.txt")
cred = file.readline().strip().split(',')
api = twitter.Api(consumer_key=cred[0],consumer_secret=cred[1],access_token_key=cred[2],access_token_secret=cred[3])
statuses = api.GetUserTimeline(user)
#find out what my last status was.
print (statuses[0].text)
#DO THIS FOREVER
while True:
    #retrieve our cred for later use
    api = twitter.Api(consumer_key=cred[0],consumer_secret=cred[1],
              access_token_key=cred[2],access_token_secret=cred[3])
    #the chrome history file is elsewhere, so we'll have to move at some point. Setting up the path so it's ready
    path = r"/Users/leahscott/Library/Application Support/Google/Chrome/Default/"
    #BOOM, change folder
    os.chdir(path)
    #Open that badboy up
    log = open('History', 'rb')
    history = log.read()


    #find out our current location, to check it worked
    retval = os.getcwd()
    print "Current working directory %s" % retval

    #insecure, not sure the console knows what we're doing so re-told it the path. Not sure if both are necessary
    console = sqlite3.connect("/Users/leahscott/Library/Application Support/Google/Chrome/Default/history")
    cursor = console.cursor()
    #find bits that look like a URL. Very temperamental
    urls = cursor.execute("SELECT * FROM urls WHERE url LIKE 'http://%.htm'")
    #print all the URLs you can find. Which is seldom ALL of them.
    for word in urls:
        print(word)
        global usedurl
        #The most recent URL is 7 bits of data in, because of all the weird numbers it couldn't filter out, so set the link
        #we're going to tweet to this link.
        title = word[-6]
        usedurl= word[-7]

    #check we're on the right track by printing the url
    print("Last url equals: " + usedurl)
    #Find out what time it is now (in Coordinated Universal Time)
    timestamp = datetime.datetime.utcnow()

    #Post status update and get the response from Twitter
    response = api.PostUpdate(title + " was the last site visited (" + usedurl + ") at: " + str(timestamp))

    #Print out response text (should be the status update if everything worked)
    print("Status updated to: " + response.text)
    print("success!")
    #Repeat hourly
    time.sleep(3600)