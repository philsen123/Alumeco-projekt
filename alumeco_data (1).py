import sqlite3
import random
import math

class AlumecoData():

    def __init__(self):
        self.db = sqlite3.connect("alumecodata.db")

        #self.create_tables()
        #self.create_data()

    def get_random_vare_id(self):
        c = self.db.cursor()
        c.execute('''
            SELECT id FROM Varer ORDER BY RANDOM() LIMIT 1;
        ''')        
        return c.fetchone()[0]
    
    def get_random_kunde_id(self):
        c = self.db.cursor()
        c.execute('''
            SELECT id FROM Kunder ORDER BY RANDOM() LIMIT 1;
        ''')
        a = c.fetchone()[0]     
        return a
    #Vores kode starter her
    
    def get_lager_antal(self,vareid):
        c= self.db.cursor()
        c.execute('''
                SELECT antal FROM LagerLokationer WHERE vare_id = ?
        ''',[vareid])
        antal=c.fetchone()[0]
        return antal
    
    def set_lager_antal(self,vareid,antal):
        c=self.db.cursor()
        c.execute('''
                UPDATE LagerLokationer SET antal = ? WHERE vare_id = ?
        ''',[antal,vareid])

        self.db.commit()

    def get_ordre_status(self, ordre):
        c = self.db.cursor()
        c.execute("""
        SELECT status FROM Ordrer WHERE id = ?""", [ordre])
        status = c.fetchone()[0]
        return status

    def get_kunde_prioritet(self, kunde):
        c = self.db.cursor()
        c.execute("""
        SELECT prioritet FROM Kunder WHERE id = ?""", [kunde])
        prioritet = c.fetchone()[0]
        return prioritet
    
    def get_varelokationer(self):
        c = self.db.cursor()
        #I det tilfælde man skal bruge en anden type vare, så erstattes 4 tallet med en variable f.eks. varenummer eller lign. Dette er bare et eksempel. 
        c.execute('''
            SELECT x,y FROM LagerLokationer WHERE LagerLokationer.vare_id = 4;
        ''')
        lx_liste = []
        ly_liste = []
        for l in c:
            lx_liste.append(l[0])
            ly_liste.append(l[1])
        l_liste = [lx_liste,ly_liste]
        #Man kan selv bestemme hvordan de skal visualiseres
        #print(lx_liste),(ly_liste)
        #print(l_liste)
        return l_liste
    
    def get_lokations_indhold(self, x_lok, y_lok):
        c = self.db.cursor()
        c.execute('''
            SELECT vare_id, antal FROM LagerLokationer WHERE x = ? AND y = ?;
        ''', [x_lok, y_lok])
        res = c.fetchone()
        return res[1], res[0]
    
    def get_varer_til_ordre (self, ordre_id):
        c = self.db.cursor()
        c.execute('''
            SELECT vare_id,antal FROM OrdreVarer where id = ? ''',[ordre_id])
        #for vare in c:
         #   print(vare[0],vare[1])

    def get_kunde_ordrer_ID(self,i):
        c = self.db.cursor()

        c.execute('''SELECT id FROM Ordrer WHERE kunde_id = ?''',[i])

        #for i in c:
            #print(f"Kunden har Ordrer ID Nummer {i[0]}")  
    
    def get_vare_lokatiner(self,vare_id):
        c=self.db.cursor()
        c.execute('''
            SELECT x,y FROM LagerLokationer where id = ?''',[vare_id])
        lx_liste = []
        ly_liste = []
        for l in c:
            lx_liste.append(l[0])
            ly_liste.append(l[1])
        return lx_liste, ly_liste
                
    def get_vare_lokatiner_x(self,vare_id):
        c=self.db.cursor()
        c.execute('''
            SELECT x FROM LagerLokationer where id = ?''',[vare_id])
        x = c.fetchone()[0]
        return x

    def get_vare_lokatiner_y(self,vare_id):
        c=self.db.cursor()
        c.execute('''
            SELECT y FROM LagerLokationer where id = ?''',[vare_id])
        y = c.fetchone()[0]
        return y

    #Vores kode slutter her
    def create_data(self):
        c = self.db.cursor()

        ## Opret Varer
        varenavne = ['Alu', 'Jern', 'Messing', 'Kobber', 'Stål']
        varetyper = ['pind', 'stang', 'rør', 'skrue', 'kasse', 'beslag', 'dims', 'møtrik', 'bolt']
        varestørrelser = [' 1x1', ' 2x2', '3x3', '5x5', '10x10', '20x20', ' 50x50', ' 100x100', ' 200x200']   
        kategorier = ['A', 'B','C','D','E'] 
        for navn in varenavne:
            for type in varetyper:
                for størrelse in varestørrelser:
                    kategori = random.choice(kategorier)
                    varenavn = navn + type + størrelse
                    c.execute('''
                        INSERT INTO Varer (navn, pris, kategori) VALUES (?,?,?);
                    ''', [varenavn, random.random() * 1000, kategori])

        ## Opret lagerlokationer. Nogle lokationer efterlades tomme.
        for x in range(64):     # x rækker
            for y in range(10): # med y hylder på hver række
                if random.random() < 0.99:
                    vare_id = self.get_random_vare_id()
                else:
                    vare_id = None
                c.execute('''
                    INSERT INTO Lagerlokationer (x,y,vare_id,antal) VALUES (?,?,?,?);
                ''', [x,y,vare_id, random.randint(1,10)])

        ## Opret kunder
        kundenavne = ['Alu', 'Jern', 'Maskin', 'Messing', 'Kobber', 'Stål']
        kundetyper = ['Eksperten', 'Imperiet', 'Handelen', 'Butikken', 'Tilbud', 'Innovation', 'Giganten']
        
        for i in range(300):            
            navn = random.choice(kundenavne) + random.choice(kundetyper) + f' {random.randint(1,100)}'
            c.execute('''
                INSERT INTO Kunder (navn, prioritet) VALUES (?,?);
            ''', [navn, random.randint(1,3)])        

        ## Opret Ordrer
        for i in range(100):
            kunde_id = self.get_random_kunde_id()
            print(f"Opretter ordre til: {kunde_id}")
            c.execute('''
                INSERT INTO Ordrer (kunde_id, status) VALUES (?,0);
            ''', [kunde_id])

        ## Tilføj Varer til Ordrer
        c.execute('SELECT id FROM Ordrer;')
        c2 = self.db.cursor()
        for ordre in c:
            print(f"Tilføjer varer til ordre {ordre[0]}")
            for vare in range(random.randint(1,10)):
                antal = random.randint(1,10)
                vare_id = self.get_random_vare_id()
                c2.execute('''
                    INSERT INTO OrdreVarer (ordre_id, vare_id, antal) VALUES (?,?,?);
                ''', [ordre[0], vare_id, antal])



        self.db.commit()


    def create_tables(self):
        c = self.db.cursor()

        try:
            c.execute('''
                CREATE TABLE Ordrer (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
		            kunde_id INTEGER,
                    status INTEGER);
            ''')
        except:
            print("Tabellen findes allerede")

        try:
            c.execute('''
                CREATE TABLE OrdreVarer (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
		            ordre_id INTEGER,
                    vare_id INTEGER,
                    antal INTEGER);
            ''')
        except:
            print("Tabellen findes allerede")

        try:
            c.execute('''
                CREATE TABLE Varer (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    navn TEXT,
                    kategori TEXT,
		            pris FLOAT);
            ''')
        except:
            print("Tabellen findes allerede")

        try:
            c.execute('''
                CREATE TABLE Kunder (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
		            navn TEXT,
                    prioritet INTEGER);
            ''')
        except:
            print("Tabellen findes allerede")
        
        try:
            c.execute('''
                CREATE TABLE LagerLokationer (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
		            x INTEGER,
                    y INTEGER,
                    vare_id INTEGER,
                    antal INTEGER);
            ''')
        except:
            print("Tabellen findes allerede")

        self.db.commit()

