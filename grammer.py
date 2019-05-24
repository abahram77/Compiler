file = open("grammer","r")
string_list= file.readlines()
grammer={}


def get_nonterminal(str):
    if (str in grammer.keys()):
        return

    grammer[str] = []


for i in string_list :
    if(i[-1]=="\n"):
        i=i[0:-1]

    splitted = i.split()

    get_nonterminal(splitted[0])
    grammer[splitted[0]].append(splitted[2:])


def get_grammer() :
    new_dict={}
    for i in grammer.keys():
        new_dict[i]=[]
    for i in grammer.keys():

        for j in grammer[i] :
            list=[]
            for k in j:
                if(k=="eof"):
                    instead="EOF"
                    list.append(instead)
                elif(k=="lt"):
                    instead = "<"
                    list.append(instead)
                elif (k == "equal"):
                    instead = "="
                    list.append(instead)
                elif (k == "~"):
                    instead = "=="
                    list.append(instead)
                elif (k == "oAcl"):
                    instead = "{"
                    list.append(instead)
                elif (k == "cAcl"):
                    instead = "}"
                    list.append(instead)
                elif (k == "oBrac"):
                    instead = "["
                    list.append(instead)
                elif (k == "cBrac"):
                    instead = "]"
                    list.append(instead)
                elif (k == "minus"):
                    instead = "-"
                    list.append(instead)
                elif (k == "comma"):
                    instead = ","
                    list.append(instead)
                else:
                    list.append(k)

            new_dict[i].append(list)
    return new_dict

