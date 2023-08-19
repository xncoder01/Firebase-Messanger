from PyQt5.QtWidgets import QFileDialog, QMainWindow, QMessageBox, QDialog, QApplication
from PyQt5.QtCore import QMutex, QPropertyAnimation, QRect, QTimer, QThread, Qt
from firebase_admin import initialize_app, db, storage, credentials, firestore
from PyQt5.QtGui import QImage, QPixmap, QMovie, QBrush, QPainter, QColor
from Res.Templates.Registration import Ui_Registration
from Res.Templates.AddFriends import Ui_addFriends
from Res.Templates.Loading import Ui_Loading
from Res.Templates.Capture import Ui_Capture
from Res.Templates.profile import Ui_Profile
from PyQt5 import QtGui, QtCore, QtWidgets
from Res.Templates.Camera import Ui_Camera
from Res.Templates.Login import Ui_Login
# from Res.Templates import Email_sender
from Res.Templates.Home import Ui_Home
from PIL import Image, ImageDraw
from datetime import datetime
import threading
import traceback
import sqlite3
import random
import time
import sys
import cv2
import os
import gc
import re

class RegistrationThread(QThread):
    def __init__(self, parent=None, fname=None, lname=None, email=None, image=None, password=None):
        super(RegistrationThread, self).__init__(parent)
        self.fname=fname
        self.lname=lname
        self.email=email
        self.file=image
        self.password=password

    def run(self):
        UserId = userIdGenerator()
        collectionIds = dbstore.collection("Ids")
        docsIds = collectionIds.document(UserId)
        while docsIds.get().exists:
            UserId = userIdGenerator()
        docsIds.set("")

        collection = dbstore.collection("Users")
        docs = collection.document(self.email)
        with open(self.file, 'rb') as file:
            image_data = file.read()

        data = {
            'First Name':self.fname,
            'Last Name':self.lname,
            'Email':self.email,
            'Image':image_data,
            'UserId':UserId,
            'Password':self.password
        }
        dta = {
            'First Name':self.fname,
            'Last Name':self.lname,
            'Email':self.email,
            'UserId':UserId,
            'Password':self.password
        }
        docs.set(data)
        database.child(UserId).child('Info').set(dta)

class MainThread(QThread):
    signal = QtCore.pyqtSignal(str)

    def __init__(self, argum=None, userid=None, friendUserid=None, msg=None, docs=None):
        super().__init__()
        self.docs = docs
        self.argum = argum
        self.userid = userid
        self.friendUserid = friendUserid
        self.msg = msg
    
    def run(self):
        if self.argum == "image":
            self.imageDownload()
            self.signal.emit("Image Downloaded")
        elif self.argum == "Friends":
            self.allFriends(self.userid)
        elif self.argum == "SendMsg":
            self.senderMsg(self.friendUserid, self.userid, self.msg)
        elif self.argum == "RecvMsg":
            self.receiveMsg(self.friendUserid, self.userid)
        elif self.argum == "Pending":
            self.pending(self.userid, self.friendUserid)

    def pending(self, userid, friendUserid):
        pendings = database.child(friendUserid).child("Messages").child("Receive").child(userid).get()
        if pendings != None:
            for pend in pendings:
                if pendings[pend]['Status'] == "Pending":
                    database.child(friendUserid).child("Messages").child("Receive").child(userid).child(pend).update({'Status':'Seen'})

    def allFriends(self, userid):
        lock.lock()
        try:
            frnds_records = database.child(userid).child("Friends").get()
            if frnds_records != None:
                for frnd in frnds_records.values():
                    curMsg.execute(f"CREATE TABLE IF NOT EXISTS F{frnd['UserId']}(UserId TEXT, Message TEXT, Time TEXT, Status TEXT)")
                    connMsg.commit()

                    now = datetime.now()
                    current_time = now.strftime("%Y:%m:%d:%H:%M:%S:%p").lower()
                    collection = dbstore.collection("Users")
                    query = collection.where(field_path="UserId", op_string="==", value=frnd["UserId"])
                    docs = query.get()
                    curTemp.execute("SELECT Message, Time, Status FROM Friends WHERE UserId=?", [frnd['UserId']])
                    data = curTemp.fetchall()
                    if data == []:
                        curTemp.execute("INSERT INTO Friends VALUES(?, ?, ?, ?, ?)", [frnd["UserId"], f"{docs[0].to_dict().get('First Name')} {docs[0].to_dict().get('Last Name')}", "New Added", current_time, "Seen"])
                        conneTemp.commit()
                        image = f"Res/Images/Friends/{frnd['UserId']}.png"
                        with open(image, 'wb') as file:
                            file.write(docs[0].to_dict().get("Image"))
                            file.close()
                    else:
                        ms = data[0][0]
                        tm = data[0][1]
                        st = data[0][2]
                        curMsg.execute(f"SELECT Message, Time, Status FROM F{frnd['UserId']} ORDER BY Time COLLATE NOCASE ASC")
                        msgs = curMsg.fetchall()
                        if msgs != []:
                            for msg in msgs:
                                ms = msg[0]
                                tm = msg[1]
                                st = msg[2]
                        curTemp.execute(f"""UPDATE Friends SET Message = ? WHERE UserId = '{frnd["UserId"]}'""", [ms])
                        conneTemp.commit()
                        curTemp.execute(f"""UPDATE Friends SET Time = ? WHERE UserId = '{frnd["UserId"]}'""", [tm])
                        conneTemp.commit()
                        curTemp.execute(f"""UPDATE Friends SET Status = ? WHERE UserId = '{frnd["UserId"]}'""", [st])
                        conneTemp.commit()
        finally:
            lock.unlock()
        self.signal.emit("Friend Done")

    def senderMsg(self, friendUserid, userid, msg):
        curMsg.execute(f"CREATE TABLE IF NOT EXISTS F{friendUserid}(UserId TEXT, Message TEXT, Time TEXT, Status TEXT)")
        connMsg.commit()

        now = datetime.now()
        current_time = now.strftime("%Y:%m:%d:%H:%M:%S:%p").lower()

        senddata = {"Msg":msg, "Time":current_time, "Status": "Seen"}
        recvdata = {"Msg":msg, "Time":current_time, "Status": "Pending"}
        database.child(userid).child("Messages").child("Send").child(friendUserid).child(current_time).set(senddata)
        database.child(friendUserid).child("Messages").child("Receive").child(userid).child(current_time).set(recvdata)
        self.signal.emit("Send successfully")

    def receiveMsg(self, friendUserid, userid):
        lock.lock()
        try:
            recvmsg = database.child(userid).child("Messages").child("Receive").child(friendUserid).get()
            if recvmsg != None:
                for msg in recvmsg.values():
                    print(msg)
                    curMsg.execute(f"SELECT Time FROM F{friendUserid} WHERE Time='{msg['Time']}'")
                    check = curMsg.fetchone()
                    if check == None:
                        curMsg.execute(f"INSERT INTO F{friendUserid} VALUES(?, ?, ?, ?)", [friendUserid, msg['Msg'], msg['Time'], msg['Status']])
                        connMsg.commit()
        finally:
            lock.unlock()
        self.signal.emit("Received")

    def imageDownload(self):
        self.image = "Res/Images/self.png"
        with open(self.image, 'wb') as file:
            file.write(self.docs[0].to_dict().get("Image"))
        self.signal.emit("Image Downloaded")

class ManageFriend(QThread):
    signalFriend = QtCore.pyqtSignal(str, str, str)
    signalPending = QtCore.pyqtSignal(str, str, str, str, str)
    signalRequest = QtCore.pyqtSignal(str, str, str, str, str)
    signalWindowStatus = QtCore.pyqtSignal(str, str)

    def __init__(self, parent=None, argum=None, userid=None, search=None, email=None, id=None, em=None):
        super(ManageFriend, self).__init__(parent)
        self.argum = argum
        self.search = search
        self.userid = userid
        self.em = em
        self.id = id
        self.email = email

    def run(self):
        if self.argum == "Request":
            self.Request(self.userid)
        elif self.argum == "Pending":
            self.Pending()
        elif self.argum == "Added":
            self.Added()
        elif self.argum == "UsertoRequest":
            self.UsertoRequest()
        elif self.argum == "CancelRequest":
            self.CancelRequest()
        elif self.argum == "Accept":
            self.Accept()

    def Accept(self):
        now = datetime.now()
        current_time = now.strftime("%Y:%m:%d:%H:%M:%p").lower()
        frienddata = {"UserId":self.id[1:], "Email":self.em, "Time":current_time}
        owndata = {"UserId":self.userid, "Email":self.email, "Time":current_time}
        database.child(self.userid).child("Friends").child(self.id[1:]).set(frienddata)
        database.child(self.id[1:]).child("Friends").child(self.userid).set(owndata)
        database.child(self.userid).child("Pending").child(self.id[1:]).delete()
        database.child(self.id[1:]).child("Request").child(self.userid).delete()

    def CancelRequest(self):
        database.child(self.userid).child("Request").child(self.id[1:]).delete()
        database.child(self.id[1:]).child("Pending").child(self.userid).delete()

    def UsertoRequest(self):
        now = datetime.now()
        current_time = now.strftime("%Y:%m:%d:%H:%M:%p").lower()
        frienddata = {"UserId":self.id[1:], "Email":self.em, "Time":current_time}
        owndata = {"UserId":self.userid, "Email":self.email, "Time":current_time}
        database.child(self.userid).child("Request").child(self.id[1:]).set(frienddata)
        database.child(self.id[1:]).child("Pending").child(self.userid).set(owndata)

    def Request(self, userid):
        all_records = {}
        foundAll = False
        foundFrnd = True
        foundReq = True
        for key, value in database.get().items():
            if key.startswith(self.search):
                foundAll = True
                all_records[key] = value
        if foundAll and all_records != {}:
            for rec in all_records.values():
                if rec["Info"]['UserId'] != userid:
                    if database.child(userid).child("Friends").get() != None:
                        frnds_records = {key: value for key, value in database.child(userid).child("Friends").get().items() if key.startswith(f"{self.search}")}
                        for frnd in frnds_records.values():
                            if frnd["UserId"] == rec['Info']['UserId']:
                                self.signalWindowStatus.emit("all", "Req")
                                self.signalFriend.emit("Req", f"{rec['Info']['First Name']} {rec['Info']['Last Name']}", rec['Info']["UserId"])
                                foundFrnd = False
                    if foundFrnd:
                        if database.child(userid).child("Request").get() != None:
                            req_records = {key: value for key, value in database.child(userid).child("Request").get().items() if key.startswith(f"{self.search}")}
                            for req in req_records.values():
                                if req['UserId'] == rec['Info']['UserId']:
                                    foundReq = False
                                    self.signalWindowStatus.emit("all", "Req")
                                    self.signalRequest.emit("Req", f"{rec['Info']['First Name']} {rec['Info']['Last Name']}", rec['Info']['Email'], rec['Info']['UserId'], "Cancel")
                        if foundReq:
                            self.signalWindowStatus.emit("all", "Req")
                            self.signalRequest.emit("Req", f"{rec['Info']['First Name']} {rec['Info']['Last Name']}", rec['Info']['Email'], rec['Info']['UserId'], "Request")
        else:
            self.signalWindowStatus.emit("not", "Req")

    def Pending(self):
        found = False
        if database.child(self.userid).child("Pending").get() != None:
            pen_records = {}
            for key, value in database.child(self.userid).child("Pending").get().items():
                if key.startswith(self.search):
                    pen_records[key] = value
                    found = True
        if found and pen_records != {}:
            for pen in pen_records.values():
                rec = {key : value for key, value in database.child(pen["UserId"]).child("Info").get().items()}
                self.signalPending.emit("Pen", f"{rec['First Name']} {rec['Last Name']}", f"P{rec['UserId']}", pen['Email'], pen["Time"])
                self.signalWindowStatus.emit("all", "Pen")
        else:
            self.signalWindowStatus.emit("not", "Pen")

    def Added(self):
        found = False
        if database.child(self.userid).child("Friends").get() != None:
            frnds_records = {}
            for key, value in database.child(self.userid).child("Friends").get().items():
                if key.startswith(self.search):
                    frnds_records[key] = value
                    found = True
        if found and frnds_records != {}:
            for frnd in frnds_records.values():
                rec = {key : value for key, value in database.child(frnd["UserId"]).child("Info").get().items()}
                self.signalFriend.emit("Added", f"{rec['First Name']} {rec['Last Name']}", rec['UserId'])
                self.signalWindowStatus.emit("all", "Added")
        else:
            self.signalWindowStatus.emit("not", "Added")