#Til at teste om jeres funktion virker. Den her tester funktionen få lager antal også sætter et antal
if __name__ == "__main__":
    data = AlumecoData()
    antal= data.get_vare_lokatiner(40)
    print("Antal:" + str(antal))

inp= ""
print('')
print('Kommandoer: ')
print('  afstand - Viser afstanden mellem 2 varer')

while not inp.startswith('q'):     
    inp = input('> ')    
    if inp== "afstand":        
        n=input('Intast vare id 1:')        
        a=input('Intast vare id 2:')        
        data = AlumecoData()        
        x1= data.get_vare_lokatiner_x(n)        
        y1= data.get_vare_lokatiner_y(n)        
        y2= data.get_vare_lokatiner_y(a)        
        x2= data.get_vare_lokatiner_x(a)  

        ChebyshevAfstand1=abs(x1-x2)        
        ChebyshevAfstand2=abs(y1-y2)        
        mantahanafstand=(abs(x1-x2)+abs(y1-y2))        
        euafstand=math.sqrt((x2-x1)**2+(y2-y1)**2)         
        print("Punkt 1:" + str(x1),";",str(y1))        
        print("Punkt 2:" + str(x2),";",str(y2))        
        if ChebyshevAfstand1 >= ChebyshevAfstand2:             
            print("Chebyshev Afstand:"+str(ChebyshevAfstand1))         
        elif ChebyshevAfstand2 > ChebyshevAfstand1:             
            print("Chebyshev Afstand:"+str(ChebyshevAfstand2))        
        print("Manhattan Afstand:"+str(mantahanafstand))        
        print("Euklædisk Afstand:"+str(euafstand))        
        print('')        
        print('Kommandoer: ')
        print(' afstand - viser afstanden mellem to varer')
