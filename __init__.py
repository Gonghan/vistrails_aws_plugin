from core.modules.vistrails_module import Module, ModuleError
import core.modules
import core.modules.basic_modules
import core.modules.module_registry
import core.system
import gui.application

from PyQt4 import QtCore, QtGui, QtWebKit
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

import api
import sys
import pexpect
import re
import uuid
import time
import os
import webbrowser

version = "0.0.5"
name = "AmazonPlugin"
identifier = "edu.cmu.nasaproject.vistrails.amazonplugin"
#this is my private key, username and public dns, change it into yours
private_key="~/Desktop/credential/free_instance.pem"
username="ubuntu"
public_dns="ec2-54-193-41-130.us-west-1.compute.amazonaws.com"
ssh_command_pre="ssh -i "+private_key+" "+username+"@"+public_dns
scp_command_pre="scp -i "+private_key

class JobStatusViewer(QtGui.QWidget):

    def __init__(self, parent=None):

        QtGui.QWidget.__init__(self, parent)
        self.setWindowTitle('Job Status')
        gridLayout = QtGui.QGridLayout()
        self.setLayout(gridLayout)

        self.usage_label = QtGui.QLabel()
        self.usage_label.setTextFormat(QtCore.Qt.RichText)
        self.usage_label.setOpenExternalLinks(True)
        gridLayout.addWidget(self.usage_label, 1, 0)

    def updateStatus(self):
#ssh -i ~/Downloads/gonghankey.pem ubuntu@ec2-54-200-158-71.us-west-2.compute.amazonaws.com "find /home/ubuntu/hecc/config -type f | grep #'.txt'"

        self.usage_label.setText("Loading...")

        # login info
        username = loginWindow.username
        password = loginWindow.password
	displayText=""
	queue_command=ssh_command_pre+" \"find ~/hecc/Server/job_queue -type f| grep '/"+username+"_'"+"\""
	print >> sys.stderr, queue_command
	running_command=ssh_command_pre+" \"find ~/hecc/Server/running -type f| grep '/"+username+"_'"+"\""
	print >> sys.stderr, running_command
	done_command=ssh_command_pre+" \"find ~/hecc/Server/done -type f| grep '/"+username+"_'"+"\""
	print >> sys.stderr, done_command

	queue_results=os.popen(queue_command,"r")
	running_results=os.popen(running_command,"r")
	done_results=os.popen(done_command,"r")

	displayText+="In Queue"
	while 1:
	    displayText+="<br>"
	    try:
      		line=queue_results.readline()
	    except:
		break
	    if not line: break
	    displayText+=line.replace("/home/ubuntu/hecc/Server/job_queue","")
	    sys.stdout.flush() 
	queue_results.close()
	displayText+="<br>Running"
	while 1:
   	    displayText+="<br>"
	    try:
      		line=running_results.readline()
	    except:
		break
	    if not line: break
	    displayText+=line.replace("/home/ubuntu/hecc/Server/running","")
	    sys.stdout.flush() 
	running_results.close()
	displayText+="<br>Done"
	while 1:
            displayText+="<br>"
	    try:
      		line=done_results.readline()
	    except:
		break
	    if not line: break
	    displayText+=line.replace("/home/ubuntu/hecc/Server/done","")
	    sys.stdout.flush() 
	done_results.close()

        
        self.usage_label.setText(displayText)


class LoginViewer(QtGui.QWidget):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setWindowTitle('Login Viewer')
        gridLayout = QtGui.QGridLayout()
        self.setLayout(gridLayout)

        self.usernameLabel = QtGui.QLabel('User Name')
        gridLayout.addWidget(self.usernameLabel, 0, 0)
        self.usernameEdit = QtGui.QLineEdit()
        gridLayout.addWidget(self.usernameEdit, 0, 1)

        self.passwordLabel = QtGui.QLabel('Password')
        gridLayout.addWidget(self.passwordLabel, 1, 0)
        self.passwordEdit = QtGui.QLineEdit()
        self.passwordEdit.setEchoMode(QtGui.QLineEdit.Password)
        gridLayout.addWidget(self.passwordEdit, 1, 1)

        self.loginButton = QtGui.QPushButton('Login')
        gridLayout.addWidget(self.loginButton, 2, 1)
        self.connect(self.loginButton, QtCore.SIGNAL('clicked()'), self.save)

    def save(self):
        self.username = str(self.usernameEdit.text())
        self.password = str(self.passwordEdit.text())
        self.hide()

class EstimatorViewer(QtGui.QWidget):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setWindowTitle('Estimator Viewer')
        gridLayout = QtGui.QGridLayout()
        self.setLayout(gridLayout)

        self.usernameLabel = QtGui.QLabel('Notify Email')
        gridLayout.addWidget(self.usernameLabel, 0, 0)
        self.usernameEdit = QtGui.QLineEdit()
        gridLayout.addWidget(self.usernameEdit, 0, 1)

        self.loginButton = QtGui.QPushButton('Estimate')
        gridLayout.addWidget(self.loginButton, 2, 1)
        self.connect(self.loginButton, QtCore.SIGNAL('clicked()'), self.save)

    def save(self):
        self.email = str(self.usernameEdit.text())
	vt_filepath = api.get_current_controller().get_locator().name

	url="http://einstein.sv.cmu.edu/estimator?email='"+self.email+"'&vfile='"+vt_filepath+"'"
	print >> sys.stderr, url
	webbrowser.open_new(url)
        self.hide()