def mask_image(imgdata):
    image = QImage.fromData(imgdata, imgdata[-3:])
    image = image.convertToFormat(QImage.Format_ARGB32)
    imgsize = min(image.width(), image.height())
    rect = QRect(
        (image.width() - imgsize) // 2,
        (image.height() - imgsize) // 2,
        imgsize,
        imgsize
    )
    cropped_image = image.copy(rect)
    out_img = QImage(imgsize, imgsize, QImage.Format_ARGB32)
    out_img.fill(QColor(0, 0, 0, 0))
    painter = QPainter(out_img)
    brush = QBrush(cropped_image)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setBrush(brush)
    painter.setPen(Qt.NoPen)
    painter.drawEllipse(0, 0, imgsize, imgsize)
    painter.end()
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    screen = app.primaryScreen()
    pr = screen.devicePixelRatio()
    max_size = min(screen.size().width(), screen.size().height()) * pr
    scale_factor = min(1.0, max_size / imgsize)
    scaled_img = out_img.scaled(int(imgsize * scale_factor), int(imgsize * scale_factor), Qt.KeepAspectRatio, Qt.SmoothTransformation)
    pixmap = QPixmap.fromImage(scaled_img)
    return pixmap

def CircleImages(path):
#     # img = Image.open(path)
#     # h,w = img.size
#     # lum_img = Image.new('L',[h,w] ,0)
#     # draw = ImageDraw.Draw(lum_img)
#     # draw.pieslice([(0,0),(h,w)],0,360,fill=255)
#     # img_arr = np.array(img)
#     # lum_img_arr = np.array(lum_img)
#     # final_img_arr = np.dstack((img_arr, lum_img_arr))
#     # Image.fromarray(final_img_arr).save("Res/Images/Capture.png")

#     # base_width = 360
#     # image = Image.open('Res/Images/Capture.png')
#     # width_percent = (base_width / float(image.size[0]))
#     # hsize = int((float(image.size[1]) * float(width_percent)))
#     # image = image.resize((base_width, hsize), PIL.Image.ANTIALIAS)
#     # image.save('Res/Images/Capture.png')

    # Load the image
    image = Image.open(path)
    width, height = image.size

    # Create a circular mask
    mask = Image.new('L', (width, height), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, width, height), fill=255)

    # Apply the mask to the image
    result = Image.new('RGBA', (width, height))
    result.paste(image, mask=mask)

    # Save the cropped image
    result.save('Res/Images/Capture.png')

def generateOTP() :
    digits = "0123456789"
    OTP = ''.join([random.choice(digits) for _ in range(6)])
    return OTP

def userIdGenerator() :
    digits = "0123456789"
    USERID = ''.join(random.choices(digits, k=12))
    return USERID

class Registration(QMainWindow):
    def __init__(self):
        gc.collect()
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.ui = Ui_Registration()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.close)
        self.ui.pushButton_2.clicked.connect(self.next)
        self.ui.pushButton_3.clicked.connect(self.signin)
        self.ui.pushButton_4.clicked.connect(self.finish)
        self.ui.pushButton_5.clicked.connect(self.register)
        self.ui.pushButton_6.clicked.connect(self.verify)
        self.ui.pushButton_7.clicked.connect(self.back)
        self.ui.pushButton_8.clicked.connect(self.signin)
        self.ui.pushButton_9.clicked.connect(self.remove)
        self.ui.pushButton_10.clicked.connect(self.add)
        self.ui.pushButton_11.clicked.connect(self.finish)
        self.ui.lineEdit.textChanged.connect(self.page1)
        self.ui.lineEdit_2.textChanged.connect(self.page1)
        self.ui.lineEdit_3.textChanged.connect(self.page1)
        self.ui.lineEdit_4.textChanged.connect(self.page2)
        self.ui.lineEdit_5.textChanged.connect(self.page2)
        self.ui.lineEdit_6.textChanged.connect(self.page2)
        self.ui.pushButton_2.setEnabled(False)
        self.ui.pushButton_4.setEnabled(False)
        self.ui.pushButton_5.setEnabled(False)
        self.ui.pushButton_6.setEnabled(False)
        self.ui.pushButton_7.setEnabled(False)
        self.ui.pushButton_8.setEnabled(False)
        self.ui.pushButton_9.setEnabled(False)
        self.ui.pushButton_10.setEnabled(False)
        self.ui.pushButton_11.setEnabled(False)
        self.frame_animation = QPropertyAnimation(self.ui.frame, b"geometry")
        self.frame2_animation = QPropertyAnimation(self.ui.frame_2, b"geometry")
        self.frame3_animation = QPropertyAnimation(self.ui.frame_3, b"geometry")
        self.frame4_animation = QPropertyAnimation(self.ui.frame_4, b"geometry")
        self.frame5_animation = QPropertyAnimation(self.ui.frame_5, b"geometry")
        self.ui.label_11.setPixmap(QtGui.QPixmap("Res/Images/registration.png"))
        self.ui.label_10.setPixmap(QtGui.QPixmap("Res/Images/temp.png"))
        self.checkemail = None
        self.verified = False
        self.file = "Res/Images/temp.png"

        def moveWindow(e):
            if self.isMaximized() == False:
                if e.buttons() == Qt.LeftButton:
                    self.move(self.pos() + e.globalPos() - self.clickPosition)
                    self.clickPosition = e.globalPos()
                    e.accept()
        self.ui.label_4.mouseMoveEvent = moveWindow

    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()

    def page1(self):
        self.fname = self.ui.lineEdit.text()
        self.lname = self.ui.lineEdit_2.text()
        self.email = self.ui.lineEdit_3.text()
        if self.fname != "":
            self.fname = self.fname[0].upper() + self.fname[1:]
        if self.lname != "":
            self.lname = self.lname[0].upper() + self.lname[1:]
        if self.fname != "" and self.lname != "" and self.email != "":
            self.ui.pushButton_2.setStyleSheet(
                "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0.955, stop:0 rgba(0, 157, 255, 255), stop:0.552239 rgba(12, 188, 207, 255));\n"
                "border-radius:5px;\n"
                "color: rgb(255, 255, 255);\n"
            )
            self.ui.pushButton_2.setEnabled(True)
        else:
            self.ui.pushButton_2.setStyleSheet(
                "border-radius:5px;\n"
                "background-color: rgb(5, 127, 165);\n"
                "color: rgb(185, 185, 185);"
            )
            self.ui.pushButton_2.setEnabled(False)

    def page2(self):
        self.otp = self.ui.lineEdit_4.text()
        self.pass1 = self.ui.lineEdit_5.text()
        self.pass2 = self.ui.lineEdit_6.text()
        if not self.verified:
            if self.otp != "":
                self.ui.pushButton_6.setStyleSheet(
                    "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0.955, stop:0 rgba(0, 157, 255, 255), stop:0.552239 rgba(12, 188, 207, 255));\n"
                    "border-radius:5px;\n"
                    "color: rgb(255, 255, 255);\n"
                )
                self.ui.pushButton_6.setEnabled(True)
            else:
                self.ui.pushButton_6.setStyleSheet(
                    "border-radius:5px;\n"
                    "background-color: rgb(5, 127, 165);\n"
                    "color: rgb(185, 185, 185);"
                )
                self.ui.pushButton_6.setEnabled(False)
        
        if self.pass1 != "" and self.pass2 != "" and self.verified:
            self.ui.pushButton_5.setStyleSheet(
                "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0.955, stop:0 rgba(0, 157, 255, 255), stop:0.552239 rgba(12, 188, 207, 255));\n"
                "border-radius:5px;\n"
                "color: rgb(255, 255, 255);\n"
            )
            self.ui.pushButton_5.setEnabled(True)
        else:
            self.ui.pushButton_5.setStyleSheet(
                "border-radius:5px;\n"
                "background-color: rgb(5, 127, 165);\n"
                "color: rgb(185, 185, 185);"
            )
            self.ui.pushButton_5.setEnabled(False)

    def imgPath(self, path):
        self.file = path
        imgdata = open(self.file, 'rb').read()
        pixmap = mask_image(imgdata)
        self.ui.label_10.setPixmap(pixmap)
        self.image = open(f"{self.file}", "rb")
        if self.file != "Res/Images/temp.png":
            self.ui.pushButton_4.setGeometry(QRect(40, 320, 0, 41))
            self.ui.pushButton_10.setGeometry(QRect(240, 320, 0, 41))
            self.ui.pushButton_4.setEnabled(False)
            self.ui.pushButton_10.setEnabled(False)
            self.ui.pushButton_11.setEnabled(True)
            self.ui.pushButton_9.setEnabled(True)

    def finish(self):
        self.frame_animation.setDuration(500)
        self.frame_animation.setStartValue(QRect(470, 90, 441, 501))
        self.frame_animation.setEndValue(QRect(470, 90, 0, 501))
        self.frame_animation.start()
        self.frame5_animation.setDuration(500)
        self.frame5_animation.setStartValue(QRect(470, 90, 0, 501))
        self.frame5_animation.setEndValue(QRect(470, 90, 441, 501))
        self.frame5_animation.start()
        self.ui.pushButton_8.setEnabled(True)
        self.ui.pushButton_10.setEnabled(False)
        self.ui.pushButton_11.setEnabled(False)
        self.ui.pushButton_4.setEnabled(False)
        self.ui.pushButton_9.setEnabled(False)
        # threading.Thread(target=Email_sender.register_sender, args=(self.email, f"{self.fname} {self.lname}"))
        self.th = RegistrationThread(fname=self.fname, lname=self.lname, email=self.email, image=self.file, password=self.pass1)
        self.th.start()

    def back(self):
        animbtn = QPropertyAnimation(self.ui.pushButton_6, b"geometry")
        animbtn.setDuration(0)
        animbtn.setEndValue(QRect(290, 20, 111, 31))
        animbtn.start()
        self.verified = False
        self.ui.pushButton_5.setEnabled(False)
        self.ui.pushButton_6.setEnabled(False)
        self.ui.pushButton_7.setEnabled(False)
        self.ui.pushButton_2.setEnabled(True)
        self.ui.pushButton_3.setEnabled(True)
        self.ui.lineEdit_4.setReadOnly(False)
        self.checkemail = self.email
        self.frame2_animation.setDuration(500)
        self.frame2_animation.setStartValue(QRect(0, 90, 0, 411))
        self.frame2_animation.setEndValue(QRect(0, 90, 441, 411))
        self.frame2_animation.start()
        self.frame3_animation.setDuration(500)
        self.frame3_animation.setStartValue(QRect(0, 90, 441, 411))
        self.frame3_animation.setEndValue(QRect(0, 90, 0, 411))
        self.frame3_animation.start()
        del animbtn

    def signin(self):
        self.lg = Login()
        self.lg.show()
        self.close()
        del self.lg, self.checkemail, self.file, self.fname, self.lname, self.email, self.otp, self.pass1, self.pass2
        self.th = None
        self.clickPosition = None
        self.cp = None
        self.generateOtp = None

    def add(self):
        self.cp = ImageCapture()
        self.cp.img.connect(self.imgPath)
        self.cp.exec_()
        self.cp = None

    def remove(self):
        self.ui.pushButton_11.setEnabled(False)
        self.ui.pushButton_9.setEnabled(False)
        self.ui.pushButton_10.setEnabled(True)
        self.ui.pushButton_4.setEnabled(True)
        self.ui.pushButton_4.setGeometry(QRect(40, 320, 161, 41))
        self.ui.pushButton_10.setGeometry(QRect(240, 320, 161, 41))
        self.file = "Res/Images/temp.png"
        imgdata = open(self.file, 'rb').read()
        pixmap = mask_image(imgdata)
        self.ui.label_10.setPixmap(pixmap)
        self.image = open(f"{self.file}", "rb")

    def verify(self):
        if self.generateOtp == self.otp:
            self.verified = True
            animbtn = QPropertyAnimation(self.ui.pushButton_6, b"geometry")
            animbtn.setDuration(0)
            animbtn.setEndValue(QRect(290, 20, 0, 31))
            animbtn.start()
            self.ui.lineEdit_4.setReadOnly(True)
            self.ui.pushButton_6.setEnabled(False)
            del animbtn
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Failed")
            msg.setText("OTP does not matched")
            msg.setIcon(QMessageBox.Critical)
            msg.exec_()
            del msg

    def next(self):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.fullmatch(regex, self.email):
            collection = dbstore.collection("Users")
            docs = collection.document(self.email)
            if docs.get().exists:
                msg = QMessageBox()
                msg.setWindowTitle("Failed")
                msg.setText("Email address already registered")
                msg.setIcon(QMessageBox.Critical)
                msg.exec_()
            else:
                self.ui.lineEdit_4.setText("")
                if self.checkemail != self.email:
                    self.generateOtp = generateOTP()
                    print(self.generateOtp)
                    # threading.Thread(target=Email_sender.sender, args=(self.email, self.generateOtp)).start()
                self.ui.pushButton_2.setEnabled(False)
                self.ui.pushButton_3.setEnabled(False)
                self.ui.pushButton_7.setEnabled(True)
                self.frame2_animation.setDuration(500)
                self.frame2_animation.setStartValue(QRect(0, 90, 441, 411))
                self.frame2_animation.setEndValue(QRect(0, 90, 0, 411))
                self.frame2_animation.start()
                self.frame3_animation.setDuration(500)
                self.frame3_animation.setStartValue(QRect(0, 90, 0, 411))
                self.frame3_animation.setEndValue(QRect(0, 90, 411, 411))
                self.frame3_animation.start()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Failed")
            msg.setText("Invalid Email address")
            msg.setIcon(QMessageBox.Critical)
            msg.exec_()
            del msg

    def register(self):
        if len(self.pass1) > 5:
            if self.pass1 == self.pass2:
                self.frame3_animation.setDuration(500)
                self.frame3_animation.setStartValue(QRect(0, 90, 441, 411))
                self.frame3_animation.setEndValue(QRect(0, 90, 0, 411))
                self.frame3_animation.start()
                self.frame4_animation.setDuration(500)
                self.frame4_animation.setStartValue(QRect(0, 90, 0, 411))
                self.frame4_animation.setEndValue(QRect(0, 90, 441, 411))
                self.frame4_animation.start()
                self.ui.pushButton_4.setEnabled(True)
                self.ui.pushButton_10.setEnabled(True)
                self.ui.pushButton_5.setEnabled(False)
                self.ui.pushButton_6.setEnabled(False)
                self.ui.pushButton_7.setEnabled(False)
            else:
                msg = QMessageBox()
                msg.setWindowTitle("Failed")
                msg.setText("Both password not matched")
                msg.setIcon(QMessageBox.Critical)
                msg.exec_()
                del msg
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Failed")
            msg.setText("At least 6 digit password")
            msg.setIcon(QMessageBox.Critical)
            msg.exec_()
            del msg

