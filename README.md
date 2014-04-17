vistrails_aws_plugin
====================


----------


Configuration:
--------------

Install the vistrails:

1. sudo apt-get install xvfb python-matplotlib python-suds
2. wget http://downloads.sourceforge.net/project/vistrails/vistrails/v2.0.1/vistrails-src-2.0.1-5e35e2b83b90.tar.gz
3. tar -zxvf vistrails-src-2.0.1-5e35e2b83b90.tar.gz
4. Running a workflow

  See scripts/run_vistrails_batch_xvfb.sh for more details

5. Debugging VisTrails installing or runtime issues:

  Check VisTrails’s log file: ~/.vistrails/vistrails_2_0_1.log



Install the Amazon Plugin:

1. Go to ~/.vistrails.userpackages/
2. mkdir AmazonPlugin
3. touch __init__.py
4. copy and paste the code
5. enable the plugin inside the vistrails
6. restart vistrails


Run:
--------------

 1. open vistrails
 2. import a workflow
 3. click amazon plugin and go to estimator
 4. a web page will be automatcally opened and then the workflow data will be loaded into the page.
 

Description:
--------------
To be done later.