class SendViewer(QtGui.QWidget):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setWindowTitle('Send to Amazon Settings')
        gridLayout = QtGui.QGridLayout()
        self.setLayout(gridLayout)

        self.emailLabel = QtGui.QLabel('Notification Email')
        gridLayout.addWidget(self.emailLabel, 0, 0)
        self.emailEdit = QtGui.QLineEdit()
        gridLayout.addWidget(self.emailEdit, 0, 1)

        """
        self.ncpusLabel = QtGui.QLabel('Number of CPUs')
        gridLayout.addWidget(self.ncpusLabel, 1, 0)
        self.ncpusEdit = QtGui.QLineEdit()
        self.ncpusEdit.setText("32")
        gridLayout.addWidget(self.ncpusEdit, 1, 1)
        """

        self.prefLabel = QtGui.QLabel('Preference')
        gridLayout.addWidget(self.prefLabel, 2, 0)
        self.prefCombo = QtGui.QComboBox()
        self.prefCombo.addItem("Performance", "performance")
        self.prefCombo.addItem("Cost", "cost")
        self.prefCombo.addItem("Manual", "manual")
        gridLayout.addWidget(self.prefCombo, 2, 1)
        self.connect(self.prefCombo, QtCore.SIGNAL('currentIndexChanged(QString)'), self.changeNodeInputs)

        """
        self.nodeLabel = QtGui.QLabel('Node Type')
        gridLayout.addWidget(self.nodeLabel, 3, 0)
        self.nodeCombo = QtGui.QComboBox()
        self.nodeCombo.addItem("Sandy Bridge", "san")
        self.nodeCombo.addItem("Westmere", "wes")
        self.nodeCombo.addItem("Nehalem", "neh")
        self.nodeCombo.addItem("Harpertown", "har")
        gridLayout.addWidget(self.nodeCombo, 3, 1)

        self.selectLabel = QtGui.QLabel('Number of Nodes')
        gridLayout.addWidget(self.selectLabel, 4, 0)
        self.selectEdit = QtGui.QLineEdit()
        self.selectEdit.setText("2")
        gridLayout.addWidget(self.selectEdit, 4, 1)
        """

        # Sandy bridge input
        self.sanLabel = QtGui.QLabel('Sandy Bridge')
        gridLayout.addWidget(self.sanLabel, 3, 0)
        self.sanEdit = QtGui.QLineEdit()
        self.sanEdit.setText("4")
        gridLayout.addWidget(self.sanEdit, 3, 1)

        # Westmere bridge input
        self.wesLabel = QtGui.QLabel('Westmere')
        gridLayout.addWidget(self.wesLabel, 4, 0)
        self.wesEdit = QtGui.QLineEdit()
        self.wesEdit.setText("2")
        gridLayout.addWidget(self.wesEdit, 4, 1)

        # Nehalem bridge input
        self.nehLabel = QtGui.QLabel('Nehalem')
        gridLayout.addWidget(self.nehLabel, 5, 0)
        self.nehEdit = QtGui.QLineEdit()
        self.nehEdit.setText("1")
        gridLayout.addWidget(self.nehEdit, 5, 1)

        # Harpertown bridge input
        self.harLabel = QtGui.QLabel('Harpertown')
        gridLayout.addWidget(self.harLabel, 6, 0)
        self.harEdit = QtGui.QLineEdit()
        self.harEdit.setText("1")
        gridLayout.addWidget(self.harEdit, 6, 1)

        self.sendButton = QtGui.QPushButton('Send to Amazon')
        gridLayout.addWidget(self.sendButton, 8, 1)
        self.connect(self.sendButton, QtCore.SIGNAL('clicked()'), self.send)

    def changeNodeInputs(self):
      # preference = self.prefCombo.currentText()
      preference = self.prefCombo.itemData(self.prefCombo.currentIndex()).toString()
      print >> sys.stderr, preference

      if preference == "performance":
        self.sanEdit.setText("4")
        self.wesEdit.setText("2")
        self.nehEdit.setText("1")
        self.harEdit.setText("1")
      elif preference == "cost":
        self.sanEdit.setText("1")
        self.wesEdit.setText("1")
        self.nehEdit.setText("2")
        self.harEdit.setText("4")
      elif preference == "manual":
        self.sanEdit.setText("0")
        self.wesEdit.setText("0")
        self.nehEdit.setText("0")
        self.harEdit.setText("0")

    def send(self):
    
        # this line prints out the latest workflow name which we can leverage later
        #workflow_name = api.get_available_versions()[1][api.get_available_versions()[0][-1]]
	workflow_name="tmp"
        
        # login info
        username = loginWindow.username
        password = loginWindow.password
        
        vt_filepath = api.get_current_controller().get_locator().name
	print >> sys.stderr, "##### vt_filepath: "+vt_filepath
        remote_filename = username + "_" + str(uuid.uuid4()) + "_" + vt_filepath.split('/')[-1][:-3]

        # spawn the scp pexpect thread and login
        config_text = "email: "+str(self.emailEdit.text())+"\\nworkflow_name: "+str(workflow_name)+"\\nscheduling: "
        config_text += "\\n    type: "+str(self.prefCombo.itemData(self.prefCombo.currentIndex()).toString())
        """
        config_text += "\\n    ncpus: "+str(self.ncpusEdit.text())
        config_text += "\\n    node: "+str(self.nodeCombo.itemData(self.nodeCombo.currentIndex()).toString())
        config_text += "\\n    select: "+str(self.selectEdit.text())
        """
	print >> sys.stderr, "##### config_text: "+config_text

	#look at http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AccessingInstancesLinux.html
	command=ssh_command_pre+" \"echo -ne '"+config_text+"' >> ~/hecc/Server/config/"+remote_filename+".yml" + "\""

	print >> sys.stderr, "##### ssh_command: "+command
	os.system(command)

	#Sample: scp -i ~/Downloads/gonghankey.pem test.py ubuntu@ec2-54-200-158-71.us-west-2.compute.amazonaws.com:~/hecc/job_queue

	destination="~/hecc/Server/job_queue/"+remote_filename+".vt"
	command=scp_command_pre+" "+vt_filepath+" ubuntu@"+public_dns+":"+destination
	print >> sys.stderr, "##### scp_command: "+command
	os.system(command)

        self.hide()


