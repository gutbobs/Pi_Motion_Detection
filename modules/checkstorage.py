import os
import glob
import sys

''' this module checks the storage folder specified in the variables file 
and makes sure it's contents do not exceed the size limit specified in it. 
When the total file size of the contents meets or exceeds the limit, 
the oldest files are removed until the total size is under the limit
'''

def GetTotalSize(variables):
	folder_to_check = variables['file_path']
	total_size = 0
	for dir_path, dir_names, filenames in os.walk(folder_to_check):
		for f in filenames:
			fp = os.path.join(dir_path,f)
			total_size += os.path.getsize(fp)

	return total_size

def RemoveOldFiles(variables):
	folder_to_check = variables['file_path']
	total_size = 0
	bytes_to_clean = variables['bytes_to_clean'] 
	files = glob.glob(os.path.join(folder_to_check,'*'))
	files.sort(key = os.path.getmtime)

	files_to_delete = []
	for f in files:
		total_size += os.path.getsize(f)
		if total_size < bytes_to_clean:
			files_to_delete.append(f)
		else:
			break

	for f in files_to_delete:
		os.remove(f)

if __name__ == "__main__":
	global_variables={"file_path":sys.argv[1],
				"max_folder_size_in_gb" : 5
				}
	global_variables['total_used_storage'] = GetTotalSize(global_variables)
	print global_variables

	max_permitted_size = global_variables["max_folder_size_in_gb"] * 1024 * 1024 * 1024
	global_variables['bytes_to_clean'] = global_variables['total_used_storage'] - max_permitted_size 
	print global_variables,max_permitted_size
	if global_variables['bytes_to_clean']  >= 0:
		print "Old files need to be deleted"
		RemoveOldFiles(global_variables)
