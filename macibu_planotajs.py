import tkinter as tk
from tkinter import messagebox

kopejais_laiks = 0
darba_laiks = 0
atlikusais_laiks = 0
atputas_laiks = 0

# saraksta attēlošana
atputa = True

saraksts = []

pievieno = False

# Dzēš ievades tekstu, kad uz tā uzspiež
def tira_ievadi(event):
    event.widget.delete(0, tk.END)

# Ievadīto laiku limitē līdz 59
def limite_laiku():
    global kopejais_laiks, pievieno

    def clamp(entry):
        try:
            value = int(entry.get())
            return min(value, 59)
        except ValueError:
            return 0

    hours   = clamp(h_ievade)
    minutes = clamp(min_ievade)
    seconds = clamp(sec_ievade)

    kopejais_laiks = hours * 3600 + minutes * 60 + seconds

    if kopejais_laiks < 600: # vismaz 10 min
        messagebox.showinfo(' ', '  Kopējam laikam jābūt vismaz 10 min!')
        return

    # Paslēpj ievades skatu, parāda galveno, un parāda pogu
    sakuma_skats.place_forget()
    galvenais_skats.place(relx=0, rely=0, relwidth=1, relheight=1)
    parstat_poga.place(relx=0.6, rely=0.68, anchor="center")

    pievieno = True
    pievieno_laiku()

def atpakal():
    global darba_laiks, pievieno, kopejais_laiks
    kopejais_laiks = 0
    darba_laiks = 0
    pievieno = False

    galvenais_skats.place_forget()
    sakuma_skats.place(relx=0, rely=0, relwidth=1, relheight=1)

def izveido_sarakstu():
    global darba_laiks, atputas_laiks, kopejais_laiks, saraksts

    darba_laiks -= 1 # pievieno_laiku() dod 1 par daudz

    if darba_laiks > 0:
        if kopejais_laiks / darba_laiks > 20:
            messagebox.showinfo(' ', '  Darba laiks pārāk mazs!')
            return

    atlikusais = kopejais_laiks
    atputas_laiks = darba_laiks // 5

    # kamēr atlikušais ir 
    while atlikusais > 0:
        atlikusais-= darba_laiks          # atņem darba laiku

        if atlikusais > atputas_laiks:    # un ja atlikušajā ir vairāk nekā atpūtas laiks
            saraksts.append(atputas_laiks)
            saraksts.append(darba_laiks)
            atlikusais -= (atputas_laiks) # tad atņem atpūtas laiku
        else:               
            #saraksts.append(darba_laiks + int(atlikusais))
            atlikusais = 0

    atpakal_poga.pack_forget() # Noņem atpakaļ pogu
    parstat_poga.place_forget() # Noņem pārstāt pogu
    attelo_sarakstu()

# Skaita uz priekšu darba laiku
def pievieno_laiku():
    global darba_laiks, pievieno

    if not pievieno: return

    hours, remainder = divmod(darba_laiks, 3600)
    mins, secs = divmod(remainder, 60)
    laiks.config(text=f"{hours:02d}:{mins:02d}:{secs:02d}", fg = "white")

    darba_laiks += 1
    logs.after(1000, pievieno_laiku)

# Skaita uz atpakaļ atlikušo intervāla laiku
def atnem_laiku():
    global atlikusais_laiks, saraksts, atputa

    if atlikusais_laiks >= 0:
        hours, remainder = divmod(atlikusais_laiks, 3600)
        mins, secs = divmod(remainder, 60)
        laiks.config(text=f"{hours:02d}:{mins:02d}:{secs:02d}", fg = "white")

        atlikusais_laiks -= 1
        logs.after(1000, atnem_laiku)
    else:
        del saraksts[0] #izdzēš pirmo, to kas tikko beidzās

        atputa = not atputa

        partaisa_sarakstu()

