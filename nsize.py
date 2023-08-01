import os
current_wd = os.getcwd()
print(current_wd)
list_dr = os.listdir(current_wd)
total=0
for files in list_dr:
    print(files)
    total += os.path.getsize(files)
print (total)
for name in os.listdir(dirname):
    path = os.path.join(dirname, name)
    if os.path.isdir(path):
    
        os.chdir(path)
        walkfn(path)

def walkfn(dirname):
    output = os.path.join(dirname, 'output')
    if os.path.exists(output):
        with open(output) as file1:
            for line in file1:
                if line.startswith('Final value:'):
                    print line
    else:
        for name in os.listdir(dirname):
            path = os.path.join(dirname, name)
            if os.path.isdir(path):
                
                walkfn(path)