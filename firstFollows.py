file = open("firstFollows","r")
string_list= file.readlines()
firsts={}
follows={}
for i in string_list:
    line = i.split("\t")
    for j in range(0,len(line)) :
        line1= line[j].split()
        if(j==0):
            name = line1[0]
        if(j==1):
            firsts[name]=line1
        elif(j==2):
            follows[name]=line1
        elif(j==3):
            if(line1[0]=="yes"):
                firsts[name].append('ep')
def get_first() :
    new_dict={}
    for i in firsts.keys():
        new_dict[i]=[]
    for i in firsts.keys():

        for j in firsts[i] :
            if(j=="eof"):
                instead="EOF"
                new_dict[i].append(instead)
            elif(j=="lt"):
                instead = "<"
                new_dict[i].append(instead)
            elif (j == "equal"):
                instead = "="
                new_dict[i].append(instead)
            elif (j == "~"):
                instead = "=="
                new_dict[i].append(instead)
            elif (j == "oAcl"):
                instead = "{"
                new_dict[i].append(instead)
            elif (j == "cAcl"):
                instead = "}"
                new_dict[i].append(instead)
            elif (j == "oBrac"):
                instead = "["
                new_dict[i].append(instead)
            elif (j == "cBrac"):
                instead = "]"
                new_dict[i].append(instead)
            elif (j == "minus"):
                instead = "-"
                new_dict[i].append(instead)
            elif (j == "comma"):
                instead = ","
                new_dict[i].append(instead)
            else:
                new_dict[i].append(j)
    return new_dict
def get_follow() :
    new_dict={}
    for i in follows.keys():
        new_dict[i]=[]
    for i in follows.keys():

        for j in follows[i] :
            if(j=="eof"):
                instead="EOF"
                new_dict[i].append(instead)
            elif(j=="lt"):
                instead = "<"
                new_dict[i].append(instead)
            elif (j == "equal"):
                instead = "="
                new_dict[i].append(instead)
            elif (j == "~"):
                instead = "=="
                new_dict[i].append(instead)
            elif (j == "oAcl"):
                instead = "{"
                new_dict[i].append(instead)
            elif (j == "cAcl"):
                instead = "}"
                new_dict[i].append(instead)
            elif (j == "oBrac"):
                instead = "["
                new_dict[i].append(instead)
            elif (j == "cBrac"):
                instead = "]"
                new_dict[i].append(instead)
            elif (j == "minus"):
                instead = "-"
                new_dict[i].append(instead)
            elif (j == "comma"):
                instead = ","
                new_dict[i].append(instead)
            else:
                new_dict[i].append(j)
    return new_dict