class AmazonPlugin(Module):
    """AmazonPlugin is an adapter to Amazon"""

    def __init__( self ):
        Module.__init__(self)

    def is_cacheable(self):
        return False

    def compute(self):
        print >> sys.stderr," Compute "
        # grab input information from the ports
        #self.vt_filepath = self.forceGetInputFromPort( "vt_filepath" )
        #self.remote_filename = self.forceGetInputFromPort( "remote_filename" )
        #self.username = self.forceGetInputFromPort( "username" )
        #self.password = self.forceGetInputFromPort( "password" )
        #self.sendMode = self.forceGetInputFromPort( "send mode", True )

        # flag the operation as completed
        #self.setResult( "complete flag", True )

###############################################################################

def initialize(*args, **keywords):

    # We'll first create a local alias for the module registry so that
    # we can refer to it in a shorter way.
    basic = core.modules.basic_modules
    reg = core.modules.module_registry.registry
    reg.add_module(AmazonPlugin)
    
    global loginWindow, jobstatusWindow, sendWindow, webWindow, estimatorWindow
    loginWindow = LoginViewer()
    jobstatusWindow = JobStatusViewer()
    sendWindow = SendViewer()
    webWindow = QWebView()
    estimatorWindow=EstimatorViewer()

###################

def menu_items():

    def view_usages():
        usageWindow.show()
        usageWindow.activateWindow()
        usageWindow.raise_()

    def view_cpu_usage():
        webWindow.load(QUrl("http://www.nas.nasa.gov/monitoring/hud/realtime/pleiadespanel1.html"))
        webWindow.resize(350,540)
        webWindow.show()
        webWindow.activateWindow()
        webWindow.raise_()

    def view_pbs_status():
        #webWindow.load(QUrl("http://www.nas.nasa.gov/monitoring/hud/realtime/pleiadespanel2.html"))
        #webWindow.resize(280,380)
        #webWindow.show()
        #webWindow.activateWindow()
        #webWindow.raise_()
	estimatorWindow.show()
	estimatorWindow.activateWindow()
	estimatorWindow.raise_()

    def view_filesystem_usage():
        webWindow.load(QUrl("http://www.nas.nasa.gov/monitoring/hud/realtime/pleiadespanel3.html"))
        webWindow.resize(320,450)
        webWindow.show()
        webWindow.activateWindow()
        webWindow.raise_()

    def view_jobstatus():
        jobstatusWindow.show()
        jobstatusWindow.activateWindow()
        jobstatusWindow.raise_()
        jobstatusWindow.updateStatus()

    def log_on_Amazon():
        loginWindow.show()
        loginWindow.activateWindow()
        loginWindow.raise_()

    def send_to_Amazon():
        sendWindow.show()
        sendWindow.activateWindow()
        sendWindow.raise_()

    lst = []
    lst.append(("Log on Amazon", log_on_Amazon))
    lst.append(("Send to Amazon", send_to_Amazon))
    lst.append(("View CPU Usage", view_cpu_usage))
    lst.append(("Go to estimator", view_pbs_status))
    lst.append(("View File System Status", view_filesystem_usage))
    lst.append(("View Job Status", view_jobstatus))
    return tuple(lst)
