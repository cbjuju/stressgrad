# -*- coding: mbcs -*-
#
# Abaqus/CAE Release 2018 replay file
# Internal Version: 2017_11_07-11.21.41 127140
# Run by skunda on Fri Apr 16 05:57:04 2021
#

# from driverUtils import executeOnCaeGraphicsStartup
# executeOnCaeGraphicsStartup()
#: Executing "onCaeGraphicsStartup()" in the site directory ...
from abaqus import *
from abaqusConstants import *
session.Viewport(name='Viewport: 1', origin=(1.36719, 1.36719), width=201.25, 
    height=135.625)
session.viewports['Viewport: 1'].makeCurrent()
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
execfile('driver.py', __main__.__dict__)
#: Warning: An output database lock file /home/skunda/problems/cylinderCompression/fivePercentQuadTets/Job.lck has been detected. This may indicate that the output database is opened for writing by another application.
#: /home/skunda/problems/cylinderCompression/fivePercentQuadTets/Job.odb will be opened read-only. 
#: Model: /home/skunda/problems/cylinderCompression/fivePercentQuadTets/Job.odb
#: Number of Assemblies:         1
#: Number of Assembly instances: 0
#: Number of Part instances:     1
#: Number of Meshes:             1
#: Number of Element Sets:       403
#: Number of Node Sets:          56
#: Number of Steps:              1
print 'RT script done'
#: RT script done