# Vizuāli attēlo sarakstu 
def attelo_sarakstu():
    global pievieno, atlikusais_laiks, atputa, saraksts
    pievieno = False
    first = True
    y = 0

    box_frame.place(relx=0, rely=0, relwidth=0.3, relheight=1)

    # Attēlo sarakstu
    for x in saraksts:

        if atputa:
            color = "#4B0F1C"
            text = formate_laiku(atputas_laiks)
        else:
            color = "#0F2D4B"
            text = formate_laiku(darba_laiks)

        if first: # Pirmā
            box = tk.Frame(box_frame, bg=color, width=110, height=30, highlightbackground="white", highlightthickness=1)
            box.place(relx=0.2,rely=0.18 + y, anchor="w")

            uzraksts.configure(text="Atpūta") # Maina nosaukumu
            box_frame.configure(bg="#160404") # Fona krāsu
            galvenais_skats.configure(bg="#160404")
            laiks.configure(bg="#160404")
            uzraksts.configure(bg="#160404")
            virs_teksts.configure(bg="#160404")

            first = False
        else: # Pārējās
            box = tk.Frame(box_frame, bg=color, width=110, height=30)
            box.place(relx=0.2,rely=0.18 + y, anchor="w")
            box.pack_propagate(False) # Lai teksts nemaina izmēru
            box_teksts = tk.Label(box, text=text, bg = color, fg="white")
            box_teksts.pack(expand=True)
        
        #if len(saraksts) % 1 == 0: # Ja sarakstā intervālu skaits nav pāra skaitlis
        atputa = not atputa
        y += 0.1

    # aizsūta šī brīža intervāla laiku uz skaitītāju
    atlikusais_laiks = int(saraksts[0])
    atnem_laiku()

def partaisa_sarakstu():
    global pievieno, atlikusais_laiks, atputas_laiks, darba_laiks, saraksts, atputa
    first = True
    y = 0

    a = atputa

    # Izdzēš visu no box_frame
    for widget in box_frame.winfo_children():
        widget.destroy()

    # Attēlo sarakstu
    for whatever in saraksts:

        if a:
            color = "#4B0F1C"
            text = formate_laiku(atputas_laiks)
        else:
            color = "#0F2D4B"
            text = formate_laiku(darba_laiks)

        if first: # Pirmā
            box = tk.Frame(box_frame, bg=color, width=110, height=30, highlightbackground="white", highlightthickness=1)
            box.place(relx=0.2,rely=0.18 + y, anchor="w")

            # Maina uzrakstu balstoties uz pirmā
            if atputa:
                uzraksts.configure(text="Atpūta")
                box_frame.configure(bg="#160404")
                galvenais_skats.configure(bg="#160404")
                laiks.configure(bg="#160404")
                uzraksts.configure(bg="#160404")
                virs_teksts.configure(bg="#160404")
            else:
                uzraksts.configure(text="Darbs")
                box_frame.configure(bg="#040D16")
                galvenais_skats.configure(bg="#040D16")
                laiks.configure(bg="#040D16")
                uzraksts.configure(bg="#040D16")
                virs_teksts.configure(bg="#040D16")
            first = False
        else: # Visas pārējās
            box = tk.Frame(box_frame, bg=color, width=110, height=30)
            box.place(relx=0.2,rely=0.18 + y, anchor="w")
            box.pack_propagate(False) # Lai teksts nemaina izmēru
            box_teksts = tk.Label(box, text=text, bg = color, fg="white")
            box_teksts.pack(expand=True)
        
        a = not a
        y += 0.1

    # Aizsūta šī brīža intervāla laiku uz skaitītāju
    if len(saraksts) <= 0:
        box_frame.configure(bg="#000000")
        galvenais_skats.configure(bg="#000000")
        laiks.configure(bg="#000000", text=" ")
        uzraksts.configure(bg="#000000", text="Darbs pabeigts!")
        virs_teksts.configure(bg="#000000", text=" ")
        return
    else:
        atlikusais_laiks = int(saraksts[0])
        atnem_laiku()
    
