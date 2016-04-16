
def clicked():
    usernameChange()
    if not window1.Ui_window1.hasclicked:

        window1.Ui_window1.thread = AThread()
        window1.Ui_window1.thread.start()






def showTitles():
    t = open(config.titlesFile, 'r')

    if os.stat(config.titlesFile).st_size != 0:
        ui.listWidget.clear()

        for title in t:
            ui.listWidget.addItem(title.strip())



def showTitlesCache():
    for title in open(config.titlesCache, 'r'):
        ui.listWidget.addItem(title.strip())



def cashData():
    t = open(config.titlesFile, 'r')
    l = open(config.linksFile,'r')

    if os.stat(config.titlesFile).st_size != 0:
        Empty(config.titlesCache)
        for title in t:
            open(config.titlesCache, 'a+').write(title)

    if os.stat(config.linksFile).st_size != 0:
        Empty(config.linksCache)
        for link in l:

            open(config.linksCache, 'a+').write(link)






def Empty(dir):
    open(dir, 'w').close()



def linkToVideo(item):

    youtube.linkVideo(ui.listWidget.currentRow())

def usernameChange():

    config.Username = ui.lineEdit.text()
    open('Username.txt').close()

    with open('Username.txt','w') as file:
        file.writelines(config.Username)
    file.close()
    config.Username = ui.lineEdit.text()

    print config.Username





if __name__ == "__main__":
    import sys
    from PyQt4 import QtGui,QtCore
    import window1
    import config
    import youtube
    import os
    import time

    class AThread(QtCore.QThread):
        def __init__(self,parent=None):
            super(AThread,self).__init__(parent)
        def run(self):

            window1.Ui_window1.hasclicked = True
            print config.Username + '2'
            ui.label.setText('Fetching...')
            ui.label.show()
            youtube.getid(config.Username)


            print'showing'
            if youtube.haveconnection:


                youtube.getuploads()
                if not youtube.data:
                    print 'no data'
                    ui.label.setText('No Uploads')
                try:
                    if youtube.completedRetrieve:
                        print 'cash'
                        ui.label.hide()
                        showTitles()
                        cashData()
                    else:
                        ui.label.setText('Failed')
                except(AttributeError):
                    pass
            else:
                ui.label.setText('no connection')
                ui.label.show()



            window1.Ui_window1.hasclicked = False
            return




    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = window1.Ui_window1()
    ui.setupUi(MainWindow)
    MainWindow.show()

    ui.label.hide()
    ui.pushButton.clicked.connect(clicked)
    ui.lineEdit.returnPressed.connect(clicked)


    ui.listWidget.itemClicked.connect(linkToVideo)

    showTitlesCache()
    window1.Ui_window1.hasclicked = False
    ui.lineEdit.setVisible(1)

    with open('Username.txt','r') as file:
        config.Username = file.read()
    file.close()
    ui.lineEdit.setText(config.Username)

    app.setWindowIcon(QtGui.QIcon(config.window1IconFile))








    sys.exit(app.exec_())



