import os, shutil
import System
#from System.IO import Directory, Path
import clr

import string

#Adding the uniqe ANSYS API's
clr.AddReference("Ans.UI.Toolkit")
clr.AddReference("Ans.UI.Toolkit.Base")
from Ansys.UI.Toolkit import *


filepath = ""
activedirc = '.'
errors = []
version = 2.01b
status = "released"

class Settings:
	def __init__(self):
		self.filepath = ""
		self.activedirc = ""


def __init__(context):
	setting = Settings()	
	ExtAPI.Log.WriteMessage("Init SGRE Workflow, version:" + str(version) + " ,Status:" + str(status))
	ExtAPI.Log.WriteMessage("Program created by: EDRmedeso Aps. Jul18,Tech/AFL")
	ExtAPI.Log.WriteMessage("MD5> fc9d3606-bb55-8f0f-8336-fc264ec82976")
	return True

#-------------Input -----------------------------
	
def updateInput(task):
	""" Running these lines of code when the update task in WB is activated.
		The aggrument task is a UserTask
	"""	
	ExtAPI.Log.WriteMessage('updating task ' + task.Name)
	#Finding ObjectTest directory in WB project task when Updating.
	if 'Input' in task.Name: 		
		ExtAPI.Log.WriteMessage('Updating the Input task')
		
		inputfilepath = task.Properties['SelectInputAPDLFile'].Value	
		inputReferencePath = task.Properties[1].Properties['SelectReferenceAPDLdir'].Value
		inputRefFilters = task.Properties[1].Properties['RefFileFilter'].Value

		ExtAPI.Log.WriteMessage('InputReferencePath :' + inputReferencePath)
		ExtAPI.Log.WriteMessage('InputRefFilters :' + inputRefFilters)
		
		#mapdlInputFile1 = setup1.AddInputFile(FilePath="") #removing peviously set input files 		
		#Setting the filepath in the MAPDL setup, scirpt file is now move to the dp0 directory if the project.
		#changing the directory path seperator - DAMMM Windows
		
		#Becasue of the UserTask structure, it does not directly link back to the Automated ACT Taskgroup
		#Containing the Extrenal Task Mechanical APDL		
		system1 = task.TaskGroup.InternalObject #this returns some thing like: /Schematic/System:CSTRUCT
		system1Name = system1.Name #now we have the abbreviation "CSTRUCT" of the Automated TaskGroup
		system1 = GetSystem(Name=system1Name)
		setup1 = system1.GetContainer(ComponentName="Setup")
		ExtAPI.Log.WriteMessage('Task setup1 name: ' + setup1.Name)

		if os.path.isfile(inputfilepath):						
			#Adding input file
			mapdlInputFile1 = setup1.AddInputFile(FilePath=inputfilepath)			
			#Adding reference files
			APDLfilePath = task.ActiveDirectory	
			APDLfilePath = os.path.dirname(APDLfilePath)
			#APDLfilePath = os.path.abspath(APDLfilePath.replace('\\','/'))
			APDLfilePath = APDLfilePath + '\\ANSYS'
			ExtAPI.Log.WriteMessage('Info: APDLfilePath dirc :' + APDLfilePath)	
			#Get filters	
			filtersList = inputRefFilters.split(';')

			#Starts the copying of the Outputfiles	
			if not copyFiles(filtersList, inputReferencePath, APDLfilePath, False, [inputfilepath], False):
				ExtAPI.Log.WriteMessage('Error: Error ourcurred in Copying of reference files')
				return False

			#Making sure that the input file is still the selected input file
			#mapdlInputFile1 = setup1.AddInputFile(FilePath=
			mapdlInputFile1 = setup1.AddInputFile(FilePath=inputfilepath)			
			Settings.filepath = inputfilepath
			ExtAPI.Log.WriteMessage('Mapdl Input file set automatically')
			return True
		else:
			ExtAPI.Log.WriteMessage('ERROR: Input file at:' + inputfilepath + 'not found')
			ExtAPI.Log.WriteMessage('Warning: Mapdl Input file not set automatically:')
			return False

def taskinit(task):
	""" Initialing the input task in WB """
	ExtAPI.Log.WriteMessage('Task initialized: ' + task.Name)
	#Setting a node maybe
	#Setting a default path (previous used
	return True
	
def OnInit(entity, property):
	#Setting default path in the Selection of Input file
	property.Value = "" #Setting a blank input file
	ExtAPI.Log.WriteMessage('Info: The input filepath has been reset')
	return True

