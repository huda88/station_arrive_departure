#!/usr/local/bin/python3


# import the module needed to do the research and the requests from internet
import urllib.request 
import re
import datetime


# find the current time and transform in 2 number 1 for the hours and 1 for the minutes, add 3 hours to have the time to check 
def time ():    
    now = str(datetime.datetime.now().time())
    now = now.split(':')
    time_to_check = [int(now[0])+3, int(now[1])]
    return now, time_to_check

# download data from the website and save it in a html file. 

def request_train(choise):
    while ('done'):
        try:
            response = urllib.request.urlopen(choise).read().decode('UTF-8')
            text = open('text.html', 'w')
            text.write( response)
            text.close()
            return 'done'
        except FileNotFoundError:
            text = open('text.html')
            raise request_train()
            
#create a dictionary with the information dowlnoad from the website

def create_dictionary(train_timelst, platform, train_from):
    lst_for_dictionary = list(zip(train_from, platform))
    lst_for_dictionary = [list(x) for x in lst_for_dictionary]

    for x in range (len(train_timelst)):
        for a in range(len(lst_for_dictionary)):
            if a == x: 
                train_timelst[x][1] = [train_timelst[x][1]]+ lst_for_dictionary[a]
    general_dictionary = dict(train_timelst)

    return general_dictionary


#search inside the file with regular expression, and use the create_dictionary to return a dictionary and a list
#of the train in the correct order

def searchinformation():
    text2 = open('text.html').read()
    train_time = re.findall(r'<span class="bold">(.*)</span>', text2)
    train_timelst = [[train_time[x], (train_time[x+1]).split(':')]for x in range(0,len(train_time),2)]
    train_in_order = [train_time[x] for x in range(0,len(train_time),2)]
    
    platform_temporary = re.findall(r'<td class="platform" headers="sq_platform">\n(.*)<br>\n&nbsp;\n</td>|' +
                                    '<td class="platform" headers="sq_platform">\n(.*)\n</td>', text2)
    platform = [y for x in platform_temporary for y in x if y !='']
    
    train_from = re.findall(r'<a href="http://fahrplan.sbb.ch/bin/stboard.exe/.*?">(.*)</a></span>', text2)
    train_from = [ x if x != 'Z&#252;rich HB' else 'Zuerich HB' for x in train_from]
    dictionary= create_dictionary(train_timelst, platform, train_from)

    return train_in_order, dictionary


# function to check the time, with actual hours.
def check_hour(dictionary):
    now, time_to_check = time()
    if time_to_check[0] < 3:
            time_to_check[0]+= 24
    new_dictionary = dict()
    for key in dictionary:
        arrival_hours = int(dictionary[key][0][0])
        arrival_minutes = int(dictionary[key][0][1])
        difference = time_to_check[0] - arrival_hours
        if 0 < difference <= 3 or difference >= 24 :
                new_dictionary[key] = dictionary[key]
        elif difference == 0 :
            if arrival_minutes <= time_to_check[1]:
                new_dictionary[key] = dictionary[key]
  
    return new_dictionary

#little function to check the lengh before the print to add one or 2 \t
def lengh (string):
    if len(string) < 8:
        print(string, end='\t\t')
    else:
        print(string, end='\t')
        
#tofrom
def tofrom (str_choise):
    if str_choise[0] == 'Arrives  ':
        return 'From'
    else:
        return 'To'
        
#printing function. column 
def print_all(now, train_in_order, new_dictionary, str_choise):
    print('\n\nActual time :\t' + now[0]+ ':' + now[1] + 2*'\t' + str_choise[0] + '\n')
    print(('- - '*20)+'\nTrain\t\tHours\t\t' + tofrom(str_choise)+ '\t\tPlatform\n' + ('- - '*20)+ '\n')
    for train in train_in_order:
        if train in new_dictionary:
            info = new_dictionary[train]
            lengh (train)
            for e in info:
                if type(e)== list:
                    a= e[0]+ ':'+ e[1]
                    lengh (a)
                else:
                    lengh (e)
            print('\n')
    print('\n' + ('- - '*20))

# Arrives or Departures

def arrives_departures(arrives, departures):
    while (True):
        choise = input('Hello, Could you specify if you want more information about:' +
                     '\nArrives = a or Departures = d' +
                     '\n\nInput your choise: ')
        if choise == 'a':
            return arrives, ('Arrives  ', 'Departures')
        elif choise == 'd':
            return departures, ('Departures', 'Arrives  ')
        else:
            print('Error, try again')
        