class ImageCapture(QDialog):
    img = QtCore.pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.ui = Ui_Capture()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.browse)
        self.ui.pushButton_2.clicked.connect(self.capture)
        self.ui.pushButton_3.clicked.connect(self.close)

        def moveWindow(e):
            if self.isMaximized() == False:
                if e.buttons() == Qt.LeftButton:
                    self.move(self.pos() + e.globalPos() - self.clickPosition)
                    self.clickPosition = e.globalPos()
                    e.accept()
        self.ui.label_2.mouseMoveEvent = moveWindow

    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()

    def imgPath(self, path):
        self.img.emit(path)

    def browse(self):
        self.file = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\',"Image files (*.jpg *.png *.jpeg)")
        self.file = self.file[0]
        if len(self.file) != 0:
            self.img.emit(self.file)
            self.close()

    def capture(self):
        self.cm = Camera()
        self.cm.img.connect(self.imgPath)
        self.close()
        self.cm.exec_()

class Camera(QDialog):
    img = QtCore.pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.ui = Ui_Camera()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.cl)
        self.ui.pushButton_2.clicked.connect(self.cap)
        self.i = 0
        self.j = 0
        self.k = 0
        self.a = 0

        self.t = threading.Thread(target=self.camera)
        self.t.start()

        self.st = QTimer(self)
        self.st.timeout.connect(self.sto)
        self.st.start()

        def moveWindow(e):
            if self.isMaximized() == False:
                if e.buttons() == Qt.LeftButton:
                    self.move(self.pos() + e.globalPos() - self.clickPosition)
                    self.clickPosition = e.globalPos()
                    e.accept()
        self.ui.label_3.mouseMoveEvent = moveWindow

    def displayImage(self, img, window=1):
        qformat = QImage.Format_Indexed8
        if len(img.shape) == 3:
            if (img.shape[2]) == 4:
                qformat = QImage.Format_RGBA888
            else:
                qformat = QImage.Format_RGB888
        img = QImage(img, img.shape[1], img.shape[0], qformat)
        img = img.rgbSwapped()
        self.j = 1
        self.ui.label.setPixmap(QPixmap.fromImage(img))
        self.ui.label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

    def sto(self):
        if self.a == 1:
            self.t.join()
            self.img.emit("Res/Images/Capture.png")
            self.hide()
            self.st.stop()

    def camera(self):
        cam = cv2.VideoCapture(0)
        while True:
            res, img = cam.read()
            self.displayImage(img, 1)
            if self.j == 1:
                animation1 = QPropertyAnimation(self.ui.label_2, b"geometry")
                animation1.setDuration(0)
                animation1.setEndValue(QRect(210, 240, 0, 51))
                animation1.start()

            if self.k == 1:
                cv2.imwrite("Res/Images/Capture.png", img)
                CircleImages("Res/Images/Capture.png")
                self.a = 1
                break

            if self.i == 1:
                break
            cv2.waitKey(0)
        cam.release()
        cv2.destroyAllWindows()

    def cap(self):
        self.k = 1

    def cl(self):
        self.hide()
        self.i = 1

    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()

class Login(QMainWindow):
    def __init__(self):
        gc.collect()
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.ui = Ui_Login()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.close)
        self.ui.pushButton_2.clicked.connect(self.login)
        self.ui.pushButton_3.clicked.connect(self.signup)
        lineditlistener = QTimer(self)
        lineditlistener.timeout.connect(self.LineEditListener)
        lineditlistener.start()
        self.load = Loading()
        
        def moveWindow(e):
            if self.isMaximized() == False:
                if e.buttons() == Qt.LeftButton:
                    self.move(self.pos() + e.globalPos() - self.clickPosition)
                    self.clickPosition = e.globalPos()
                    e.accept()
        self.ui.label_3.mouseMoveEvent = moveWindow

    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()

    def LineEditListener(self):
        self.email = self.ui.lineEdit.text()
        self.passwd = self.ui.lineEdit_2.text()
        if self.email != "" and self.passwd != "":
            self.ui.pushButton_2.setStyleSheet(
                "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0.955, stop:0 rgba(0, 157, 255, 255), stop:0.552239 rgba(12, 188, 207, 255));\n"
                "border-radius:5px;\n"
                "color: rgb(255, 255, 255);\n"
            )
            self.ui.pushButton_2.setEnabled(True)
        else:
            self.ui.pushButton_2.setStyleSheet(
                "border-radius:5px;\n"
                "background-color: rgb(5, 127, 165);\n"
                "color: rgb(185, 185, 185);"
            )
            self.ui.pushButton_2.setEnabled(False)

    def login(self):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.fullmatch(regex, self.email):
            collection = dbstore.collection("Users")
            docs = collection.document(self.email)
            if docs.get().exists:
                query = collection.where(field_path="Email", op_string="==", value=self.email)
                docs = query.get()
                if len(docs) > 0 and self.passwd == docs[0].to_dict().get("Password"):
                    msg = QMessageBox()
                    msg.setWindowTitle("Done")
                    msg.setText("Login successfully")
                    msg.setIcon(QMessageBox.Information)
                    msg.exec_()
                    try:
                        curTemp.execute(f"SELECT Email FROM TempUser")
                        us1 = curTemp.fetchall()[0]
                        curTemp.execute(f"UPDATE TempUser SET UserId = ? WHERE Email = '{us1[0]}'", [docs[0].to_dict().get("UserId")])
                        conneTemp.commit()
                        curTemp.execute(f"UPDATE TempUser SET Email = ? WHERE Email = '{us1[0]}'", [self.email])
                        conneTemp.commit()
                        del us1
                    except:
                        curTemp.execute("INSERT INTO TempUser VALUES(?, ?)", [docs[0].to_dict().get("UserId"), self.email])
                        conneTemp.commit()
                    self.hm = Main()
                    self.hm.show()
                    self.close()
                    del msg
                    del self.hm
                else:
                    msg = QMessageBox()
                    msg.setWindowTitle("Failed")
                    msg.setText("Incorrect Password")
                    msg.setIcon(QMessageBox.Critical)
                    msg.exec_()
                    del msg
            else:
                msg = QMessageBox()
                msg.setWindowTitle("Failed")
                msg.setText("Email does not registered")
                msg.setIcon(QMessageBox.Critical)
                msg.exec_()
                del msg
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Failed")
            msg.setText("Invalid Email Address")
            msg.setIcon(QMessageBox.Critical)
            msg.exec_()
            del msg

    def signup(self):
        self.rg = Registration()
        self.rg.show()
        self.close()
        del self.rg
        self.loading = None
        self.clickPosition = None
        del self.email
        del self.passwd

