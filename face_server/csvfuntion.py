import csv

array=[]
for i in range(3):
    array.append([])
print(array)

nullplace=[]
for i in range(3):
    nullplace.append([])
print(nullplace)


def load_and_tmp(name):
    typenum=0
    with open('./'+name+'.csv', 'r', newline='',encoding='utf_8_sig') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        tmp = list(reader)
        if name =="adv":
            typenum=1
        if name == "costo":
            typenum=2
        array[typenum]=tmp
        for i in range(len(tmp)):
            if (tmp[i][0]==''):
                nullplace[typenum].append(i)
                print (nullplace[typenum])
                #print("costo 2 =''")
                
        if typenum < 2 : 
            for i in range(len(array[typenum])):
                array[typenum][i][1] =array[typenum][i][1]
            
def printdata(name):  #顧客本身有空值解決，但其他有空值暫無解決，參考鍵有空值暫無解決
    typenum=0
    count=0
    if name =="adv":
        typenum=1
    if name == "costo":
        typenum=2
    print(name)
    for i in range(len(array[typenum])):
            if len(nullplace[typenum])>0:
                if count <len(nullplace[typenum]):
                    if i == nullplace[typenum][count]:
                        count+=1
                        continue                
            if typenum < 2 :
                print(array[typenum][i][0],array[typenum][i][1])
                continue
            if typenum == 2:
                if i ==0 :
                    print(array[typenum][0][0],
                      array[typenum][0][1],
                      array[typenum][0][2],
                      array[typenum][0][3])
                    continue
                print(array[typenum][i][0],
                      array[typenum][i][1],
                      array[typenum][i][2],
                      array[typenum][i][3])

def add_new(name,content,oke_content="",adv_content=""):
    typenum=0
    if name =="adv":
        typenum=1
    if name == "costo":
        typenum=2
    if_null=0
    
    if typenum<2:
        for i in range(len(array[typenum])):
            if len(array[typenum][i]) == 0 :
                array[typenum][i]=[i,content]
                if_null=1
        if if_null ==0:
            array[typenum].append([(len(array[typenum])),content])
    if typenum==2:
        for i in range(len(array[typenum])):
            if len(array[typenum][i]) == 0 :
                array[typenum][i]=[i,oke_content,adv_content,content]
                if_null=1
        if if_null ==0:
            array[typenum].append([(len(array[typenum])),oke_content,adv_content,content])
            
    with open(name+'.csv', 'w', newline='',encoding='utf_8_sig') as csvfile:
        writer = csv.writer(csvfile)
        for i in range(len(array[typenum])):
            writer.writerow(array[typenum][i])
            

def change_new(name,target,content,oke=0,adv=0):
    typenum=0
    if name =="adv":
        typenum=1
    if name == "costo":
        typenum=2
    
    tmp_tar=0
    if typenum<2:
        for i in range(len(array[typenum])):
                if i ==0:
                    continue
                if array[typenum][i][0] == '':
                    continue
                if int(array[typenum][i][0]) == target:
                    tmp_tar=i
                    break
        if(tmp_tar>0):
            array[typenum][tmp_tar]=[tmp_tar,content]
        if(tmp_tar==0):
            print("查無資料")
    if typenum == 2:
        for i in range(len(array[typenum])):
                if i == 0:
                    continue
                if array[typenum][i][0]=='':
                    continue
                if int(array[typenum][i][0]) == int(target):
                    tmp_tar=i
                    break
        if(tmp_tar>0):
            array[typenum][tmp_tar]=[tmp_tar,oke,adv,content]
        if(tmp_tar==0):
            print("查無資料")
    with open(name+'.csv', 'w', newline='',encoding='utf_8_sig') as csvfile:
        writer = csv.writer(csvfile)
        for i in range(len(array[typenum])):
            writer.writerow(array[typenum][i])

def delete_new(name,target):
    typenum=0
    if name =="adv":
        typenum=1
    if name == "costo":
        typenum=2
    count=0
    tmp_tar=0
    if typenum<2:
        for i in range(len(array[typenum])):             
                if i ==0:
                    continue
                if len(nullplace[typenum]):
                    if count<len(nullplace[typenum]):
                        if i == nullplace[typenum][count] :
                            count+=1
                            continue
                if int(array[typenum][i][0]) == target:
                    tmp_tar=i
                    break
        if(tmp_tar>0):
            array[typenum][tmp_tar]=['','']
        if(tmp_tar==0):
            print("查無資料")
    if typenum==2:
        for i in range(len(array[typenum])):             
                if i ==0:
                    continue
                if len(nullplace[typenum]):
                    if count<len(nullplace[typenum]):
                        if i == nullplace[typenum][count] :
                            count+=1
                            continue
                #print(array[typenum][i][0],target)
                if int(array[typenum][i][0]) == target:
                    tmp_tar=i
                    break
        if(tmp_tar>0):
            array[typenum][tmp_tar]=["","","",""]
        if(tmp_tar==0):
            print("查無資料")
    with open(name+'.csv', 'w', newline='',encoding='utf_8_sig') as csvfile:
        writer = csv.writer(csvfile)
        for i in range(len(array[typenum])):
            writer.writerow(array[typenum][i])
print(load_and_tmp('adv'))