# Sekundes formatē minūtēs un stundās
def formate_laiku(seconds):
    seconds = int(seconds) # Drošībai
    hours, remainder = divmod(seconds, 3600)
    mins, secs = divmod(remainder, 60)
    return f"{hours:02d}:{mins:02d}:{secs:02d}"
        
#________________________________________________________________________________________________________________________________________

# ------------------------------ Window ------------------------------
logs = tk.Tk()
logs.title("Laika dalītājs")
logs.geometry("500x400")
logs.attributes("-topmost", True)
logs.resizable(False, False)

# ------------------------------ Ievades skats ------------------------------

sakuma_skats = tk.Frame(logs, bg="#1c1c1c")
sakuma_skats.place(relx=0, rely=0, relwidth=1, relheight=1)

# Mērvienība virs ievades
tk.Label(sakuma_skats, text="   stundas            minūtes           sekundes", 
bg="#1c1c1c", fg="#949494", font=("Arial", 10)).place(relx=0.5, rely=0.35, anchor="center")

timeFrame = tk.Frame(sakuma_skats, bg="#1c1c1c")
timeFrame.place(relx=0.5, rely=0.45, anchor="center")

# Stundas
h_ievade = tk.Entry(timeFrame, bg="#1c1c1c", fg = "white", font=("Arial", 26), width=3, justify="center", bd=0)
h_ievade.insert(0, "00")
h_ievade.bind("<FocusIn>", tira_ievadi)
# Minūtes
min_ievade = tk.Entry(timeFrame, bg="#1c1c1c", fg = "white", font=("Arial", 26), width=3, justify="center", bd=0)
min_ievade.insert(0, "00")
min_ievade.bind("<FocusIn>", tira_ievadi)
# Sekundes
sec_ievade = tk.Entry(timeFrame, bg="#1c1c1c", fg = "white", font=("Arial", 26), width=3, justify="center", bd=0)
sec_ievade.insert(0, "00")
sec_ievade.bind("<FocusIn>", tira_ievadi)

h_ievade.pack(side="left")
tk.Label(timeFrame, text=" : ", bg="#1c1c1c", fg = "white", font=("Arial", 24)).pack(side="left")
min_ievade.pack(side="left")
tk.Label(timeFrame, text=" : ", bg="#1c1c1c", fg = "white", font=("Arial", 24)).pack(side="left")
sec_ievade.pack(side="left")

# Set time button
sakt_poga = tk.Button(sakuma_skats, text="Sākt", width=7, font=("Arial", 18), bg="#1c1c1c", fg = "white", command=limite_laiku)
sakt_poga.place(relx=0.5, rely=0.65, anchor="center")

# ------------------------------ Galvenais skats ------------------------------

galvenais_skats = tk.Frame(logs, bg="#040D16")

# Uzraksts
uzraksts = tk.Label(galvenais_skats, text="Darbs", font=("Arial", 30),fg="white",bg="#040D16")
uzraksts.place(relx=0.6, rely=0.1, anchor="center")

# Teksts virs laika
virs_teksts = tk.Label(galvenais_skats, text="Intervala laiks:", font=("Arial", 12),fg="#adadad",bg="#040D16")
virs_teksts.place(relx=0.6, rely=0.4, anchor="center")

# Laika teksts
laiks = tk.Label(galvenais_skats, text="00:00:00", font=("Arial", 35),fg="white",bg="#040D16")
laiks.place(relx=0.6, rely=0.5, anchor="center")

# Pārstāt darbu
parstat_poga = tk.Button(galvenais_skats, text="Pārstāt darbu", width=10, font=("Arial", 10), bg="#040D16", fg = "white", command=izveido_sarakstu)

# Intervālu rāmis
box_frame = tk.Frame(galvenais_skats, bg="#040D16")

# Atpakaļ
atpakal_poga = tk.Button(galvenais_skats, text="<", width=3, font=("Arial", 14), bg="#000000", fg = "white", command=atpakal)
atpakal_poga.pack(anchor="w")

logs.mainloop()