def InputFileTypeCheck(entity, property):
	#Check the chosen file type is correct. 	
	global filepath
	ExtAPI.Log.WriteMessage('Info: InputFileTypeCheck property.Value : ' + str(property.Value))
	if property.Value != "":
		filepath = property.Value
		#print filepath
		#ExtAPI.Log.WriteMessage('InputFileTypeCheck property.Value : ' + filepath)
		#os.path.splitext()
		fileext = System.IO.Path.GetExtension(filepath)
		#dirn = System.IO.Path.GetDirectoryName(System.IO.Path.GetFullPath(filepath))
		#entity.Properties[1].Properties[0].Value = dirn
		
		if fileext in [".cdb",".inp", ".db", ".txt"]:		
			#ExtAPI.Log.WriteMessage('Seleted ADPL File supported, file extension: ' + fileext)
			if InputFilePathChanged(entity, property):								
				#entity.AllProperties[2].Value = dirn
				return True
			else:
				return False
		else:
			ExtAPI.Log.WriteMessage('Seleted ADPL input File type not supported, file extension: ' + fileext)
			return False
	else:
		return False

def InputFilePathChanged(entity, property):	
	#Called when the user changes the filepath chacking the access to the file
	#global filepath
	if property.Value != "":
		filepath = property.Value		
		full_filepath = System.IO.Path.GetFullPath(filepath)	
			
		if System.IO.File.Exists(full_filepath):				
			return True
		else:			
			return False

def InputValidate(entity, property):		
	ExtAPI.Log.WriteMessage('Info: Input file OnValidate Callback')
	#InputFilePathChanged_OnValidate(entity, property)
	return True

def InputApply(entity, property):		
	ExtAPI.Log.WriteMessage('Info: Input file OnApply CAllback')
	if property.Value != "":		
		Infile = property.Value
		ExtAPI.Log.WriteMessage('Info: Input Apply  input file : ' + Infile)
		dirn = System.IO.Path.GetDirectoryName(System.IO.Path.GetFullPath(Infile))
		ExtAPI.Log.WriteMessage('Info: Reference file path has been set to: ' + dirn)
		OnInitRef(entity, entity.Properties[1].Properties['SelectReferenceAPDLdir'], dirn)
		#entity.Properties[1].Properties['SelectReferenceAPDLdir'].Value = dirn	
	return True

def Input_String2Value(entity, property, value):
	ExtAPI.Log.WriteMessage('Info: Input file Input_String2Value CAllback')
	return True

def OnInitRef(entity, property, Value=""):
	#Setting the reference file path to input file directory
	property.Value = Value
	ExtAPI.Log.WriteMessage('Info: Reference file path has been reset')
	return True

def InputApplyRef(entity, property):
	ExtAPI.Log.WriteMessage('Info: Reference file path -  OnApply Callback')	
	return True
	
def InputValidateRef(entity, property):
	ExtAPI.Log.WriteMessage('Info: Reference file path -  OnValidate Callback')
	ExtAPI.Log.WriteMessage('Info: Reference file path  change to: ' + property.Value)
	return True
	
def RefFileFilterCheck(entity, property):
	#Check the selected filter setting for the reference filter
	if filterCheck(property, filterString=['txt','inp','xml','db','rst','log','out','all','*','','*.*']):
		return True
	else: 		
		return False 

#------------- MADPL -----------------------------
def updateMapdl(task):	
	#Updating the MAPDL task in the TaskGroup - NOT USED - Can not get at Custom callback from a external task
	Settings.activedirc = task.ActiveDirectory	

	system1 = task.TaskGroup.InternalObject #this returns some thing like: /Schematic/System:CSTRUCT
	system1Name = system1.Name #now we have the abbreviation "CSTRUCT" of the Automated TaskGroup
	system1 = GetSystem(Name=system1Name)
	
	input1 = system1.GetContainer(ComponentName="Input")
	inputfilepath = input1.Properties['SelectInputAPDLFile'].Value	
	inputReferencePath = input1.Properties['SelectReferenceAPDLdirc'].Value
	inputRefFilters = input1.Properties['RefFileFilter'].Value
	
	ExtAPI.Log.WriteMessage('Info: inputReferencePath dirc :' + inputReferencePath)	

	#Adding reference files
	APDLfilePath = setup1.ActiveDirectory	
	APDLfilePath = os.path.dirname(APDLfilePath)
	#APDLfilePath = os.path.abspath(APDLfilePath.replace('\\','/'))
	APDLfilePath = APDLfilePath + '\\ANSYS'
	ExtAPI.Log.WriteMessage('Info: APDLfilePath dirc :' + APDLfilePath)	

	#if not System.IO.Directory.Exists(APDLfilePath):
	#	ExtAPI.Log.WriteMessage('Info: Directory not found :' + str(APDLfilePath))	
	#	return False	
	#ExtAPI.Log.WriteMessage('Info: files in ActiveMAPDL dirc :' + str(files))	
	
	#Get filters	
	filtersList = inputRefFilters.split(';')

	#Starts the copying of the Outputfiles	
	if not copyFiles(filtersList, inputReferencePath, APDLfilePath, False, [], False):
		ExtAPI.Log.WriteMessage('Error: Error ourcurred in Copying of reference files')
		return False

	"""
	Reffiles=[]	
	for (path, dirc, files) in os.walk(inputReferencePath):
		temp = System.IO.Path.Combine(path, file) #full path til the file
		if not temp == inputfilepath:
			Reffiles.append(temp) #sourcefile
			ExtAPI.Log.WriteMessage('Info: Adding file :' + temp)
			setup1.AddFile(FilePath=temp)
		else:
			ExtAPI.Log.WriteMessage('Info: Input file allready added:' + temp)
	"""

	#Adding input file
	setup1 = system1.GetContainer(ComponentName="Setup")
	if System.IO.File.Exists(inputfilepath):
		mapdlInputFile1 = setup1.AddInputFile(FilePath=inputfilepath) 
	return True