#function to get the input form the user and to distribuite what the function has to do 
def intput(now, train_in_order, new_dictionary, str_choise, arrives, departures, choise):
    
    while ('e'):
        name = input('\n' + ('- - '*20) +
                     'You are displaing ' + str_choise[0] +
                     '\n\nWhat do you want to display? You have many options:' +
                     '\n\nResult '+ str_choise[0] + '\t: t' +
                     '\nSpecific search' + 2*'\t' + ': s' +
                     '\nRefresh' + 3*'\t' + ': r' +
                     '\nChange to ' + str_choise[1] + '\t: c' +
                     '\nExit' + 3*'\t' + ': e' +
                     '\n\nInput your choice: ')
        if name == 't':
            print_all(now, train_in_order, new_dictionary, str_choise)
        elif name == 's':
            specific_search(now, train_in_order, new_dictionary, str_choise, arrives, departures, choise)
        elif name == 'r':
            request_train(choise)
        elif name == 'c':
            main()
        elif name == 'e':
            print('\n' + ('- - '*20) +'\n' + ('- - '*20) +
                  'Thank you for using this application. See you soon')
            return
        else:
            print('Error, try again')
            
# second input function to do the modification and have only specific train hours, or platform.
def specific_search(now, train_in_order, new_dictionary, str_choise, arrives, departures, choise):
    while ('r'):
        specific= input('\n' + ('- - '*20) +
                        '\n\nDisplay only some' + tofrom(str_choise) + 
                        '\n\nSpecific train' + 2*'\t' + ': s' +
                        '\nSpecific platform\t: p' +
                        '\n' + str_choise[0] + ' ' + tofrom(str_choise) + 2*'\t' + ': f' +
                        '\nReturn' + 3*'\t' + ': r' +
                        '\nChange to ' + str_choise[1] + '\t: c' +
                        '\n\nInput your choice: ')
    
        if specific == 's':
            search_train(now, train_in_order, new_dictionary,  str_choise)
        elif specific == 'p':
            search_values('platform', 2, new_dictionary, train_in_order, now,  str_choise)
        elif specific == 'f':
            search_values('from/ to a specific city', 1, new_dictionary, train_in_order, now, str_choise)
        elif specific == 'r':
            return
        elif specific == 'c':
            arrives_departures(arrives, departures)
        else:
            print('Error, try again')

# general input to research in dictionary 
def input_specific( name ):
    result = input ('Enter a specific ' + name + ' :')
    return result

# search for key in dictionary 
def search_train(now, train_in_order, new_dictionary, str_choise):
    one_dictionary = {}
    while (True):
        try: 
            train = input_specific ('train')
            for key in new_dictionary:
                if key == train:
                    one_dictionary[key]= new_dictionary[key]
            if len(one_dictionary) >= 1:
                print_all(now, train_in_order, one_dictionary, str_choise)
                return True
        except:
            print('Not found, try again')

# search for value in a dictionary 
def search_values(name, b, new_dictionary, train_in_order, now, str_choise):
    possibility = list()
    
    for key in new_dictionary:
        if new_dictionary[key][b] not in possibility:
            possibility.append(new_dictionary[key][b])
    print('The possibilities are:')
    for x in possibility:
        print( x , end = ', ')
    value_dictionary = {}
    while (True):
        try: 
            value = input_specific (name) 
            for key in new_dictionary:
                if value == new_dictionary[key][b]:
                    value_dictionary[key]= new_dictionary[key]
            if len(value_dictionary) >= 1:
                print_all(now, train_in_order, value_dictionary, str_choise)
                return True
        except:
            print('Not found, try again')
    
    
def main():
    arrives = 'http://fahrplan.sbb.ch/bin/stboard.exe/en?input=8505300&REQTrain_name=&boardType='\
              'arr&time=now&productsFilter=2:111101001&selectDate=today&maxJourneys=40&start=yes'
    departures = 'http://fahrplan.sbb.ch/bin/stboard.exe/en?input=8505300&REQTrain_name=&boardType'\
                 '=dep&time=now&productsFilter=2:111101001&selectDate=today&maxJourneys=40&start=yes'
    choise, str_choise = arrives_departures(arrives, departures)
    now, time_to_check = time()
    request_train(choise)
    train_in_order, dictionary = searchinformation()
    new_dictionary = check_hour(dictionary)
    intput(now, train_in_order, new_dictionary, str_choise, arrives, departures, choise)
    return


main()


