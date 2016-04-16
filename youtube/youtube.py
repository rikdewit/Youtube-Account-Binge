import urllib, json
import config
import webbrowser
import sys,os






def getid(Username):
    global urlforid
    global f_forid
    global uploadsid
    global data
    print Username + '3'

    urlforid = 'https://www.googleapis.com/youtube/v3/channels?part=contentDetails&forUsername=%s&key=%s' % (
    Username, config.Api)


    f_forid = connect(urlforid)

    if haveconnection:
        try:
            uploadsid = json.loads(f_forid)['items'][0]['contentDetails']['relatedPlaylists']['uploads']
            data = 1
            return 1
        except(IndexError):
            print 'there seems to be nothing here!'
            data = 0
    else:
        data = 0

def getuploads():
    global completedRetrieve

    open(config.titlesFile, 'w').close()
    open(config.linksFile, 'w').close()
    t = open(config.titlesFile, 'a+')
    l = open(config.linksFile, 'a+')

    if haveconnection & data:

        urlforuploads = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId=%s&maxResults=%s&key=%s" % (
        uploadsid, config.maxResults, config.Api)

        f_foruploads = connect(urlforuploads)

        i = 0
        retrieving = 1
        while retrieving:
            if not haveconnection:
                completedRetrieve = 0
                break

            try:

                    title = json.loads(f_foruploads)['items'][i]['snippet']['title']
                    link = json.loads(f_foruploads)['items'][i]['snippet']['resourceId']['videoId']
            except(IndexError):
                try:
                    nextPageToken = json.loads(f_foruploads)['nextPageToken']
                    print nextPageToken
                except(KeyError):
                    print 'no nextPageToken'
                    completedRetrieve = 1
                    print completedRetrieve
                    break

                urlforuploads = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId=%s&maxResults=%s&pageToken=%s&key=%s" % (
                uploadsid, config.maxResults, nextPageToken, config.Api)

                f_foruploads = connect(urlforuploads)


                i = 0

            t.write(title.encode('utf8') + '\n')
            l.write(link.encode('utf8') + '\n')




            i += 1





def connect(url):
    global haveconnection
    try:
        f = urllib.urlopen(url).read()
        haveconnection = 1
        return f
    except(IOError):
        haveconnection = 0
        print 'no internet connection'
        return 0

def linkVideo(index):
    for i,link in enumerate(open(config.linksCache,'r')):
        if i == index:
            url = 'youtube.com/watch?v={}'.format(link.strip())
            webbrowser.get("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s").open(url)