#------------- Output -----------------------------		
def updateOutput(task):
	"""updating the Data out task in the TaskGroup"""
	#Getting the Mapdl for this TaskGroup Active directory
	#property.Value = ""
	ExtAPI.Log.WriteMessage('Info: Updating the Output task')
	systemName = task.TaskGroup.InternalObject.Name	
	ExtAPI.Log.WriteMessage('SystemName : ' + systemName)	
	setup1 = ExtAPI.DataModel.GetTaskGroupById(systemName).Tasks[1]
	activeDir = setup1.ActiveDirectory
	ExtAPI.Log.WriteMessage('Info: ActiveMAPDL dirc :' + activeDir)	

	APDLfilePath = setup1.ActiveDirectory	
	APDLfilePath = os.path.dirname(APDLfilePath)
	#APDLfilePath = os.path.abspath(APDLfilePath.replace('\\','/'))
	APDLfilePath = APDLfilePath + '\\ANSYS'
	ExtAPI.Log.WriteMessage('Info: APDLfilePath dirc :' + APDLfilePath)	
	
	if not System.IO.Directory.Exists(APDLfilePath):
		ExtAPI.Log.WriteMessage('Info: Directory not found :' + str(APDLfilePath))	
		return False
	
		ExtAPI.Log.WriteMessage('Info: files in ActiveMAPDL dirc :' + str(files))	
	
	#get filters
	filters = task.Properties['FileFilter'].Value
	filtersList = filters.split(';')

	# starts the copying of the Outputfiles
	DataOut = ExtAPI.DataModel.GetTaskGroupById(systemName).Tasks[2]
	DataOutDirc = DataOut.Properties['OutputDirectory'].Value
	DeleteFilesInDP = DataOut.Properties['DeleteDPs'].Value
	if copyFiles(filtersList, APDLfilePath, DataOutDirc, DeleteFilesInDP):
		return True
	else:
		return False
	
def OninitOutput(entity, property):
	#empty the output directory path
	ExtAPI.Log.WriteMessage('Info: initializing Output: ')
	property.Value = ""	
	return True	
	
def OutputFileFilterCheck(entity, property):
	#Checking the selected filter types - Receiving a String like jpg;rst;...,all 
	if filterCheck(property, filterString=['txt','db','rst','inp','dsp','err','esav','full','log','mntr','out','all','*','']):
		return True
	else: 
		return False 

def OutputFilePathChanged(entity, property):
	#checking the path of the selected output file directory
	if property.Value != "":
		if not System.IO.Directory.Exists(property.Value):
			ExtAPI.Log.WriteMessage('The Output directory :' + property.Value + 'was not found, files are not copied')
			#ExtAPI.Log.WriteMessage('INFO: Output file located at :' + Settings.activedirc)
			return False
		else:
			#ExtAPI.Log.WriteMessage('INFO: Output file located at :' + Settings.activedirc)
			return True
	else: 
		return False

def DeleteDP(entity, property):
	pass
	return True 

#------------- Global WB -----------------------------
def onBeforeUpdate(task):
	#Call before a global project update is done
	msg = getPrintMessage('pre-update', task)
	print msg
	return True

def onAfterUpdate(task):
	#called after a successfull completion of all task in a TaskGroup, continues though all TaskGroups in project
	msg = getPrintMessage('post-update', task)
	print msg
	return True

def onAfterSourcesChanged(task):
	#called after a change in one of the tasks in a TaskGroup, continues though all TaskGroups in project
	msg = getPrintMessage('Task changed', task)
	print msg
	return True