class Main(QMainWindow):
    messageSignal = QtCore.pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.ui = Ui_Home()
        self.ui.setupUi(self)
        self.icon = QtGui.QIcon()
        self.icon1 = QtGui.QIcon()
        self.icon2 = QtGui.QIcon()
        self.icon3 = QtGui.QIcon()
        self.icon4 = QtGui.QIcon()
        self.icon5 = QtGui.QIcon()
        self.icon6 = QtGui.QIcon()
        self.icon7 = QtGui.QIcon()
        self.icon8 = QtGui.QIcon()
        self.icon9 = QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap("Res/Templates/img/plus1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.icon1.addPixmap(QtGui.QPixmap("Res/Templates/img/menu1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.icon2.addPixmap(QtGui.QPixmap("Res/Templates/img/person.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.icon3.addPixmap(QtGui.QPixmap("Res/Templates/img/attach.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.icon4.addPixmap(QtGui.QPixmap("Res/Templates/img/send1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.icon5.addPixmap(QtGui.QPixmap("Res/Templates/img/plus1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.icon6.addPixmap(QtGui.QPixmap("Res/Templates/img/logout.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.icon7.addPixmap(QtGui.QPixmap("Res/Templates/img/close.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.icon8.addPixmap(QtGui.QPixmap("Res/Templates/img/restore.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.icon9.addPixmap(QtGui.QPixmap("Res/Templates/img/minimize.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.pushButton.setIcon(self.icon1)
        self.ui.pushButton_2.setIcon(self.icon5)
        self.ui.pushButton_3.setIcon(self.icon1)
        self.ui.pushButton_4.setIcon(self.icon4)
        self.ui.pushButton_5.setIcon(self.icon3)
        self.ui.pushButton_6.setIcon(self.icon2)
        self.ui.pushButton_7.setIcon(self.icon2)
        self.ui.pushButton_8.setIcon(self.icon6)
        self.ui.pushButton_9.setIcon(self.icon7)
        self.ui.pushButton_10.setIcon(self.icon8)
        self.ui.pushButton_11.setIcon(self.icon9)
        
        self.ui.pushButton_2.clicked.connect(self.addFriend)
        self.ui.pushButton_4.clicked.connect(self.Send)
        self.ui.pushButton_7.clicked.connect(self.profileview)
        self.ui.pushButton_8.clicked.connect(self.logout)
        self.ui.pushButton_9.clicked.connect(self.close)
        self.ui.pushButton_10.clicked.connect(self.restore)
        self.ui.pushButton_11.clicked.connect(self.showMinimized)
        self.ui.listWidget.itemSelectionChanged.connect(self.selectionChanged)
        
        self.friendlist = []
        self.initialize()
        self.movie = QMovie("Res/Images/loading.gif")
        self.ui.label_7.setMovie(self.movie)
        self.movie.start()
        self.loading = True
        self.messageSignal.connect(self.Messages)

        self.gripSize = 16
        self.grips = []
        for _ in range(4):
            grip = QtWidgets.QSizeGrip(self)
            grip.resize(self.gripSize, self.gripSize)
            self.grips.append(grip)

        def moveWindow(e):
            if self.isMaximized() == False:
                if e.buttons() == Qt.LeftButton:
                    self.move(self.pos() + e.globalPos() - self.clickPosition)
                    self.clickPosition = e.globalPos()
                    e.accept()
        self.ui.frame_26.mouseMoveEvent = moveWindow

    def checkData(self):
        if self.loading:
            self.ui.frame_32.setMaximumHeight(16777215)
            self.ui.scrollArea.setMaximumHeight(0)
        else:
            self.ui.frame_32.setMaximumHeight(0)
            self.ui.scrollArea.setMaximumHeight(16777215)

        try:
            for friend in self.friendlist:
                if friend[1] == self.friendUserid:
                    modelIndex = self.ui.listWidget.model().index(friend[0], 0)
                    self.ui.listWidget.setCurrentIndex(modelIndex)
        except:pass

    def initialize(self):
        curTemp.execute(f"SELECT UserId, Email FROM TempUser")
        us1 = curTemp.fetchall()[0]
        self.userid = us1[0]
        self.email = us1[1]

        frnds = database.child(self.userid).child("Friends").get()
        if frnds != None:
            for frnd in frnds:
                curMsg.execute(f"CREATE TABLE IF NOT EXISTS F{frnd}(UserId TEXT, Message TEXT, Time TEXT, Status TEXT)")
                connMsg.commit()
            userData = database.child(self.userid).child("Messages").child("Send").get()
            if userData != None:
                for userd in userData:
                    for udata in userData[userd]:
                        curMsg.execute(f"select Time from F{userd} where Time=?", [udata])
                        getTime = curMsg.fetchone()
                        if getTime == None:
                            curMsg.execute(f"insert into F{userd} values(?, ?, ?, ?)", [self.userid, userData[userd][udata]['Msg'], userData[userd][udata]['Time'], userData[userd][udata]['Status']])
                            connMsg.commit()
        self.frndlistener = database.child(self.userid).child("Friends").listen(self.Friendlisten)
        self.listener = database.child(self.userid).child("Messages").child("Receive").listen(self.Msglistening)
        self.checkDataUpdate = QTimer(self)
        self.checkDataUpdate.timeout.connect(self.checkData)
        self.checkDataUpdate.start(500)

        collection = dbstore.collection("Users")
        query = collection.where(field_path="Email", op_string="==", value=self.email)
        docs = query.get()
        self.fname = docs[0].to_dict().get("First Name")
        self.lname = docs[0].to_dict().get("Last Name")
        self.email = docs[0].to_dict().get("Email")
        self.userid = docs[0].to_dict().get("UserId")
        self.password = docs[0].to_dict().get("Password")
        self.mainTh = MainThread(argum="image", docs=docs)

        if not self.mainTh.isRunning():
            self.mainTh.start()
        else:
            self.mainTh.wait()
        self.mainTh.signal.connect(self.RunTimeUpdates)

    def RunTimeUpdates(self, check):
        if check == "Image Downloaded":
            self.image = f"Res/Images/self.png"
            imgdata = open(self.image, 'rb').read()
            pixmap = mask_image(imgdata)
            self.ui.label_6.setPixmap(pixmap)
        elif check == "Friend Done":
            self.FriendPanel()
            self.FriendCard()

    def FriendCard(self):
        curTemp.execute("select * from Friends")
        allData = curTemp.fetchall()
        for frnd in allData:
            try:
                if frnd[0] == self.friendUserid:
                    lblT = self.findChild(QtWidgets.QLabel, f"T{frnd[0]}")
                    if lblT != None:
                        lblT.setText(self.DateTime(frnd[3]))
                    lblM = self.findChild(QtWidgets.QLabel, f"M{frnd[0]}")
                    if lblM != None:
                        lblM.setText(frnd[2])
                else:
                    frndM = self.findChild(QtWidgets.QLabel, f"M{frnd[0]}")
                    if frndM != None:
                        frndM.setText(frnd[2])
                    frndT = self.findChild(QtWidgets.QLabel, f"T{frnd[0]}")
                    if frndT != None:
                        frndT.setText(self.DateTime(frnd[3]))
                    curMsg.execute(f"select count(Status) from F{frnd[0]} where Status='Pending'")
                    pen = curMsg.fetchone()
                    frndP = self.findChild(QtWidgets.QLabel, f"P{frnd[0]}")
                    if frndP != None:
                        frndP.setText(str(pen[0]))
            except:
                frndM = self.findChild(QtWidgets.QLabel, f"M{frnd[0]}")
                if frndM != None:
                    frndM.setText(frnd[2])
                frndT = self.findChild(QtWidgets.QLabel, f"T{frnd[0]}")
                if frndT != None:
                    frndT.setText(self.DateTime(frnd[3]))
                curMsg.execute(f"select count(Status) from F{frnd[0]} where Status='Pending'")
                pen = curMsg.fetchone()
                frndP = self.findChild(QtWidgets.QLabel, f"P{frnd[0]}")
                if frndP != None:
                    frndP.setText(str(pen[0]))

    def Friendlisten(self, event):
        try:
            for lblkey in event.data.keys():
                lbls = self.findChild(QtWidgets.QLabel, f"M{lblkey}")
                if lbls == None:
                    curTemp.execute("select UserId, Name, Message, Time, Status from Friends where UserId=?", [lbls])
                    frnd = curTemp.fetchone()
                    if frnd == None:
                        self.th1 = MainThread(argum="Friends", userid=self.userid)
                        if not self.th1.isRunning():
                            self.th1.start()
                        else:
                            self.th1.wait()
                        self.th1.signal.connect(self.RunTimeUpdates)
        except:pass

    def Msglistening(self, event):
        if event.data != None and event.path == "/":
            for frndId in event.data.keys():
                for tm in event.data[frndId].keys():
                    curMsg.execute(f"select Time from F{frndId} where Time=?", [tm])
                    ftTime = curMsg.fetchone()
                    if ftTime == None:
                        curMsg.execute(f"insert into F{frndId} values(?, ?, ?, ?)", [frndId, event.data[frndId][tm]['Msg'], event.data[frndId][tm]['Time'], event.data[frndId][tm]['Status']])
                        connMsg.commit()
                        curTemp.execute("update Friends set Message=? where UserId=?", [event.data[frndId][tm]['Msg'], frndId])
                        conneTemp.commit()
                        curTemp.execute("update Friends set Time=? where UserId=?", [event.data[frndId][tm]['Time'], frndId])
                        conneTemp.commit()
                        curTemp.execute("update Friends set Status=? where UserId=?", ["Pending", frndId])
                        conneTemp.commit()
                    try:
                        if frndId == self.friendUserid:
                            self.msguserid = frndId
                            self.msgs = event.data[frndId][tm]['Msg']
                            self.messageSignal.emit(self.msguserid, self.msgs)
                            curMsg.execute(f"UPDATE F{self.friendUserid} SET Status = ? where Status='Pending'", ["Seen"])
                            connMsg.commit()
                    except:pass
        else:
            frndId, tm = event.path[1:].split("/")
            curMsg.execute(f"select Time from F{frndId} where Time=?", [tm])
            ftTime = curMsg.fetchone()
            if ftTime == None:
                curMsg.execute(f"insert into F{frndId} values(?, ?, ?, ?)", [frndId, event.data['Msg'], event.data['Time'], event.data['Status']])
                connMsg.commit()
                curTemp.execute("update Friends set Message=? where UserId=?", [event.data['Msg'], frndId])
                conneTemp.commit()
                curTemp.execute("update Friends set Time=? where UserId=?", [event.data['Time'], frndId])
                conneTemp.commit()
                curTemp.execute("update Friends set Status=? where UserId=?", ["Pending", frndId])
                conneTemp.commit()
            try:
                if frndId == self.friendUserid:
                    self.msguserid = frndId
                    self.msgs = event.data['Msg']
                    self.messageSignal.emit(self.msguserid, self.msgs)
                    curMsg.execute(f"UPDATE F{self.friendUserid} SET Status = ? where Status='Pending'", ["Seen"])
                    connMsg.commit()
            except:print(traceback.print_exc())
        self.FriendCard()
        threading.Thread(target=self.ScrollMsg).start()

    def FriendPanel(self):
        curTemp.execute("SELECT UserId, Name, Message, Time FROM Friends ORDER BY Time COLLATE NOCASE ASC")
        frnds = curTemp.fetchall()
        if frnds != []:
            for frnd in frnds:
                frndlst = self.findChild(QtWidgets.QLabel, f"M{frnd[0]}")
                if frndlst == None:
                    curMsg.execute(f"select count(Status) from F{frnd[0]} where Status='Pending'")
                    pen = curMsg.fetchone()
                    self.Friends(frnd[0], f"Res/Images/Friends/{frnd[0]}", frnd[1], frnd[2], frnd[3], str(pen[0]))

    def Send(self):
        msg = self.ui.lineEdit_2.text()
        if msg != "":
            try:
                self.Messages(self.userid, msg)
                now = datetime.now()
                current_time = now.strftime("%Y:%m:%d:%H:%M:%S:%p").lower()
                curMsg.execute(f"INSERT INTO F{self.friendUserid} VALUES(?, ?, ?, ?)", [self.userid, msg, current_time, "Seen"])
                connMsg.commit()

                curTemp.execute(f"""UPDATE Friends SET Message = ? WHERE UserId = '{self.friendUserid}'""", [msg])
                conneTemp.commit()
                curTemp.execute(f"""UPDATE Friends SET Time = ? WHERE UserId = '{self.friendUserid}'""", [current_time])
                conneTemp.commit()
                curTemp.execute(f"""UPDATE Friends SET Status = ? WHERE UserId = '{self.friendUserid}'""", ["Seen"])
                conneTemp.commit()
                self.FriendCard()

                self.ui.lineEdit_2.setText("")
                self.th2 = MainThread(argum="SendMsg", friendUserid=self.friendUserid, userid=self.userid, msg=msg)
                if not self.th2.isRunning():
                    self.th2.start()
                else:
                    self.th2.wait()
                self.th2.signal.connect(self.RunTimeUpdates)
            except:pass
        self.ui.lineEdit_2.setFocus()

    def changeMsgWindow(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.deleteLayout(item.layout())

    def ScrollMsg(self): 
        time.sleep(0.1)
        x = self.ui.scrollArea.verticalScrollBar().maximum()
        self.ui.scrollArea.verticalScrollBar().setValue(x)

    def selectionChanged(self):
        self.loading = True
        self.ui.lineEdit_2.setFocus()
        self.ui.frame_11.setMaximumHeight(0)
        self.ui.frame_10.setMaximumHeight(16777215)
        self.item = self.ui.listWidget.currentItem()
        self.friendUserid, self.name, self.imag = self.item.statusTip().split(',')
        self.ui.label_2.setText(self.name)
        self.ui.label_5.setPixmap(QtGui.QPixmap(self.imag))

        curMsg.execute(f"SELECT UserId, Message, Time, Status FROM F{self.friendUserid} ORDER BY Time COLLATE NOCASE ASC")
        msgs = curMsg.fetchall()
        self.loading = False
        self.changeMsgWindow(self.ui.verticalLayout_16)
        for msg in msgs:
            self.Messages(msg[0], msg[1])
        curMsg.execute(f"UPDATE F{self.friendUserid} SET Status = ? where Status='Pending'", ["Seen"])
        connMsg.commit()

        self.th3 = MainThread(argum='Pending', userid=self.userid, friendUserid=self.friendUserid)
        if not self.th3.isRunning():
            self.th3.start()
        else:
            self.th3.wait()

        lbl = self.findChild(QtWidgets.QLabel, f"P{self.friendUserid}")
        lbl.setMinimumSize(QtCore.QSize(0, 0))
        lbl.setMaximumSize(QtCore.QSize(0, 0))
        threading.Thread(target=self.ScrollMsg).start()

    def restore(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def closeEvent(self, event):
        del self.listener
        del self.frndlistener

    def resizeEvent(self, event):
        QMainWindow.resizeEvent(self, event)
        rect = self.rect()
        self.grips[1].move(rect.right() - self.gripSize, 0)
        self.grips[2].move(rect.right() - self.gripSize, rect.bottom() - self.gripSize)
        self.grips[3].move(0, rect.bottom() - self.gripSize)

    def Messages(self, user, msg):
        if user == self.userid:
            self.msgSenderFont = QtGui.QFont()
            self.msgSenderFont.setFamily("Calibri")
            self.msgSenderFont.setPointSize(12)
            self.msgSenderFrame = QtWidgets.QFrame()
            self.msgSenderLabel = QtWidgets.QLabel()
            self.msgSenderLabel.setText(msg)
            self.msgSenderLabel.setStyleSheet(
                "padding: 7px 10px 10px 15px;\n"
                "background-color: rgba(35, 112, 255, 100);\n"
                "border-top-left-radius: 15px;\n"
                "border-bottom-left-radius: 15px;\n"
                "border-bottom-right-radius: 15px;\n"
            )
            self.msgSenderLabel.setFont(self.msgSenderFont)
            self.msgSenderLabel.setWordWrap(True)
            self.msgSenderLabel.setMaximumWidth(600)
            self.msgSenderLayout = QtWidgets.QHBoxLayout()
            self.msgSenderLayout.addWidget(self.msgSenderLabel)
            self.msgSenderLayout.setContentsMargins(0, 0, 0, 0)
            self.msgSenderLayout.setSpacing(0)
            self.msgSenderFrame.setLayout(self.msgSenderLayout)
            self.msgSenderFrame.setMaximumSize(self.msgSenderLabel.sizeHint())
            self.ui.verticalLayout_16.addWidget(self.msgSenderFrame, 0, QtCore.Qt.AlignRight)
        
        else:
            self.msgReceiverFont = QtGui.QFont()
            self.msgReceiverFont.setFamily("Calibri")
            self.msgReceiverFont.setPointSize(12)
            self.msgReceiverFrame = QtWidgets.QFrame()
            self.msgReceiverLabel = QtWidgets.QLabel()
            self.msgReceiverLabel.setText(msg)
            self.msgReceiverLabel.setStyleSheet(
                "padding: 7px 15px 10px 10px;\n"
                "background-color: rgba(3, 122, 158, 100);\n"
                "border-top-right-radius: 15px;\n"
                "border-bottom-left-radius: 15px;\n"
                "border-bottom-right-radius: 15px;\n"
            )
            self.msgReceiverLabel.setFont(self.msgReceiverFont)
            self.msgReceiverLabel.setWordWrap(True)
            self.msgReceiverLabel.setMaximumWidth(600)
            self.msgReceiverLayout = QtWidgets.QHBoxLayout()
            self.msgReceiverLayout.addWidget(self.msgReceiverLabel)
            self.msgReceiverLayout.setContentsMargins(0, 0, 0, 0)
            self.msgReceiverLayout.setSpacing(0)
            self.msgReceiverFrame.setLayout(self.msgReceiverLayout)
            self.msgReceiverFrame.setMaximumSize(self.msgReceiverLabel.sizeHint())
            self.ui.verticalLayout_16.addWidget(self.msgReceiverFrame, 0, QtCore.Qt.AlignLeft)

    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()

    def profileview(self):
        self.pf = Profile(self.fname, self.lname, self.userid, self.email, self.password, self.image)
        if self.pf.exec() == 1:
            self.email = self.pf.returninfo()[0]
            self.fname = self.pf.returninfo()[1]
            self.lname = self.pf.returninfo()[2]
            self.password = self.pf.returninfo()[3]

    def logout(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Are you sure ?")
        msgBox.setWindowTitle("Logout")
        msgBox.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
        msgBox.setDefaultButton(QMessageBox.No)
        returnValue = msgBox.exec()

        if returnValue == QMessageBox.Yes:
            self.lg = Login()
            self.lg.show()
            curTemp.execute(f"DELETE FROM TempUser WHERE UserID='{self.userid}'")
            conneTemp.commit()
            conneTemp.execute("DROP TABLE Friends")
            conneTemp.commit()
            curMsg.execute("SELECT name FROM sqlite_master WHERE type='table'")
            table_names = curMsg.fetchall()
            for table in table_names:
                table_name = table[0]
                curMsg.execute(f"DROP TABLE IF EXISTS {table_name}")
            connMsg.commit()
            self.close()

    def Friends(self, userid, image, name, msg, time, pend):
        self.frame = QtWidgets.QFrame()
        self.frame.setGeometry(QtCore.QRect(70, 80, 441, 81))
        self.frame.setStyleSheet("background-color:rgba(0, 0, 0, 0);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setContentsMargins(7, 7, 7, 7)
        self.horizontalLayout.setSpacing(7)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setMinimumSize(QtCore.QSize(65, 57))
        self.frame_2.setMaximumSize(QtCore.QSize(65, 57))
        self.frame_2.setStyleSheet("border:none;")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.label = QtWidgets.QLabel(self.frame_2)
        self.label.setGeometry(QtCore.QRect(0, 0, 60, 57))
        self.label.setMinimumSize(QtCore.QSize(60, 0))
        self.label.setMaximumSize(QtCore.QSize(60, 16777215))
        self.label.setStyleSheet("border: 2px solid rgba(5, 107, 202, 150);\n"
        "border-radius: 28px;")
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("../../../../Test/Res/Images/Friends/158204111134.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.frame_2)
        self.pushButton.setGeometry(QtCore.QRect(0, 0, 65, 57))
        self.pushButton.setStyleSheet("border: none;\n"
        "background: none;")
        self.pushButton.setText("")
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.frame_2)
        self.frame_3 = QtWidgets.QFrame(self.frame)
        self.frame_3.setStyleSheet("border:none;")
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame_6 = QtWidgets.QFrame(self.frame_3)
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame_6)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_3 = QtWidgets.QLabel(self.frame_6)
        self.label_3.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(13)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: rgb(205, 235, 255);\n"
        "background-color: rgba(0, 0, 0, 0);")
        self.label_3.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_4.addWidget(self.label_3)
        self.verticalLayout_2.addWidget(self.frame_6)
        self.frame_5 = QtWidgets.QFrame(self.frame_3)
        self.frame_5.setMinimumSize(QtCore.QSize(0, 20))
        self.frame_5.setMaximumSize(QtCore.QSize(16777215, 25))
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_5)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.frame_5)
        self.label_2.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgba(205, 235, 255, 170);\n"
        "background-color: rgba(0, 0, 0, 0);")
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.verticalLayout_3.addWidget(self.label_2)
        self.verticalLayout_2.addWidget(self.frame_5)
        self.horizontalLayout.addWidget(self.frame_3)
        self.frame_4 = QtWidgets.QFrame(self.frame)
        self.frame_4.setMinimumSize(QtCore.QSize(120, 0))
        self.frame_4.setMaximumSize(QtCore.QSize(120, 16777215))
        self.frame_4.setStyleSheet("border:none;")
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_7 = QtWidgets.QFrame(self.frame_4)
        self.frame_7.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_7.setObjectName("frame_7")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame_7)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_4 = QtWidgets.QLabel(self.frame_7)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color: rgb(173, 173, 173);\n"
        "padding-bottom: 2px;")
        self.label_4.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.verticalLayout_5.addWidget(self.label_4)
        self.verticalLayout.addWidget(self.frame_7)
        self.frame_8 = QtWidgets.QFrame(self.frame_4)
        self.frame_8.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_8.setObjectName("frame_8")
        self.label_5 = QtWidgets.QLabel(self.frame_8)
        self.label_5.setGeometry(QtCore.QRect(46, 0, 27, 27))
        self.label_5.setMinimumSize(QtCore.QSize(0, 0))
        self.label_5.setMaximumSize(QtCore.QSize(0, 0))
        self.label_5.setStyleSheet("background-color: rgb(105, 255, 245);\n"
        "border-radius: 12px;\n"
        "padding-bottom:2px;")
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setBold(True)
        self.label_5.setFont(font)
        self.verticalLayout.addWidget(self.frame_8)
        self.horizontalLayout.addWidget(self.frame_4)

        self.label_2.setObjectName(f"M{userid}")
        self.label_4.setObjectName(f"T{userid}")
        self.label_5.setObjectName(f"P{userid}")
        imgdata = open(image+".png", 'rb').read()
        pixmap = mask_image(imgdata)

        if pend == "0":
            self.label_4.setText(self.DateTime(time))
        else:
            self.label_5.setMinimumSize(QtCore.QSize(30, 25))
            self.label_5.setMaximumSize(QtCore.QSize(30, 25))
            self.label_4.setText(self.DateTime(time))
            self.label_5.setText(pend)

        self.frame.setObjectName(f"F{userid}")
        self.pushButton.setObjectName(f"B{userid}")
        self.label_3.setText(name)
        self.label_2.setText(msg)
        self.label.setPixmap(pixmap)

        self.profile = QtWidgets.QListWidgetItem()
        self.profile.setStatusTip(f"{userid},{name},{image}")
        self.profile.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
        self.profile.setSizeHint(QtCore.QSize(0, 75))
        self.ui.listWidget.addItem(self.profile)
        self.ui.listWidget.setItemWidget(self.profile, self.frame)

    def DateTime(self, time):
        now = datetime.now()
        current_time = now.strftime("%Y:%m:%d:%H:%M:%S:%p").lower()
        y, m, d, hr, mit, s, a = time.split(":")
        yc, mc, dc, hrc, mitc, sc, ac = current_time.split(":")
        if int(hr) > 12:
            hr = str(int(hr) - 12)
        if int(hrc) > 12:
            hrc = str(int(hrc) - 12)
            
        if y==yc and m==mc and d==dc and hr==hrc and mit==mitc and a==ac:
            return "Now"
        elif y==yc and m==mc and d==dc:
            return f"{hr}:{mit} {a}"
        elif y==yc and m==mc and int(dc)-1==int(d):
            return "yesterday"
        else:
            return f"{d}/{m}/{y[2:]}"

    def addFriend(self):
        self.adfd = AddFriends(userid=self.userid, email=self.email)
        self.adfd.exec()

class HoverIconButton(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)

        self.icon_button = QtWidgets.QPushButton()
        self.icon_button.setFixedSize(QtCore.QSize(171, 141))
        self.icon_button.setIcon(QtGui.QIcon("Res/Templates/img/edit.png"))
        self.icon_button.setIconSize(QtCore.QSize(50, 50))
        self.icon_button.setStyleSheet("QPushButton{\n"
        "    border:none;\n"
        "    border-radius: 70.4px;\n"
        "    background-color:rgba(0, 0, 0, 0);\n"
        "    color:rgba(0, 0, 0, 0);\n"
        "}\n"
        "QPushButton:hover {\n"
        "    background-color:rgba(0, 0, 0, 50);\n"
        "}")
        self.icon_button.hide()

        layout.addWidget(self.icon_button)
    
    def enterEvent(self, event):
        self.icon_button.show()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.icon_button.hide()
        super().leaveEvent(event)

class Profile(QDialog):
    
    def __init__(self, fname, lname, userid, email, password, image):
        super().__init__()
        self.ui = Ui_Profile()
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.ui.pushButton.clicked.connect(self.edit)
        self.ui.pushButton_2.clicked.connect(self.change)
        self.ui.pushButton_3.clicked.connect(self.cl)
        self.ui.pushButton_4.clicked.connect(self.updatePasswd)
        self.ui.pushButton_5.clicked.connect(self.back)
        self.ui.pushButton_6.clicked.connect(self.sendOtp)
        self.ui.pushButton_7.clicked.connect(self.saveinfo)
        self.ui.pushButton_8.clicked.connect(self.sendingOtp)
        self.ui.pushButton_9.clicked.connect(self.passwdsend)
        self.ui.pushButton_10.clicked.connect(self.sendPasswordOTP)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Res/Templates/img/close.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.pushButton_3.setIcon(icon)
        self.ui.lineEdit.setText(fname)
        self.ui.lineEdit_2.setText(lname)
        self.ui.lineEdit_3.setText(email)
        self.ui.lineEdit_4.setText(userid)
        self.ui.lineEdit_5.setText(password)
        self.ui.pushButton_4.setEnabled(False)
        self.ui.pushButton_5.setEnabled(False)
        self.ui.pushButton_6.setEnabled(False)
        self.ui.pushButton_7.setEnabled(False)
        self.ui.pushButton_8.setEnabled(False)
        self.ui.pushButton_9.setEnabled(False)
        self.ui.pushButton_10.setEnabled(False)
        self.fname = fname
        self.lname = lname
        self.email = email
        self.userid = userid
        self.password = password
        imgdata = open(image, 'rb').read()
        pixmap = mask_image(imgdata)
        self.ui.label_12.setPixmap(pixmap)

        self.pushbutton = HoverIconButton(self.ui.frame_10)
        self.pushbutton.setGeometry(QtCore.QRect(160, 30, 171, 141))

        self.gripSize = 16
        self.grips = []
        for _ in range(4):
            grip = QtWidgets.QSizeGrip(self)
            grip.resize(self.gripSize, self.gripSize)
            self.grips.append(grip)
        def moveWindow(e):
            if self.isMaximized() == False:
                if e.buttons() == Qt.LeftButton:
                    self.move(self.pos() + e.globalPos() - self.clickPosition)
                    self.clickPosition = e.globalPos()
                    e.accept()
        self.ui.frame.mouseMoveEvent = moveWindow

    def sendOtp(self):
        self.f_name = self.ui.lineEdit.text()
        self.l_name = self.ui.lineEdit_2.text()
        self.e_mail = self.ui.lineEdit_3.text()
        if self.e_mail != "" and self.f_name != "" and self.l_name != "":
            regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            if re.fullmatch(regex, self.e_mail):
                if self.email == self.e_mail:
                    self.sendingOtp()
                else:
                    collection = dbstore.collection("Users")
                    docs = collection.document(self.email)
                    if docs.get().exists:
                        self.ui.lineEdit_3.setFocus()
                        msg = QMessageBox()
                        msg.setWindowTitle("Failed")
                        msg.setText("Email address already registered")
                        msg.setIcon(QMessageBox.Critical)
                        msg.exec_()
                    else:
                        self.sendingOtp()
            else:
                self.ui.lineEdit_3.setFocus()
                msg = QMessageBox()
                msg.setWindowTitle("Failed")
                msg.setText("Invalid Email address")
                msg.setIcon(QMessageBox.Critical)
                msg.exec_()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Failed")
            msg.setText("Some info not field")
            msg.setIcon(QMessageBox.Critical)
            msg.exec_()

    def sendingOtp(self):
        self.generateOtp = generateOTP()
        print(self.generateOtp)
        self.ui.lineEdit_9.setFocus()
        self.ui.pushButton_6.setFixedHeight(0)
        self.ui.pushButton_6.setEnabled(False)
        self.ui.pushButton_7.setEnabled(True)
        self.ui.pushButton_7.setGeometry(QtCore.QRect(165, 600, 151, 41))
        self.ui.lineEdit_9.setFixedHeight(46)
        self.ui.label_8.setFixedHeight(21)
        self.ui.frame_10.setMinimumHeight(650)
        self.setMinimumSize(602, 782)
        self.resize(602, 782)
        self.sec1 = 30
        self.seconds1 = QTimer(self)
        self.seconds1.timeout.connect(self.resend1)
        self.seconds1.start(1000)

    def resend1(self):
        self.ui.label_9.setText(f"Resend {self.sec1} sec")
        if self.sec1 == 0:
            self.ui.pushButton_8.setEnabled(True)
            self.ui.pushButton_8.setFixedHeight(35)
            self.seconds1.stop()
        else:
            self.sec1 -= 1

    def passwdsend(self):
        self.current_passwd = self.ui.lineEdit_6.text()
        self.new_passwd = self.ui.lineEdit_7.text()
        re_passwd = self.ui.lineEdit_8.text()
        if self.current_passwd != "" or self.new_passwd != "" or re_passwd != "":
            if self.password == self.current_passwd:
                if self.new_passwd == re_passwd:
                    if self.new_passwd != self.current_passwd:
                        self.sendPasswordOTP()
                    else:
                        self.ui.lineEdit_7.setFocus()
                        msg = QMessageBox()
                        msg.setWindowTitle("Failed")
                        msg.setText("Current and new password don't take a same")
                        msg.setIcon(QMessageBox.Critical)
                        msg.exec_()
                else:
                    self.ui.lineEdit_8.setFocus()
                    msg = QMessageBox()
                    msg.setWindowTitle("Failed")
                    msg.setText("Both passwords does not matched!")
                    msg.setIcon(QMessageBox.Critical)
                    msg.exec_()
            else:
                self.ui.lineEdit_6.setFocus()
                msg = QMessageBox()
                msg.setWindowTitle("Failed")
                msg.setText("Current password does not matched!")
                msg.setIcon(QMessageBox.Critical)
                msg.exec_()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Failed")
            msg.setText("Some info not field")
            msg.setIcon(QMessageBox.Critical)
            msg.exec_()

    def sendPasswordOTP(self):
        self.generateOTP = generateOTP()
        print(self.generateOTP)
        self.ui.pushButton_9.setFixedHeight(0)
        self.ui.pushButton_9.setEnabled(False)
        self.ui.pushButton_4.setEnabled(True)

        self.ui.pushButton_5.setGeometry(QtCore.QRect(100, 400, 121, 41))
        self.ui.pushButton_4.setGeometry(QtCore.QRect(270, 400, 121, 41))

        self.ui.lineEdit_10.setFixedHeight(46)
        self.ui.label_10.setFixedHeight(21)

        self.ui.frame_22.setMinimumHeight(450)
        self.setMinimumSize(602, 582)
        self.resize(602, 582)
        self.sec2 = 30
        self.seconds2 = QTimer(self)
        self.seconds2.timeout.connect(self.resend2)
        self.seconds2.start(1000)

    def resend2(self):
        self.ui.label_11.setText(f"Resend {self.sec2} sec")
        if self.sec2 == 0:
            self.ui.pushButton_10.setEnabled(True)
            self.ui.pushButton_10.setFixedHeight(35)
            self.seconds2.stop()
        else:
            self.sec2 -= 1

    def returninfo(self):
        return self.email, self.fname, self.lname, self.password

    def updatePasswd(self):
        otp = self.ui.lineEdit_10.text()
        if otp == self.generateOTP:
            self.password = self.new_passwd
            database.child(self.userid).child("Info").update({"Password":self.new_passwd})
            msg = QMessageBox()
            msg.setWindowTitle("Done")
            msg.setText("Update successfully")
            msg.setIcon(QMessageBox.Information)
            msg.exec_()
            self.accept()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Failed")
            msg.setText("Wrong OTP")
            msg.setIcon(QMessageBox.Critical)
            msg.exec_()

    def edit(self):
        self.ui.lineEdit.setReadOnly(False)
        self.ui.lineEdit_2.setReadOnly(False)
        self.ui.lineEdit_3.setReadOnly(False)
        self.ui.lineEdit.setFocus()
        self.ui.pushButton.setFixedHeight(0)
        self.ui.pushButton.setEnabled(False)
        self.ui.pushButton_6.setEnabled(True)

    def change(self):
        self.ui.frame_4.setMaximumWidth(0)
        self.ui.frame_15.setMaximumWidth(16777215)
        self.ui.pushButton.setEnabled(False)
        self.ui.pushButton_2.setEnabled(False)
        self.ui.pushButton_6.setEnabled(False)
        self.ui.pushButton_7.setEnabled(False)
        self.ui.pushButton_8.setEnabled(False)
        self.ui.pushButton_11.setEnabled(False)
        self.ui.pushButton_9.setEnabled(True)
        self.ui.pushButton_5.setEnabled(True)
        self.ui.lineEdit_6.setFocus()
        self.ui.lineEdit_6.setText("")
        self.ui.lineEdit_7.setText("")
        self.ui.lineEdit_8.setText("")
        
        self.ui.frame_10.setMinimumHeight(400)
        self.setMinimumSize(602, 532)
        self.resize(602, 532)

    def back(self):
        self.ui.pushButton_5.setGeometry(QtCore.QRect(100, 320, 121, 41))
        self.ui.pushButton_4.setFixedHeight(0)
        self.ui.pushButton.setFixedHeight(41)
        self.ui.pushButton_8.setFixedHeight(0)
        self.ui.pushButton_9.setFixedHeight(41)
        self.ui.pushButton_6.setFixedHeight(41)
        self.ui.pushButton_7.setFixedHeight(41)
        self.ui.pushButton_10.setFixedHeight(0)
        self.ui.lineEdit_9.setFixedHeight(0)
        self.ui.lineEdit_10.setFixedHeight(0)
        self.ui.label_8.setFixedHeight(0)
        self.ui.label_10.setFixedHeight(0)
        self.ui.frame_10.setMinimumSize(450, 580)
        self.setMinimumSize(602, 712)
        self.resize(602, 712)
        self.ui.label_11.setText("")
        self.ui.label_9.setText("")
        try:self.seconds2.stop()
        except:pass
        try:self.seconds1.stop()
        except:pass
        self.ui.frame_4.setMaximumWidth(16777215)
        self.ui.frame_15.setMaximumWidth(0)
        self.ui.pushButton.setEnabled(True)
        self.ui.pushButton_2.setEnabled(True)
        self.ui.pushButton_11.setEnabled(True)
        self.ui.pushButton_4.setEnabled(False)
        self.ui.pushButton_5.setEnabled(False)
        self.ui.pushButton_6.setEnabled(False)
        self.ui.pushButton_7.setEnabled(False)
        self.ui.pushButton_8.setEnabled(False)
        self.ui.pushButton_9.setEnabled(False)
        self.ui.pushButton_10.setEnabled(False)
        self.ui.lineEdit.setText(self.fname)
        self.ui.lineEdit.setReadOnly(True)
        self.ui.lineEdit_2.setText(self.lname)
        self.ui.lineEdit_2.setReadOnly(True)
        self.ui.lineEdit_3.setText(self.email)
        self.ui.lineEdit_3.setReadOnly(True)
        self.ui.lineEdit_6.setText("")
        self.ui.lineEdit_7.setText("")
        self.ui.lineEdit_8.setText("")

    def saveinfo(self):
        otp = self.ui.lineEdit_9.text()
        if otp == self.generateOtp:
            database.child(self.userid).child("Info").update({"Email":self.e_mail, 'First Name':self.f_name, 'Last Name':self.l_name})
            self.fname = self.f_name
            self.lname = self.l_name
            self.email = self.e_mail
            msg = QMessageBox()
            msg.setWindowTitle("Done")
            msg.setText("Update successfully")
            msg.setIcon(QMessageBox.Information)
            msg.exec_()
            self.accept()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Failed")
            msg.setText("Wrong OTP")
            msg.setIcon(QMessageBox.Critical)
            msg.exec_()

    def resizeEvent(self, event):
        QDialog.resizeEvent(self, event)
        rect = self.rect()
        self.grips[1].move(rect.right() - self.gripSize, 0)
        self.grips[2].move(rect.right() - self.gripSize, rect.bottom() - self.gripSize)
        self.grips[3].move(0, rect.bottom() - self.gripSize)

    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()

    def cl(self):
        self.close()

class Loading(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Loading()
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

class AddFriends(QDialog):
    def __init__(self, parent=None, userid=None, email=None):
        super(AddFriends, self).__init__(parent)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.ui = Ui_addFriends()
        self.ui.setupUi(self)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Res/Templates/img/close.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.pushButton_3.setIcon(icon)
        self.ui.pushButton_3.clicked.connect(self.close)
        
        self.timer1 = QTimer()
        self.timer1.setSingleShot(True)
        self.timer1.setInterval(1000)  # Set the pause duration in milliseconds
        self.timer1.timeout.connect(self.AddLineEdit)
        self.ui.lineEdit.textChanged.connect(self.start_timer1)

        self.timer2 = QTimer()
        self.timer2.setSingleShot(True)
        self.timer2.setInterval(1000)  # Set the pause duration in milliseconds
        self.timer2.timeout.connect(self.PendLineEdit)
        self.ui.lineEdit_2.textChanged.connect(self.start_timer2)

        self.timer3 = QTimer()
        self.timer3.setSingleShot(True)
        self.timer3.setInterval(1000)  # Set the pause duration in milliseconds
        self.timer3.timeout.connect(self.FriendLineEdit)
        self.ui.lineEdit_3.textChanged.connect(self.start_timer3)

        self.ui.tabWidget.tabBarClicked.connect(self.tabs)
        self.userid = userid
        self.email = email
        self.loading()

        self.gripSize = 16
        self.grips = []
        for _ in range(4):
            grip = QtWidgets.QSizeGrip(self)
            grip.resize(self.gripSize, self.gripSize)
            self.grips.append(grip)
        
        def moveWindow(e):
            if self.isMaximized() == False:
                if e.buttons() == Qt.LeftButton:
                    self.move(self.pos() + e.globalPos() - self.clickPosition)
                    self.clickPosition = e.globalPos()
                    e.accept()
        self.ui.frame.mouseMoveEvent = moveWindow
        self.FriendLineEdit()

    def start_timer1(self):
        if not self.timer1.isActive():
            self.timer1.start()

    def start_timer2(self):
        if not self.timer2.isActive():
            self.timer2.start()

    def start_timer3(self):
        if not self.timer3.isActive():
            self.timer3.start()

    def tabs(self, index):
        if self.ui.tabWidget.tabText(index) == "Pending":
            self.PendLineEdit()

    def resizeEvent(self, event):
        QDialog.resizeEvent(self, event)
        rect = self.rect()
        self.grips[1].move(rect.right() - self.gripSize, 0)
        self.grips[2].move(rect.right() - self.gripSize, rect.bottom() - self.gripSize)
        self.grips[3].move(0, rect.bottom() - self.gripSize)

    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()

    def loading(self):
        self.movie1 = QMovie("Res/Images/loading.gif")
        self.ui.label_2.setMovie(self.movie1)
        self.movie1.start()
        self.movie2 = QMovie("Res/Images/loading.gif")
        self.ui.label_4.setMovie(self.movie2)
        self.movie2.start()
        self.movie3 = QMovie("Res/Images/loading.gif")
        self.ui.label_6.setMovie(self.movie3)
        self.movie3.start()

    def AddLineEdit(self):
        self.ui.listWidget.setMaximumHeight(0)
        self.ui.frame_13.setMaximumHeight(16777215)
        self.ui.frame_12.setMaximumHeight(0)
        self.search1 = self.ui.lineEdit.text()
        if self.search1 == "":
            self.ui.listWidget.clear()
            self.ui.listWidget.setMaximumHeight(16777215)
            self.ui.frame_13.setMaximumHeight(0)
            self.ui.frame_12.setMaximumHeight(0)
        else:
            self.Check1()

    def PendLineEdit(self):
        self.ui.listWidget_2.setMaximumHeight(0)
        self.ui.frame_16.setMaximumHeight(16777215)
        self.ui.frame_15.setMaximumHeight(0)
        self.search2 = self.ui.lineEdit_2.text()
        self.Check2()

    def FriendLineEdit(self):
        self.ui.listWidget_3.setMaximumHeight(0)
        self.ui.frame_19.setMaximumHeight(16777215)
        self.ui.frame_18.setMaximumHeight(0)
        self.search3 = self.ui.lineEdit_3.text()
        self.Check3()

    def Check1(self):
        self.ui.listWidget.clear()
        self.AddFriendThread1 = ManageFriend(argum="Request", userid=self.userid, search=self.search1)
        if not self.AddFriendThread1.isRunning():
            self.AddFriendThread1.start()
        else:
            self.AddFriendThread1.wait()
        self.AddFriendThread1.signalRequest.connect(self.AddlineEditChange)
        self.AddFriendThread1.signalPending.connect(self.PendlineEditChange)
        self.AddFriendThread1.signalFriend.connect(self.FriendlineEditChange)
        self.AddFriendThread1.signalWindowStatus.connect(self.Status)

    def Check2(self):
        self.ui.listWidget_2.clear()
        self.AddFriendThread2 = (ManageFriend(argum="Pending", userid=self.userid, search=self.search2))
        if not self.AddFriendThread2.isRunning():
            self.AddFriendThread2.start()
        else:
            self.AddFriendThread2.wait()
        self.AddFriendThread2.signalPending.connect(self.PendlineEditChange)
        self.AddFriendThread2.signalWindowStatus.connect(self.Status)

    def Check3(self):
        self.ui.listWidget_3.clear()
        self.AddFriendThread3 = (ManageFriend(argum="Added", userid=self.userid, search=self.search3))
        if not self.AddFriendThread3.isRunning():
            self.AddFriendThread3.start()
        else:
            self.AddFriendThread3.wait()
        self.AddFriendThread3.signalFriend.connect(self.FriendlineEditChange)
        self.AddFriendThread3.signalWindowStatus.connect(self.Status)

    def Status(self, win, change):
        if change == "Req":
            if win == "all":
                self.ui.listWidget.setMaximumHeight(16777215)
                self.ui.frame_13.setMaximumHeight(0)
                self.ui.frame_12.setMaximumHeight(0)
            elif win == "not":
                self.ui.frame_12.setMaximumHeight(16777215)
                self.ui.frame_13.setMaximumHeight(0)
                self.ui.listWidget.setMaximumHeight(0)
        elif change == "Pen":
            if win == "all":
                self.ui.listWidget_2.setMaximumHeight(16777215)
                self.ui.frame_15.setMaximumHeight(0)
                self.ui.frame_16.setMaximumHeight(0)
            elif win == "not":
                self.ui.listWidget_2.setMaximumHeight(0)
                self.ui.frame_16.setMaximumHeight(0)
                self.ui.frame_15.setMaximumHeight(16777215)
        elif change == "Added":
            if win == "all":
                self.ui.listWidget_3.setMaximumHeight(16777215)
                self.ui.frame_19.setMaximumHeight(0)
                self.ui.frame_18.setMaximumHeight(0)
            elif win == "not":
                self.ui.listWidget_3.setMaximumHeight(0)
                self.ui.frame_19.setMaximumHeight(0)
                self.ui.frame_18.setMaximumHeight(16777215)

    def AddlineEditChange(self, win, name, email, userid, status):
        if win == "Req":
            self.AddFriends(name, email, userid, self.ui.listWidget, status)

    def PendlineEditChange(self, win, name, userid, email, time):
        if win == "Req":
            self.PendFriends(name, userid, email, time, self.ui.listWidget)
        elif win == "Pen":
            self.PendFriends(name, userid, email, time, self.ui.listWidget_2)
        elif win == "Added":
            self.PendFriends(name, userid, email, time, self.ui.listWidget_3)

    def DateTime(self, time):
        now = datetime.now()
        current_time = now.strftime("%Y:%m:%d:%H:%M:%p").lower()
        y, m, d, hr, mit, a = time.split(":")
        yc, mc, dc, hrc, mitc, ac = current_time.split(":")
        if int(hr) > 12:
            hr = str(int(hr) - 12)
        if int(hrc) > 12:
            hrc = str(int(hrc) - 12)
            
        if y==yc and m==mc and d==dc and hr==hrc and mit==mitc and a==ac:
            return "Now"
        elif y==yc and m==mc and d==dc:
            return f"{hr}:{mit} {a}"
        elif y==yc and m==mc and int(dc)-1==int(d):
            return "yesterday"
        else:
            return f"{d}/{m}/{y[2:]}"

    def FriendlineEditChange(self, win, name, userid):
        if win == "Req":
            self.Friends(name, userid, self.ui.listWidget)
        elif win == "Added":
            self.Friends(name, userid, self.ui.listWidget_3)

    def AddFriends(self, name, email, userid, win, status):
        self.frame = QtWidgets.QFrame()
        self.frame.setGeometry(QtCore.QRect(10, 70, 481, 61))
        self.frame.setStyleSheet("background-color: rgb(8, 64, 98);\n"
        "border:none;")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setMinimumSize(QtCore.QSize(70, 60))
        self.frame_2.setMaximumSize(QtCore.QSize(70, 60))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.frame_2)
        self.label.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.label.setText("")
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout.addWidget(self.frame_2)
        self.frame_3 = QtWidgets.QFrame(self.frame)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame_6 = QtWidgets.QFrame(self.frame_3)
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame_6)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_3 = QtWidgets.QLabel(self.frame_6)
        self.label_3.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(13)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: rgb(205, 235, 255);\n"
        "background-color: rgba(0, 0, 0, 0);")
        self.label_3.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_4.addWidget(self.label_3)
        self.verticalLayout_2.addWidget(self.frame_6)
        self.frame_5 = QtWidgets.QFrame(self.frame_3)
        self.frame_5.setMinimumSize(QtCore.QSize(0, 20))
        self.frame_5.setMaximumSize(QtCore.QSize(16777215, 25))
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_5)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.frame_5)
        self.label_2.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgba(205, 235, 255, 170);\n"
        "background-color: rgba(0, 0, 0, 0);")
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_3.addWidget(self.label_2)
        self.verticalLayout_2.addWidget(self.frame_5)
        self.horizontalLayout.addWidget(self.frame_3)
        self.frame_4 = QtWidgets.QFrame(self.frame)
        self.frame_4.setMinimumSize(QtCore.QSize(140, 60))
        self.frame_4.setMaximumSize(QtCore.QSize(140, 60))
        self.frame_4.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.pushButton = QtWidgets.QPushButton(self.frame_4)
        self.pushButton.setGeometry(QtCore.QRect(10, 12, 120, 35))
        self.pushButton.setMinimumSize(QtCore.QSize(120, 35))
        self.pushButton.setMaximumSize(QtCore.QSize(120, 35))
        font = QtGui.QFont()
        font.setFamily("Cambria Math")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("background-color: rgb(15, 255, 111);\n"
        "border: none;\n"
        "border-radius: 10px;")
        self.pushButton.setObjectName(f"R{userid},{email}")
        self.pushButton_2 = QtWidgets.QPushButton(self.frame_4)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 12, 120, 35))
        self.pushButton_2.setMinimumSize(QtCore.QSize(120, 35))
        self.pushButton_2.setMaximumSize(QtCore.QSize(120, 35))
        font = QtGui.QFont()
        font.setFamily("Cambria Math")
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("background-color: rgb(255, 84, 87);\n"
        "border: none;\n"
        "border-radius: 10px;")
        self.pushButton_2.setObjectName(f"C{userid},{email}")
        font = QtGui.QFont()
        font.setFamily("Cambria Math")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.pushButton_2.raise_()
        self.pushButton.raise_()
        self.horizontalLayout.addWidget(self.frame_4)

        if status == "Request":
            self.pushButton.setMinimumSize(QtCore.QSize(120, 35))
            self.pushButton.setMaximumSize(QtCore.QSize(120, 35))
        elif status == "Cancel":
            self.pushButton.setMinimumSize(QtCore.QSize(0, 35))
            self.pushButton.setMaximumSize(QtCore.QSize(0, 35))
        else:
            self.pushButton.setMinimumSize(QtCore.QSize(0, 35))
            self.pushButton.setMaximumSize(QtCore.QSize(0, 35))
            self.pushButton_2.setMinimumSize(QtCore.QSize(0, 35))
            self.pushButton_2.setMaximumSize(QtCore.QSize(0, 35))
        self.label.setPixmap(QtGui.QPixmap("Res/Images/person.png"))
        self.label_3.setText(name)
        self.label_2.setText(userid)
        self.pushButton.setText("Request")
        self.pushButton_2.setText("Cancel Request")
        self.pushButton.clicked.connect(self.RequestFriend)
        self.pushButton_2.clicked.connect(self.canRequestFriend)

        self.profile = QtWidgets.QListWidgetItem()
        self.profile.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
        self.profile.setSizeHint(QtCore.QSize(100, 60))
        win.addItem(self.profile)
        win.setItemWidget(self.profile, self.frame)

    def canRequestFriend(self):
        sender = self.sender()
        push_button = self.findChild(QtWidgets.QPushButton, sender.objectName())
        id, em = push_button.objectName().split(",")
        ch = self.findChild(QtWidgets.QPushButton, f"R{id[1:]},{em}")
        self.AddFriendThread5 = ManageFriend(argum="CancelRequest", userid=self.userid, email=self.email, id=id, em=em)
        if not self.AddFriendThread5.isRunning():
            self.AddFriendThread5.start()
        else:
            self.AddFriendThread5.wait()
        ch.setMinimumSize(QtCore.QSize(120, 35))
        ch.setMaximumSize(QtCore.QSize(120, 35))

    def RequestFriend(self):
        sender = self.sender()
        push_button = self.findChild(QtWidgets.QPushButton, sender.objectName())
        id, em = push_button.objectName().split(",")
        self.AddFriendThread4 = ManageFriend(argum="UsertoRequest", userid=self.userid, email=self.email, id=id, em=em)
        if not self.AddFriendThread4.isRunning():
            self.AddFriendThread4.start()
        else:
            self.AddFriendThread4.wait()
        sender.setMinimumSize(QtCore.QSize(0, 35))
        sender.setMaximumSize(QtCore.QSize(0, 35))

    def PendFriends(self, name, userid, email, time, win):
        self.frame = QtWidgets.QFrame()
        self.frame.setGeometry(QtCore.QRect(10, 70, 549, 60))
        self.frame.setStyleSheet("background-color: rgb(8, 64, 98);\n"
        "border:none;")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setMinimumSize(QtCore.QSize(70, 60))
        self.frame_2.setMaximumSize(QtCore.QSize(70, 60))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.frame_2)
        self.label.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.label.setText("")
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout.addWidget(self.frame_2)
        self.frame_3 = QtWidgets.QFrame(self.frame)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame_6 = QtWidgets.QFrame(self.frame_3)
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame_6)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_3 = QtWidgets.QLabel(self.frame_6)
        self.label_3.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(13)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: rgb(205, 235, 255);\n"
        "background-color: rgba(0, 0, 0, 0);")
        self.label_3.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_4.addWidget(self.label_3)
        self.verticalLayout_2.addWidget(self.frame_6)
        self.frame_5 = QtWidgets.QFrame(self.frame_3)
        self.frame_5.setMinimumSize(QtCore.QSize(0, 20))
        self.frame_5.setMaximumSize(QtCore.QSize(16777215, 25))
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_5)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.frame_5)
        self.label_2.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgba(205, 235, 255, 170);\n"
        "background-color: rgba(0, 0, 0, 0);")
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_3.addWidget(self.label_2)
        self.verticalLayout_2.addWidget(self.frame_5)
        self.horizontalLayout.addWidget(self.frame_3)
        self.frame_7 = QtWidgets.QFrame(self.frame)
        self.frame_7.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_7.setObjectName("frame_7")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_7)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_5 = QtWidgets.QLabel(self.frame_7)
        font = QtGui.QFont()
        font.setFamily("Cambria Math")
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("color: rgb(6, 255, 14);")
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_2.addWidget(self.label_5)
        self.horizontalLayout.addWidget(self.frame_7)
        self.frame_4 = QtWidgets.QFrame(self.frame)
        self.frame_4.setMinimumSize(QtCore.QSize(150, 60))
        self.frame_4.setMaximumSize(QtCore.QSize(150, 60))
        self.frame_4.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.pushButton = QtWidgets.QPushButton(self.frame_4)
        self.pushButton.setGeometry(QtCore.QRect(40, 15, 90, 30))
        self.pushButton.setMinimumSize(QtCore.QSize(90, 30))
        self.pushButton.setMaximumSize(QtCore.QSize(90, 30))
        font = QtGui.QFont()
        font.setFamily("Cambria Math")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("background-color: rgb(15, 255, 111);\n"
        "border: none;\n"
        "border-radius: 10px;")
        self.pushButton.setObjectName(f"{userid},{email}")
        self.label_4 = QtWidgets.QLabel(self.frame_4)
        self.label_4.setGeometry(QtCore.QRect(40, 15, 90, 30))
        font = QtGui.QFont()
        font.setFamily("Cambria Math")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color: rgb(60, 255, 138);")
        self.label_4.setScaledContents(True)
        self.label_4.setObjectName("label_4")
        self.label_4.raise_()
        self.pushButton.raise_()
        self.horizontalLayout.addWidget(self.frame_4)

        self.label.setPixmap(QtGui.QPixmap("Res/Images/person.png"))
        self.label_4.setText("Accepted")
        self.pushButton.setText("Accept")
        self.pushButton.clicked.connect(self.Accept)
        self.label_2.setText(userid[1:])
        self.label_3.setText(name)
        self.label_5.setText(self.DateTime(time))

        self.profile = QtWidgets.QListWidgetItem()
        self.profile.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
        self.profile.setSizeHint(QtCore.QSize(100, 60))
        win.addItem(self.profile)
        win.setItemWidget(self.profile, self.frame)

    def Accept(self):
        sender = self.sender()
        push_button = self.findChild(QtWidgets.QPushButton, sender.objectName())
        accbtn = self.findChild(QtWidgets.QPushButton, push_button.objectName())
        accbtn.setMinimumSize(QtCore.QSize(0, 35))
        accbtn.setMaximumSize(QtCore.QSize(0, 35))
        id, em = push_button.objectName().split(",")
        self.FriendLineEdit()
        self.AddFriendThread6 = ManageFriend(argum="Accept", userid=self.userid, email=self.email, id=id, em=em)
        if not self.AddFriendThread6.isRunning():
            self.AddFriendThread6.start()
        else:
            self.AddFriendThread6.wait()

    def Friends(self, name, userid, win):
        self.frame = QtWidgets.QFrame()
        self.frame.setGeometry(QtCore.QRect(10, 70, 461, 60))
        self.frame.setStyleSheet("background-color: rgb(8, 64, 98);\n"
        "border:none;")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setMinimumSize(QtCore.QSize(70, 60))
        self.frame_2.setMaximumSize(QtCore.QSize(70, 60))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.frame_2)
        self.label.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.label.setText("")
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout.addWidget(self.frame_2)
        self.frame_3 = QtWidgets.QFrame(self.frame)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame_6 = QtWidgets.QFrame(self.frame_3)
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame_6)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_3 = QtWidgets.QLabel(self.frame_6)
        self.label_3.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(13)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: rgb(205, 235, 255);\n"
        "background-color: rgba(0, 0, 0, 0);")
        self.label_3.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_4.addWidget(self.label_3)
        self.verticalLayout_2.addWidget(self.frame_6)
        self.frame_5 = QtWidgets.QFrame(self.frame_3)
        self.frame_5.setMinimumSize(QtCore.QSize(0, 20))
        self.frame_5.setMaximumSize(QtCore.QSize(16777215, 25))
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_5)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.frame_5)
        self.label_2.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgba(205, 235, 255, 170);\n"
        "background-color: rgba(0, 0, 0, 0);")
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_3.addWidget(self.label_2)
        self.verticalLayout_2.addWidget(self.frame_5)
        self.horizontalLayout.addWidget(self.frame_3)
        self.frame_4 = QtWidgets.QFrame(self.frame)
        self.frame_4.setMinimumSize(QtCore.QSize(150, 60))
        self.frame_4.setMaximumSize(QtCore.QSize(150, 60))
        self.frame_4.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.label_4 = QtWidgets.QLabel(self.frame_4)
        self.label_4.setGeometry(QtCore.QRect(40, 15, 90, 30))
        font = QtGui.QFont()
        font.setFamily("Cambria Math")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color: rgb(60, 255, 138);")
        self.label_4.setScaledContents(True)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.frame_4)

        self.label_3.setText(name)
        self.label_2.setText(userid)
        self.label_4.setText("Friend")
        self.label.setPixmap(QtGui.QPixmap("Res/Images/person.png"))

        self.profile = QtWidgets.QListWidgetItem()
        self.profile.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
        self.profile.setSizeHint(QtCore.QSize(100, 60))
        win.addItem(self.profile)
        win.setItemWidget(self.profile, self.frame)

