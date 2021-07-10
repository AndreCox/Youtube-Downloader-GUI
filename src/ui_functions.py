## ==> GUI FILE
from main import *
import youtube_dl
import os
import validators

## ==> GLOBALS
GLOBAL_STATE = 0
GLOBAL_TITLE_BAR = True
directory = './'
filename = ''
Format = "mp4"



## ==> COUT INITIAL MENU
count = 1

class UIFunctions(MainWindow):

    ## ==> GLOBALS 
    GLOBAL_STATE = 0
    GLOBAL_TITLE_BAR = True
    directory = './'

    ########################################################################
    ## START - GUI FUNCTIONS
    ########################################################################

    ## ==> MAXIMIZE/RESTORE
    ########################################################################
    def maximize_restore(self):
        global GLOBAL_STATE
        status = GLOBAL_STATE
        if status == 0:
            self.showMaximized()
            GLOBAL_STATE = 1
            self.ui.horizontalLayout.setContentsMargins(0, 0, 0, 0)
            self.ui.btn_maximize_restore.setToolTip("Restore")
            self.ui.btn_maximize_restore.setIcon(QtGui.QIcon(u":/16x16/icons/16x16/cil-window-restore.png"))
            self.ui.frame_top_btns.setStyleSheet("background-color: rgb(27, 29, 35)")
            self.ui.frame_size_grip.hide()
        else:
            GLOBAL_STATE = 0
            self.showNormal()
            self.resize(self.width()+1, self.height()+1)
            self.ui.horizontalLayout.setContentsMargins(10, 10, 10, 10)
            self.ui.btn_maximize_restore.setToolTip("Maximize")
            self.ui.btn_maximize_restore.setIcon(QtGui.QIcon(u":/16x16/icons/16x16/cil-window-maximize.png"))
            self.ui.frame_top_btns.setStyleSheet("background-color: rgba(27, 29, 35, 200)")
            self.ui.frame_size_grip.show()

    ## ==> RETURN STATUS
    def returStatus():
        return GLOBAL_STATE

    ## ==> SET STATUS
    def setStatus(status):
        global GLOBAL_STATE
        GLOBAL_STATE = status

    ## ==> ENABLE MAXIMUM SIZE
    ########################################################################
    def enableMaximumSize(self, width, height):
        if width != '' and height != '':
            self.setMaximumSize(QSize(width, height))
            self.ui.frame_size_grip.hide()
            self.ui.btn_maximize_restore.hide()

    ## ==> SET TITLE BAR
    ########################################################################
    def removeTitleBar(status):
        global GLOBAL_TITLE_BAR
        GLOBAL_TITLE_BAR = status

    ## ==> HEADER TEXTS
    ########################################################################
    # LABEL TITLE
    def labelTitle(self, text):
        self.ui.label_title_bar_top.setText(text)

    # LABEL DESCRIPTION
    #def labelDescription(self, text):
    #    self.ui.label_top_info_1.setText(text)

    ## ==> DYNAMIC MENUS
    ########################################################################
    def addNewMenu(self, name, objName, icon, isTopMenu):
        font = QFont()
        font.setFamily(u"Segoe UI")
        button = QPushButton(str(count),self)
        button.setObjectName(objName)
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(button.sizePolicy().hasHeightForWidth())
        button.setSizePolicy(sizePolicy3)
        button.setMinimumSize(QSize(0, 70))
        button.setLayoutDirection(Qt.LeftToRight)
        button.setFont(font)
        button.setStyleSheet(Style.style_bt_standard.replace('ICON_REPLACE', icon))
        button.setText(name)
        button.setToolTip(name)
        button.clicked.connect(self.Button)

        if isTopMenu:
            self.ui.layout_menus.addWidget(button)
        else:
            self.ui.layout_menu_bottom.addWidget(button)


    ## ==> RESET SELECTION
    def resetStyle(self, widget):
        for w in self.ui.frame_left_menu.findChildren(QPushButton):
            if w.objectName() != widget:
                w.setStyleSheet(UIFunctions.deselectMenu(w.styleSheet()))

    ## ==> CHANGE PAGE LABEL TEXT
    def labelPage(self, text):
        newText = '| ' + text.upper()
        self.ui.label_top_info_2.setText(newText)

    def inputURL(self):
        text = self.ui.urlInput.text()
        if (validators.url(text)):
            item = QListWidgetItem(text)
            self.ui.urlList.addItem(item)
            self.ui.urlInput.clear()
            print(text)
        else:
            QMessageBox.information(self, "Warning", "That is not a valid URL")
            self.ui.urlInput.setText('')

    def getDirectory(self):
        global directory
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.Directory)
        if dlg.exec_():
            dirname = dlg.directory()
            directory = dirname.path()
            self.ui.dirPath.setText(directory)
            #f = open(filenames[0], 'r')
            print(directory)

    def onlyAudio(self):
        global Format
        print("Only audio clicked the state is " + str(self.ui.onlyAudio.isChecked()))
        if(self.ui.onlyAudio.isChecked()):
            self.ui.VideoFormat.setVisible(False)
            self.ui.VideoFormatLabel.setVisible(False)
            self.ui.VideoQuality.setVisible(False)
            self.ui.VideoQualityLabel.setVisible(False)

            self.ui.AudioFormat.setVisible(True)
            self.ui.AudioFormatLabel.setVisible(True)
            self.ui.AudioQuality.setVisible(True)
            self.ui.AudioQualityLabel.setVisible(True)
            UIFunctions.formatSetting(self)
        else:
            self.ui.VideoFormat.setVisible(True)
            self.ui.VideoFormatLabel.setVisible(True)
            self.ui.VideoQuality.setVisible(True)
            self.ui.VideoQualityLabel.setVisible(True)

            self.ui.AudioFormat.setVisible(False)
            self.ui.AudioFormatLabel.setVisible(False)
            self.ui.AudioQuality.setVisible(False)
            self.ui.AudioQualityLabel.setVisible(False)
            UIFunctions.formatSetting(self)

    def formatSetting(self):
        global Format
        if(self.ui.onlyAudio.isChecked()):
            Format = self.ui.AudioFormat.currentText().lower()
        else:
            Format = self.ui.VideoFormat.currentText().lower()
        print("The format is now " + Format)


    def download(self):
        global directory
        print (self.ui.urlList.count())
        if (self.ui.urlList.count() < 1 and self.ui.urlInput.text() == ''):
            QMessageBox.information(self, "Warning", "You must enter one or more URL's to download")
            return
        if (not validators.url(self.ui.urlInput.text()) and self.ui.urlInput.text() != ''):
            print("fails here")
            QMessageBox.information(self, "Warning", "That is not a valid URL")
            self.ui.urlInput.setText('')
            return
        print("Download Starting!")
        if (self.ui.urlInput.text() != ''):
            self.ui.urlList.addItem(self.ui.urlInput.text())
            self.ui.urlInput.setText('')
        if (directory == ''):
            directory = './'
        print(self.ui.urlList.count())
        global progress_bar
        global extra_info
        progress_bar = self.ui.progressBar
        extra_info = self.ui.ExtraInfo
        if(self.ui.onlyAudio.isChecked()):
            quality = self.ui.AudioQuality.currentText().lower()
            ydl_opts = {'format': quality + 'audio', 
                        'progress_hooks': [UIFunctions.my_hook],
                        'outtmpl': directory + '/%(title)s-%(id)s.%(ext)s',
                        'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': Format,
                        'preferredquality': '192',
                        }],
                        }
        else:           
            quality = self.ui.VideoQuality.currentText().lower()
            ydl_opts = {'format': quality, 
                        'progress_hooks': [UIFunctions.my_hook],
                        'outtmpl': directory + '/%(title)s-%(id)s.%(ext)s',
                        'postprocessors': [{
                        'key': 'FFmpegVideoConvertor',
                        'preferedformat': Format,  # one of avi, flv, mkv, mp4, ogg, webm
                        }],
                        }

        print (directory)
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            for x in range(0, self.ui.urlList.count()):
                print(self.ui.urlList.item(x).text)
                ydl.download([self.ui.urlList.item(x).text()])
    def my_hook(d):
        if d['status'] == 'finished':
            extra_info.setText("Done Downloading " + os.path.splitext(d['filename'])[0] + "." + str(Format))
            
        if d['status'] == 'downloading':
            p = d['_percent_str']
            p = p.replace('%','')
            last = p.partition(' ')[-1]
            if (last != ''):
                last_f = float(last)
            else:
                last_f = 100.0
            progress_bar.setValue(int(last_f))          
            extra_info.setText("Downloading " + os.path.splitext(d['filename'])[0] + "." + str(Format))
            
            print(d['filename'], d['_percent_str'], d['_eta_str'])    
    

    def myListWidgetContext(self,position):
       #Popup menu
       popMenu = QMenu()
       creAct =QAction("New Group",self)
       delAct =QAction("Delete group",self)
       renameAct =QAction(u'Rename', self)
       #Check if it is on the item when you right-click, if it is not, delete and modify will not be displayed.
       popMenu.addAction(creAct)
       if self.leftWidget.itemAt(position):
           popMenu.addAction(delAct)
           popMenu.addAction(renameAct)

       creAct.triggered.connect(self.CreateNewItem)
       renameAct.triggered.connect(self.RenameItem)
       delAct.triggered.connect(self.DeleteItem)
       popMenu.exec_(self.leftWidget.mapToGlobal(position))   

    ########################################################################
    ## END - GUI FUNCTIONS
    ########################################################################


    ########################################################################
    ## START - GUI DEFINITIONS
    ########################################################################

    ## ==> UI DEFINITIONS
    ########################################################################
    def uiDefinitions(self):

        #QTextedit.setBackgroundColor(QtGui.QColor(255, 255, 255, 70)) 
        def dobleClickMaximizeRestore(event):
            # IF DOUBLE CLICK CHANGE STATUS
            if event.type() == QtCore.QEvent.MouseButtonDblClick:
                QtCore.QTimer.singleShot(250, lambda: UIFunctions.maximize_restore(self))

        ## REMOVE ==> STANDARD TITLE BAR
        if GLOBAL_TITLE_BAR:
            self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
            self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            self.ui.frame_label_top_btns.mouseDoubleClickEvent = dobleClickMaximizeRestore
        else:
            self.ui.horizontalLayout.setContentsMargins(0, 0, 0, 0)
            self.ui.frame_label_top_btns.setContentsMargins(8, 0, 0, 5)
            self.ui.frame_label_top_btns.setMinimumHeight(42)
            self.ui.frame_icon_top_bar.hide()
            self.ui.frame_btns_right.hide()
            self.ui.frame_size_grip.hide()


        ## SHOW ==> DROP SHADOW
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(17)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 150))
        self.ui.frame_main.setGraphicsEffect(self.shadow)

        ## ==> RESIZE WINDOW
        self.sizegrip = QSizeGrip(self.ui.frame_size_grip)
        self.sizegrip.setStyleSheet("width: 20px; height: 20px; margin 0px; padding: 0px;")

        ### ==> MINIMIZE
        self.ui.btn_minimize.clicked.connect(lambda: self.showMinimized())

        ## ==> MAXIMIZE/RESTORE
        self.ui.btn_maximize_restore.clicked.connect(lambda: UIFunctions.maximize_restore(self))

        ## SHOW ==> CLOSE APPLICATION
        self.ui.btn_close.clicked.connect(lambda: self.close())

        self.ui.urlInput.returnPressed.connect(lambda: UIFunctions.inputURL(self))

        self.ui.urlInput.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.urlInput.customContextMenuRequested[QtCore.QPoint].connect(self.rightMenuShow)

        self.ui.progressBar.setValue(0)

        self.ui.directoryButton.clicked.connect(lambda: UIFunctions.getDirectory(self))

        self.ui.downloadButton.clicked.connect(lambda: UIFunctions.download(self))

        self.ui.onlyAudio.clicked.connect(lambda: UIFunctions.onlyAudio(self))

        self.ui.VideoFormat.currentIndexChanged.connect(lambda: UIFunctions.formatSetting(self))
        self.ui.AudioFormat.currentIndexChanged.connect(lambda: UIFunctions.formatSetting(self))

        #set up quality and format dropdowns
        self.ui.VideoFormat.addItem("MP4")
        self.ui.VideoFormat.addItem("WEBM")
        self.ui.VideoFormat.addItem("FLV")
        self.ui.VideoFormat.addItem("3GP")

        self.ui.AudioFormat.setVisible(False)
        self.ui.AudioFormatLabel.setVisible(False)
        self.ui.AudioQuality.setVisible(False)
        self.ui.AudioQualityLabel.setVisible(False)
        self.ui.AudioFormat.addItem("WAV")
        self.ui.AudioFormat.addItem("M4A")
        self.ui.AudioFormat.addItem("MP3")
        self.ui.AudioFormat.addItem("OGG")
        self.ui.AudioFormat.addItem("AAC")

        self.ui.AudioQuality.addItem("Best")
        self.ui.AudioQuality.addItem("Worst")

        self.ui.VideoQuality.addItem("Best")
        self.ui.VideoQuality.addItem("Worst")
        


        #supported Formats
        #3gp, aac, flv, m4a, mp3, mp4, ogg, wav, webm

        #video Formats
        #mp4, webm, ogg, flv, 3gp

        #audio Formats
        #WAV, M4A, MP3, AAC
    ########################################################################
    ## END - GUI DEFINITIONS
    ########################################################################