def getPrintMessage(msg, task):
    taskName = 'none'
    if task != None:
        taskName = task.Name
    return 'in ' + msg + ' callback for task ' + task.Name
	#global filepath


#------------ General --------------------------
def filterCheck(property, filterString=['all']):	
	out = []	
	#ExtAPI.Log.WriteMessage('Info: Seleted ...: ' + str(property.Value))
	filters = str(property.Value) 
	filters = filters.replace(',',';') #changing , to ;
	filters = filters.replace(' ','') # removing white spaces		
	filtersList = filters.split(';')
	for filter in filtersList:
		filter = filter.lower()
		#ExtAPI.Log.WriteMessage('File Filter : ' + filter)
		if filter == '*.*':
			out.append('True')
		else: 
			filter = filter.replace('.','')
			if filter in filterString:
				out.append('True')
			else:
				out.append('False')

	#property.Value = filters
	#ExtAPI.Log.WriteMessage('filter list Out : ' + str(out))
	
	if 'False' in out:
		#ExtAPI.Log.WriteMessage('False found in list Out, returning False')
		return False		
	else:		
		return True

def copyFiles(filtersList, InDirc, OutDirc, DeleteFiles=False, FilesNot2Copy=[], symlinks=False):	
	#Copying of files 		
	files = os.listdir(InDirc)	
	#for (path, dirc, files) in os.walk(InDirc):
	path = System.IO.Path.GetFullPath(InDirc) #System.IO.Path.GetDirectoryName(InDirc)
		
	#filter files list
	FilesToCopy = []
	if '*' or '*.*' or 'all' in filtersList: #all files
		FilesToCopy = files
	else:
		for file in files:	# some of the files, links or subdirc 
			if symlinks and os.path.islink(System.IO.Path.Combine(path, file)):
				FilesToCopy.append(file)
			elif os.path.isdir(System.IO.Path.Combine(path, file)):
				FilesToCopy.append(file)
			else: 
				if System.IO.Path.GetExtension(file)[1:] in filtersList:
					FilesToCopy.append(file)
		
	# Added a removal of the allready selected Mapdl input file.
	#ExtAPI.Log.WriteMessage("files: " +  System.IO.Path.Combine(path, files[0]))
	#ExtAPI.Log.WriteMessage("FilesNot2Copy: " + FilesNot2Copy[0])	
	tmp = FilesToCopy
	for fileNot2Copy in FilesNot2Copy:
		for indx, val in enumerate(FilesToCopy):
			fullPath_source = System.IO.Path.Combine(path, val)
			#fullPath_source = System.IO.Path.GetFullPath(val)
			if fileNot2Copy.lower() in fullPath_source.lower():
				del(tmp[indx])	
	FilesToCopy = tmp
	
	for name in FilesToCopy: 
		#ExtAPI.Log.WriteMessage('Info: file found ActiveMAPDL dirc :' + str(file))	
		fullPath_source = System.IO.Path.Combine(path, name) #sourcefile or folder full abs path		
		#fullPath_source = System.IO.Path.GetFullPath(name)		
		fullPath_target = System.IO.Path.Combine(OutDirc, name) #targetfile or folder		
		
		ExtAPI.Log.WriteMessage('Info Source :' + fullPath_source + ' Target :' +  fullPath_target)
		
		#name can be a list or a link!!!!
		try:
			if symlinks and os.path.islink(fullPath_source):
				linkto = os.readlink(fullPath_source)
				os.symlink(linkto, fullPath_target)
			elif os.path.isdir(fullPath_source):
				if not System.IO.Directory.Exists(fullPath_target):
					System.IO.Directory.CreateDirectory(fullPath_target)
				copyFiles(filtersList, fullPath_source, fullPath_target, DeleteFiles, FilesNot2Copy, symlinks)
			else:
				#copying files in stored list
				if System.IO.File.Exists(fullPath_source):
					System.IO.File.Copy(fullPath_source, fullPath_target)				
					#copy2(fullPath_source, fullPath_target)
					ExtAPI.Log.WriteMessage('Info: file copied:')	
				
				#Deleting Source file in Dp0
				if DeleteFiles:
					ExtAPI.Log.WriteMessage('Info: file delete at Source as Requested:')	
					System.IO.File.Delete(fullPath_source)
					
		except (IOError, os.error) as why:
			ExtAPI.Log.WriteMessage('ERROR in copyfile Scr: ' + str(fullPath_source) + '\nDst: ' + str(fullPath_target) + '\nFailed:' + str(why))
			return False 
			
	#ExtAPI.Log.WriteMessage('Updating the DataOut routine')	
	return True