ex = None
try:
    firebaseConfigure = {
        "type": "service_account",
        "project_id": "massenger-ab6d0",
        "private_key_id": "88d29705e5d0ac8c507d2fd012f3ba05c288d526",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC/ODiv60BCB8j/\nDUcjo9akWASW5FaVRrEbG44SAvXJpxwr04bvMj2Cye12H2Bcukn4OuB9U6bbUO3U\ni6Dd6z53RNv2vCWX37kP2qP4KNmwB4tuOHySeVknOM4Se1DavdldzbviBFeVynv0\nRCKIYMAh4rNTKE2oIaeIvcxMzYSeDrGH1oztXwQWDCjcdMK3t4Ip66WhieTZtxqn\niz2LJJfa0jl24hfWSzBMrRMl3FdFL+3Xzj0oVV7IlZXT6GhxJBRTfROxG6pEcOaA\nXWK9PwSodVMhEyML10lSvKFjhDPvyLg/TcQWGBcYQ7sSXUYsRL16npFpiZxi1cVt\nYS8Ll0oHAgMBAAECggEATRyCe6q+SIJ0MyprGDu/WJnoC+N76QnPbPOROME51f6O\nVTwhi38yn/YHTR29EdfL8Y7orZGY1ZOOvSorjqKJl7ZMj/TyogrFyddtTStIEf0Q\n5LthvP2zjqYRMBHLmtJ5gCLxk+UVXuH/V5NMa7u8b03I7A1yN42Ozo1fgE9Wnhfx\nwljRAj1Rlc5BGfcJqEpk84w717JczN/WbdiW5WqMWH1PIlXXOLur+V5YU5aj396w\nPlOM5P9WyQMLD8gzMom2IH7EdQMCHUM6QWLa1zWxnHc3SQuLhu5Mdzaai7B5eWm5\nHmOqxAXGd0io6dGbeVl8PM6BURAmMIJQBu67usQnGQKBgQD88ZnPGt5/0BNtXhrl\n94HOGHg7Ml0gNaTJpfucdEhXJHb7pgARmUBHjb17QpldrtSH1ePuHn5TesB5RGMT\nUUQ063+xED2qs7CR3SWJA1Whu0PJjr2NLZtsYYuSODIbGaqsZTCjU5wxt7rXfTIi\n2XibA6tY2iqUL3MvrexLd9Ys6QKBgQDBh7J0EZFWygKQqtg8eEIDOha8fAvX/Md/\n7QBR3jvJz12QphVS1rNnb3M8aLGTburzlJ/U9DomIxoh0TeRw737mgWKsaY/EU1y\nymOsx7lrqYexD53RKhD/E8qLXKxb9JCkbFVxoC8CaW45luW4uoab3OX1evPPQI8J\nN+phRPSpbwKBgFW1jDfIVAKdQCf8DkNEdgCe/AabD0E9zCPkEXk3UdftbD/jRPyx\noD1ewwkETTGYbz3D9WMXhBjHbHbq/GNsUx9XeUJHTY4NK1SRygk+TwLpkJO4wXQY\nMyUrfH7Eef4C2XlnJG8Dgta5+h7Qtm9mn15vhN0rt+fUmERcu8fqyHEZAoGBAIwF\nmycBYu+xXyO+iI9Pzys4hyS+d29BVDKJjnatXQLJxv+WOs1hzBHlgDHP6dMrKFEu\nUmoofj4Dna+kCRmszzNQH/xWRltRMIECUBW9t7lewm9oRh4E2qFDd4NXfNlXXKOq\nQjPg2sJa98YxGGqMgkIZFESFPgvQwOzBiRHxazd/AoGAXNhDYZlPmdS7gc++1GQT\nxRW5Q6eJnLTuGOgqMsWKP8aMZmqdjypNKGIxBbzVCyVI03GxQb7VWDkCuwBgzxY+\n8l5LGcfFawj/FQEh0RSUBIB4E09cvqKZdk+D04JrFyciv4DNuUglqD+zIL2KhLNo\n/fSlWDZKRzEIfapfvwU3ta0=\n-----END PRIVATE KEY-----\n",
        "client_email": "firebase-adminsdk-h0w9q@massenger-ab6d0.iam.gserviceaccount.com",
        "client_id": "112672501429493702580",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-h0w9q%40massenger-ab6d0.iam.gserviceaccount.com"
    }

    cred = credentials.Certificate(firebaseConfigure)
    initialize_app(cred, {
        'databaseURL': 'https://massenger-ab6d0-default-rtdb.firebaseio.com/',
        'storageBucket': "massenger-ab6d0.appspot.com"
    })

    database = db.reference('AllUsers')
    bucket = storage.bucket()
    dbstore = firestore.client()
    lock = QMutex()

    if not os.path.exists("Res"):
        os.makedirs("Res")
    if not os.path.exists("Res/Database"):
        os.makedirs("Res/Database")
    conneTemp = sqlite3.connect('Res/Database/temp.db', check_same_thread=False)
    curTemp = conneTemp.cursor()
    curTemp.execute("PRAGMA recursive_triggers = ON;")
    connMsg = sqlite3.connect('Res/Database/msg.db', check_same_thread=False)
    curMsg = connMsg.cursor()
    curMsg.execute("PRAGMA recursive_triggers = ON;")
    curTemp.execute("CREATE TABLE IF NOT EXISTS TempUser(UserId TEXT, Email TEXT)")
    conneTemp.commit()
    curTemp.execute("CREATE TABLE IF NOT EXISTS Friends(UserId TEXT, Name TEXT, Message TEXT, Time TEXT, Status TEXT)")
    conneTemp.commit()

    app = QApplication(sys.argv)
    app.setApplicationName("Fly Messener")
    curTemp.execute("SELECT UserId FROM TempUser")
    checked = curTemp.fetchall()
    if checked == []:
        wc = Login()
    else:
        wc = Main()
    wc.show()
    ex = 0

except:
    print(traceback.print_exc())
    msg = QMessageBox()
    msg.setWindowTitle("Failed")
    msg.setText("Internet not connected")
    msg.setIcon(QMessageBox.Critical)
    msg.exec_()

if ex != None:
    sys.exit(app.exec_())

QApplication.quit()

