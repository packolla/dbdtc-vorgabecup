import re
import requests
import tkinter as tk
from tkinter import filedialog as fd
import csv
from tkinter import ttk
import threading

def readTeam(teamId2, teamId1, session, writer):
    pload = {'ajax': '1', 'skills_taktiken': 'skills_dropdown', 'value': 'beste', 'teamID': teamId1,
             'vergleichID2': teamId2}

    r = session.post('https://www.du-bist-der-teamchef.at/?q=team/teamvergleich_wechseln', data=pload)

    skills_t1 = re.findall("skills_team1\.push.*, (\d)", r.text)
    skills_t2 = re.findall("skills_team2\.push.*, (\d)", r.text)
    labels = re.findall("label: '(.*)'", r.text)

    pload = {'ajax': '1', 'skills_taktiken': 'taktiken_dropdown', 'value': 'beste', 'teamID': teamId1,
             'vergleichID2': teamId2}

    r = session.post('https://www.du-bist-der-teamchef.at/?q=team/teamvergleich_wechseln', data=pload)
    taktiken_t1 = re.findall("taktiken_team1\.push.*, (\d)", r.text)
    taktiken_t2 = re.findall("taktiken_team2\.push.*, (\d)", r.text)

    team1 = []
    team1.append(labels[0])
    team1.append(teamId1)
    team1.extend(taktiken_t1)
    team1.extend(skills_t1)

    team2 = []
    team2.append(labels[1])
    team2.append(teamId2)
    team2.extend(taktiken_t2)
    team2.extend(skills_t2)

    writer.writerow(team1)
    writer.writerow(team2)

    print(labels[0],',', teamId1,end='')
    for taktik in taktiken_t1:
        print(',',taktik,end='')

    for skill in skills_t1:
        print(',', skill,end='')

    print()
    print(labels[1], ',', teamId2, end='')
    for taktik in taktiken_t2:
        print(',', taktik, end='')

    for skill in skills_t2:
        print(',', skill, end='')

    print()

def validateLogin_int():
    pb.set('try to log in')
    s = requests.Session()
    pload = {'username': username.get(), 'password': password.get()}
    r = s.post('https://www.du-bist-der-teamchef.at/?q=team_login_aktion', data=pload)

    name = re.findall("Hallo, (.+)\&nbsp\;", r.text)
    if(len(name)==0):
        pb.set('login failed!')
        return
    pb.set('logged in as: '+ name[0])

    filetypes = (('csv files', '*.csv'), ('All files', '*.*'))
    filename = fd.askopenfilename(
        title='Select a input file',
        filetypes=filetypes)

    out_filename = filename.replace(".csv", "_out.csv")
    with open(out_filename, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Teamname','ID','Abwehrriegel','Vorsichtiger Spielaufbau','Manndeckung','Kontrollierte Offensive','Direktspiel','Kurzpassspiel','Hoch in den Strafraum','Brechstange','Offensives Fluegelspiel','Fitness','Erfahrung','Kondition','Tackling','Deckung','Passen','Spielaufbau','Torinstinkt','Schusskraft','Strafraumbeherrschung','Ballabwehr'])
        with open(filename) as csvfile:
            spamreader = csv.DictReader(csvfile, delimiter=',')
            team1 = next(spamreader, None)
            team2 = next(spamreader, None)
            while team1 != None:
                if team2 == None:
                    team2 = team1
                pb.set('read Team: ' + team1['Teamname']+ ' and Team : '+team2['Teamname'])
                readTeam(team1['ID'], team2['ID'], s, writer)
                team1 = next(spamreader, None)
                team2 = next(spamreader, None)
    pb.set('exported to: '+out_filename)
    print(out_filename)
    return

def validateLogin():
    x = threading.Thread(target=validateLogin_int)
    x.start()
def ui():
    # window
    global tkWindow
    tkWindow = tk.Tk()
    tkWindow.geometry('400x150')
    tkWindow.title('Dbdtc-Vorgabecup Exporter')

    # username label and text entry box
    usernameLabel = tk.Label(tkWindow, text="User Name").grid(row=0, column=0)
    global username
    username = tk.StringVar()
    usernameEntry = tk.Entry(tkWindow, textvariable=username).grid(row=0, column=1)

    # password label and password entry box
    passwordLabel = tk.Label(tkWindow, text="Password").grid(row=1, column=0)
    global password
    password = tk.StringVar()
    passwordEntry = tk.Entry(tkWindow, textvariable=password, show='*').grid(row=1, column=1)

    # login button
    loginButton = tk.Button(tkWindow, text="Start Export", command=validateLogin).grid(row=4, column=0)

    global pb
    pb = tk.StringVar()
    tk.Label(tkWindow, textvariable=pb,fg="gray").grid(row=5, column=0, columnspan=3)

    tkWindow.mainloop()
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    ui()

    # print(r.text)
    #readTeam('43465', '51463', s)



