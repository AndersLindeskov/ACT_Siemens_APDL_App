import os, shutil
import System
import clr
global filepath

def update(task):
	ExtAPI.Log.WriteMessage('updating task ' + task.Name)
	
	#Finding ObjectTest directory in WB project task when Updating.
	
	if 'ObjectTest' in task.Name: 
		ExtAPI.Log.WriteMessage('ObjectTest found in Group' + task.Properties["GroupName"])
		system1 = GetSystem(task.Properties["GroupName"])
		setup1 = system1.GetContainer(ComponentName='Setup')
		PropA = task.Properties['NumberOfSteps'].Value
		mapdlInputFile1 = setup1.AddInputFile(FilePath=propA)
		
		
		
		# setup1 =
	
		# activeDir = task.ActiveDirectory
		# ExtAPI.Log.WriteMessage('activeDir name ' + activeDir.Name)
	
# #		for ts in ExtAPI.DataModel.TaskGroups:
# #			for t in ts:
# #				t.Name ['ObjectTest']
	
	
	# if task.Name[:10] == 'ObjectTest':
		# for i in range(len(ExtAPI.DataModel.TaskGroups)):
			# for j in range(len(ExtAPI.DataModel.TaskGroups[i].Tasks)):
				# if ExtAPI.DataModel.TaskGroups[i].Tasks[j].Name == task.Name:
					# task_name = ExtAPI.DataModel.TaskGroups[i].Name
		# system1 = GetSystem(task_name)
		# setup1 = system1.GetContainer(ComponentName='Setup')
		# propA = task.Properties['NumberOfSteps'].Value
		# mapdlInputFile1 = setup1.AddInputFile(FilePath=propA)

def taskinit(task):
	ExtAPI.Log.WriteMessage('updating task ' + task.Name)
	
def OnInit(task,property):
	test = Project.GetProjectFile()
	ExtAPI.Log.WriteMessage(test)
	
	
	
	
	#	for k in range(4):
	#		(filepath, filename) = os.path.split(filepath)
	#	ExtAPI.Log.WriteMessage(filepath)
	#	ExtAPI.DataModel.Tasks[0].Properties['NumberOfSteps'].Value = filepath
	#else:
	#	for i in range(len(ExtAPI.DataModel.Tasks)):
	#		if ExtAPI.DataModel.Tasks[i].Name[:5] == 'Setup':
	#			ExtAPI.DataModel.Tasks[i].ImageName = 'ansys'
