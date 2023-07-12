from PyQt5.QtWidgets import*
from PyQt5.QtCore import*
from PyQt5.QtGui import QPixmap
from threading import Thread
from queue import Queue
import cv2
import time
import math
import random


"""
total demands and total assets must be equal

toplam talepler ve toplam varlıklar birbirlerine eşit olmalıdır
Haritadan hangi şehrin ne kdar ihtiyacı oldugu ayarlanmalıdır


"""
class node():
    def __init__(self,name,location,color_text,color_circle,radius_small,radius_big,demand,assets=0,distance=math.inf):
        self.color_text = color_text          
        self.color_circle = color_circle
        self.radius_small = radius_small
        self.radius_big = radius_big 
        self.name = name
        self.distance = distance
        self.assets = assets
        self.demand = demand 
        self.location = location  
        self.distances = None #distances from this node to other nodes  # Diğer düğümlere olan mesafeler
        self.distances_to_senders = None #the nodes has that able to use assets for that node #Bu düğüm için varlıklarını kullanabilen düğümler
        self.received = {}

class edge():
    def __init__(self,weight,color_line,color_text,tail_node,head_node,):
        self.head_location = head_node.location
        self.teil_location = tail_node.location
        self.center_location = (int((head_node.location[0]-tail_node.location[0])/2 + tail_node.location[0]),int((head_node.location[1]-tail_node.location[1])/2 + tail_node.location[1]))
        self.color_line = color_line
        self.color_text = color_text
        self.head_node = head_node
        self.tail_node = tail_node
        self.name = f"{head_node.name}-{tail_node.name}"   
        self.weight = weight
        
class text():
    def __init__(self,text,location,color_text):
        self.text = text
        self.location = location
        self.color_text = color_text
    
    S
    
    
class Gui(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.save_sayac = 1000 # for gif images
        self.define_colors()
        self.nodes = self.define_nodes()
        self.edges = self.define_edges()
        self.texts = self.define_texts()
        self.create_screen()
        self.draw_screen()
        self.change_items_property()
        self.draw_screen()
        self.thread_distribution()
        


        
    def define_colors(self):
        self.COLOR_BLACK = (60,60,60)
        self.COLOR_ORANGE = (0,170,255)
        self.COLOR_RED = (60,10,255)
        self.COLOR_GREEN = (65,255,140)
        self.COLOR_PURPLE = (170,0,190)
        self.COLOR_GRAY = (100,100,100)

    def define_nodes(self):
        nodes = {}
        nodes["N1"] = node("N1",(600,375),self.COLOR_ORANGE,self.COLOR_BLACK,10,14,0)
        nodes["N2"] = node("N2",(750,300),self.COLOR_ORANGE,self.COLOR_BLACK,10,14,0)
        nodes["N3"] = node("N3",(750,425),self.COLOR_ORANGE,self.COLOR_BLACK,10,14,0)
        nodes["N4"] = node("N4",(750,700),self.COLOR_ORANGE,self.COLOR_BLACK,10,14,0)
        nodes["N5"] = node("N5",(775,550),self.COLOR_ORANGE,self.COLOR_BLACK,10,14,0)
        nodes["N6"] = node("N6",(1000,575),self.COLOR_ORANGE,self.COLOR_BLACK,10,14,0)
        nodes["N7"] = node("N7",(950,375),self.COLOR_ORANGE,self.COLOR_BLACK,10,14,0)
        nodes["N8"] = node("N8",(1100,450),self.COLOR_ORANGE,self.COLOR_BLACK,10,14,0)
        nodes["N9"] = node("N9",(1150,325),self.COLOR_ORANGE,self.COLOR_BLACK,10,14,0)
        nodes["N10"] = node("N10",(400,350),self.COLOR_ORANGE,self.COLOR_BLACK,10,14,0)
        nodes["N11"] = node("N11",(300,250),self.COLOR_ORANGE,self.COLOR_BLACK,10,14,0)
        nodes["N12"] = node("N12",(350,600),self.COLOR_ORANGE,self.COLOR_BLACK,10,14,0)
        nodes["N13"] = node("N13",(275,150),self.COLOR_ORANGE,self.COLOR_BLACK,10,14,0)
        nodes["N14"] = node("N14",(1100,200),self.COLOR_ORANGE,self.COLOR_BLACK,10,14,0)
        nodes["N15"] = node("N15",(1250,500),self.COLOR_ORANGE,self.COLOR_BLACK,10,14,0)
        nodes["N16"] = node("N16",(200,350),self.COLOR_ORANGE,self.COLOR_BLACK,10,14,0)
        nodes["N17"] = node("N17",(150,550),self.COLOR_ORANGE,self.COLOR_BLACK,10,14,0)
        nodes["N18"] = node("N18",(550,100),self.COLOR_ORANGE,self.COLOR_BLACK,10,14,0)
        nodes["N20"] = node("N20",(550,625),self.COLOR_ORANGE,self.COLOR_BLACK,10,14,0)
                 
        return nodes

    def define_edges(self):
        edges = {}
        edges["N1-N2"] = edge(200, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N1"], self.nodes["N2"])
        edges["N1-N3"] = edge(300, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N1"], self.nodes["N3"])
        edges["N1-N5"] = edge(400, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N1"], self.nodes["N5"])
        edges["N5-N4"] = edge(300, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N5"], self.nodes["N4"])
        edges["N2-N3"] = edge(200, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N2"], self.nodes["N3"])
        edges["N3-N5"] = edge(300, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N3"], self.nodes["N5"])
        edges["N2-N7"] = edge(400, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N2"], self.nodes["N7"])
        edges["N5-N6"] = edge(500, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N5"], self.nodes["N6"])
        edges["N7-N6"] = edge(400, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N7"], self.nodes["N6"])
        edges["N6-N8"] = edge(300, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N6"], self.nodes["N8"])
        edges["N8-N9"] = edge(300, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N8"], self.nodes["N9"])
        edges["N13-N11"] = edge(100, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N13"], self.nodes["N11"])
        edges["N11-N10"] = edge(100, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N11"], self.nodes["N10"])
        edges["N10-N12"] = edge(700, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N10"], self.nodes["N12"])
        edges["N11-N12"] = edge(800, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N11"], self.nodes["N12"])
        edges["N12-N1"] = edge(300, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N12"], self.nodes["N1"])
        edges["N10-N1"] = edge(500, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N10"], self.nodes["N1"])
        edges["N10-N2"] = edge(600, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N10"], self.nodes["N2"])

        edges["N14-N2"] = edge(600, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N14"], self.nodes["N2"])
        edges["N14-N7"] = edge(550, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N14"], self.nodes["N7"])
        edges["N14-N9"] = edge(150, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N14"], self.nodes["N9"])  
        edges["N15-N8"] = edge(400, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N15"], self.nodes["N8"])
        edges["N15-N9"] = edge(400, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N15"], self.nodes["N9"])      
        edges["N6-N4"] = edge(700, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N6"], self.nodes["N4"])      
        
        edges["N11-N16"] = edge(300, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N11"], self.nodes["N16"])    
        edges["N16-N17"] = edge(450, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N16"], self.nodes["N17"])      
        edges["N18-N13"] = edge(400, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N18"], self.nodes["N13"])      
        edges["N18-N10"] = edge(450, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N18"], self.nodes["N10"])     
        edges["N18-N2"] = edge(550, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N18"], self.nodes["N2"])
        edges["N20-N12"] = edge(150, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N20"], self.nodes["N12"])      
        edges["N20-N5"] = edge(200, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N20"], self.nodes["N5"])   
        edges["N12-N17"] = edge(150, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N12"], self.nodes["N17"])    
        
        ## THERE EDGES ARE REVERSE OF ABOVE EDGES   ##YUKARDAKİ KENARLARIN TERS YOLLU HALLERİ
        edges["N2-N1"] = edge(200, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N2"], self.nodes["N1"])
        edges["N3-N1"] = edge(300, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N3"], self.nodes["N1"])
        edges["N5-N1"] = edge(400, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N5"], self.nodes["N1"])
        edges["N4-N5"] = edge(300, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N4"], self.nodes["N5"])
        edges["N3-N2"] = edge(200, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N3"], self.nodes["N2"])
        edges["N5-N3"] = edge(300, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N5"], self.nodes["N3"])
        edges["N7-N2"] = edge(400, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N7"], self.nodes["N2"])
        edges["N6-N5"] = edge(500, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N6"], self.nodes["N5"])
        edges["N6-N7"] = edge(400, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N6"], self.nodes["N7"])
        edges["N8-N6"] = edge(300, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N8"], self.nodes["N6"])
        edges["N9-N8"] = edge(300, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N9"], self.nodes["N8"])
        edges["N11-N13"] = edge(100, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N11"], self.nodes["N13"])
        edges["N10-N11"] = edge(100, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N10"], self.nodes["N11"])
        edges["N12-N10"] = edge(700, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N12"], self.nodes["N10"])
        edges["N12-N11"] = edge(800, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N12"], self.nodes["N11"])
        edges["N1-N12"] = edge(300, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N1"], self.nodes["N12"])
        edges["N1-N10"] = edge(500, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N1"], self.nodes["N10"])
        edges["N2-N10"] = edge(600, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N2"], self.nodes["N10"])
        
        edges["N2-N14"] = edge(600, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N2"], self.nodes["N14"])
        edges["N7-N14"] = edge(550, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N7"], self.nodes["N14"])
        edges["N9-N14"] = edge(150, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N9"], self.nodes["N14"])       
        edges["N8-N15"] = edge(400, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N8"], self.nodes["N15"])
        edges["N9-N15"] = edge(400, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N9"], self.nodes["N15"])
        edges["N4-N6"] = edge(700, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N4"], self.nodes["N6"])  
        
        edges["N16-N11"] = edge(300, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N16"], self.nodes["N11"])      
        edges["N17-N16"] = edge(450, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N17"], self.nodes["N16"])  
        edges["N13-N18"] = edge(400, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N13"], self.nodes["N18"])
        edges["N10-N18"] = edge(450, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N10"], self.nodes["N18"])      
        edges["N2-N18"] = edge(550, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N2"], self.nodes["N18"])
        edges["N12-N20"] = edge(150, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N12"], self.nodes["N20"])      
        edges["N5-N20"] = edge(200, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N5"], self.nodes["N20"])      
        edges["N17-N12"] = edge(150, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N17"], self.nodes["N12"])      
        return edges
        
    def define_texts(self):
        texts = []
        
        self.text1 = text("",(10,750), self.COLOR_ORANGE)
        self.text2 = text("",(10,780), self.COLOR_ORANGE)
        self.text3 = text("",(10,720), self.COLOR_ORANGE)
        texts.append(self.text1)
        texts.append(self.text2)
        texts.append(self.text3)
        
        return texts
        
    def create_screen(self):
        self.pixmap = QPixmap("harita.jpg")
        self.screen = QLabel()
        self.screen.setPixmap(self.pixmap)
        
        layout = QGridLayout()
        layout.addWidget(self.screen)
        self.setLayout(layout)
        self.setWindowTitle("Map")
        self.resize(1400,800)
        
    def draw_screen(self):
        time.sleep(0.001)
        image = cv2.imread("harita.jpg") 
        image = self.draw_edges(image)
        image = self.draw_nodes(image)
        image = self.draw_texts(image)

        cv2.imwrite("guncel_harita.jpg",image)
        
        self.pixmap = QPixmap("guncel_harita.jpg")
        self.screen.setPixmap(self.pixmap)
        
        ##FOR GİF, GİF ÜRETMEK İÇİN
        ##cv2.imwrite(f"./images/gif_im_{self.save_sayac}.jpg",image)   # gidişatı görsel olarak kaydetmek için
        self.save_sayac += 1
        
    def draw_nodes(self,image):
        
        for node in self.nodes.values():
            cv2.circle(image, node.location ,node.radius_small, node.color_circle,-1)
            cv2.circle(image, node.location ,node.radius_big, node.color_circle,1)
            cv2.putText(image,node.name, (node.location[0]-5,node.location[1]-5) ,cv2.FONT_HERSHEY_SIMPLEX,0.7,node.color_text,2,cv2.LINE_AA) 
            cv2.putText(image,f"{node.assets}:{node.demand}:{node.distance}", (node.location[0]-10,node.location[1]+20) ,cv2.FONT_HERSHEY_SIMPLEX,0.8,node.color_text,2,cv2.LINE_AA) 
                        
        return image
    
    def draw_edges(self,image):
        for edge in self.edges.values():
            cv2.line(image, edge.teil_location , edge.head_location , edge.color_line , 2) 
            cv2.putText(image,str(edge.weight), (edge.center_location[0],edge.center_location[1]-10) ,cv2.FONT_HERSHEY_SIMPLEX,0.4,edge.color_text,1,cv2.LINE_AA) 
        
        return image
    
    def draw_texts(self,image):
        for text in self.texts:
            cv2.putText(image,text.text,text.location ,cv2.FONT_HERSHEY_SIMPLEX,0.8,text.color_text,2,cv2.LINE_AA) 
         
        return image

    
    def change_items_property(self):

        self.change_node_property("N6", 10,0)
        self.change_node_property("N7", 15,0)
        self.change_node_property("N8", 10,0)
        self.change_node_property("N9", 15,0)
        self.change_node_property("N15", 10,0)
        self.change_node_property("N4", 15,0)
        self.change_node_property("N5", 10,0)


        self.change_node_property("N1", 0, 10)
        self.change_node_property("N10", 0, 15)
        self.change_node_property("N12", 0, 10)
        self.change_node_property("N11", 0, 15)
        self.change_node_property("N20", 0, 10)
        self.change_node_property("N17", 0, 15)
        self.change_node_property("N16", 0, 10)

        
        self.change_edge_property("N6-N7",800)
        self.change_edge_property("N7-N6",800)
        
        self.change_edge_property("N5-N6",1000)
        self.change_edge_property("N6-N5",1000)
        
        self.change_edge_property("N6-N8",500)
        self.change_edge_property("N8-N6",500)
        
        self.change_edge_property("N9-N8",500)
        self.change_edge_property("N8-N9",500)
                
        self.change_edge_property("N15-N8",1100)
        self.change_edge_property("N8-N15",1100)
                
        self.change_edge_property("N15-N9",900)
        self.change_edge_property("N9-N15",900)
        
        self.change_edge_property("N4-N6",1500)
        self.change_edge_property("N6-N4",1500)
        
        self.change_edge_property("N4-N5",400)
        self.change_edge_property("N5-N4",400)
        
        
        
        
    def change_node_property(self,name,demand,assets):
        self.nodes[name].demand = demand
        self.nodes[name].assets = assets     
        if   assets > 0 :
            self.nodes[name].color_text = self.COLOR_PURPLE        
        elif demand > 0 :
            self.nodes[name].color_text = self.COLOR_RED
        else:
            self.nodes[name].color_text = self.COLOR_GREEN


        
    def change_edge_property(self,name,weight):
        self.edges[name].weight = weight
        self.edges[name].color_text = self.COLOR_RED    
        
    def thread_distribution(self):
        t = Thread(target=self.distribution)
        t.start()
        
    def distribution(self):
        self.receiver_nodes = {}
        self.sender_nodes = {}
        
        ##We add the nodes that own the entities to the sender_nodes dictionary #Varlıklara sahip olan düğümleri sender_nodes sözlüğüne ekliyoruz
        ##We add the nodes that have the requests to the sender_nodes dictionary #Taleplere sahip olan düğümleri receiver_nodes sözlüğüne ekliyoruz
        for node in self.nodes.keys():
            if self.nodes[node].assets > 0:
                self.sender_nodes[node] = self.nodes[node]
            if self.nodes[node].demand > 0:
               self.receiver_nodes[node] = self.nodes[node]
                
                
        ##GÖRSELLİK
        self.text1.text = "alicilar : " +str(self.receiver_nodes.keys())
        self.text2.text = "gonderenler : " + str(self.sender_nodes.keys())
        self.text3.text = ""
        self.draw_screen()

        ##
        
        ##if any item exist both of dictionaries,we use assets for demands  #Eğer bir düğüm hem alıcı hem de göndericiyse bunları nötreyerek azaltırız
        for node_key in self.receiver_nodes.keys():
            if node_key in self.sender_nodes.keys():
                node = self.sender_nodes[node_key]
                if node.assets >= node.demand:
                    for i in range(node.demand):
                        node.assets -= 1
                        node.demand -= 1
                        self.change_node_property(node.name,node.demand,node.assets)
                        time.sleep(1)
                        self.draw_screen()
                    self.receiver_nodes.pop(node.name)
                    
                elif node.assets < node.demand:
                    for i in range(node.assets):
                        
                        node.demand -= 1 
                        node.assets -= 1
                        self.change_node_property(node.name,node.demand,node.assets)
                        time.sleep(1)
                        self.draw_screen()
                    self.sender_nodes.pop(node.name)
        
        ##GÖRSELLİK
        self.text1.text = "alicilar : " +str(self.receiver_nodes.keys())
        self.text2.text = "gonderenler : " + str(self.sender_nodes.keys())
        self.draw_screen()
        ##GÖRSELLİK
        
        ##For every receiver node run the search function
        for node in self.receiver_nodes.values():  
            self.search(node)
        self.draw_screen()
        
        
        ##We find the total demands of nodes  # Toplam talepleri buluyoruz
        total_demand = 0
        total_asset = 0
        for node in self.receiver_nodes.values():
            total_demand += node.demand
        for node in self.sender_nodes.values():
            total_asset += node.assets
  
        print("Toplam talepler : ",total_demand)
        print("Toplam varlıklar : ",total_asset)
        
        for i in range(total_demand):
            self.transport_asset()
            

        self.text1.text = "alicilar : " +str(self.receiver_nodes.keys())
        self.text2.text = "gonderenler : " + str(self.sender_nodes.keys())  
        self.draw_screen()
        self.show_results()

        
        
        
        
    #searching distances from given node to other nodes and add results to this node attributes #Verilen node un diğer node lara olan mesafesini ölçüp özelliklerine ekliyoruz
    def search(self,target_node):
        distances = {} # {"node ismi" : (mesafe,hangi düğümden ulaşıldığı)} {"other nodes" : (distance,the node which coming from)}
        senders = {} # {"node_varlikli" : mesafe} {"node which sender" : distance}"
        

        self.text3.text = f"islem -> mesafe  : {target_node.name}"
        target_node.distance = 0
        
        Q =Queue()     
        Q.put(target_node)
        

        def recursive_travel(q):
            
            if q.qsize() != 0:              #when the queue is not empty search nodes  #sıra boş olana kadar aramaya devam et
                node = q.get()

                #Find the edges of this node and add the edges_of_node list and sort this list
                edges_of_node = []          
                for edge in self.edges.values():
                    if edge.tail_node.name == node.name:
                        edges_of_node.append(edge)
                
                edges_of_node.sort(key=lambda x : x.weight) 
                
                
                #find the distances of neighbor nodes with using this node's edges and add this values to senders and distances dictionaries 
                #nodun kenarlarını kullanarak bağlantılı olduğu node'ların mesafelerini güncelle ve senders,distances sözlüklerine ekle
                for edge in edges_of_node:
                    
                    ## Görsellik
                    edge.color_line = self.COLOR_GREEN
                    self.edges[f"{edge.head_node.name}-{edge.tail_node.name}"].color_line = self.COLOR_GREEN
                    edge.tail_node.color_circle = self.COLOR_GREEN
                    self.draw_screen()                  
                    edge.color_line = self.COLOR_GRAY
                    edge.tail_node.color_circle = self.COLOR_BLACK
                    self.edges[f"{edge.head_node.name}-{edge.tail_node.name}"].color_line = self.COLOR_GRAY
                    self.draw_screen()
                    ##
                    
                    
                    if edge.head_node.distance > edge.tail_node.distance + edge.weight:
                        
                        edge.head_node.distance = edge.tail_node.distance + edge.weight
                        distances[edge.head_node.name]  = (edge.head_node.distance,edge.tail_node.name)
                        q.put(edge.head_node)
                        if edge.head_node.assets > 0:
                            senders[edge.head_node] = edge.head_node.distance

                return recursive_travel(q)

            else:
                pass
        
        #Change distance value of all nodes to infinity # kayıt yapıldıktan sonra tüm nodeların distance(mesafe) değerlerini sonsuza ayarlıyoruz , diğer nodelar içinde mesafe hesabju yapacagımız için
        def reset_distances():
            for node in self.nodes.values():
                node.distance = math.inf
                
        recursive_travel(Q)
        reset_distances()

        target_node.distances = distances
        target_node.distances_to_senders = senders
   
    def show_results(self):
        image = cv2.imread("guncel_harita.jpg")
        x,y = 50,70
        sayac = 0
        
        S = cv2.getFontScaleFromHeight(cv2.FONT_HERSHEY_SIMPLEX,25,2) # returns factor for 25 px text
        
        for i in self.nodes.values():
            
            text = f"{i.name}  - received :  {i.received}"
            k =cv2.getTextSize(text,cv2.FONT_HERSHEY_SIMPLEX,S,2)
            cv2.rectangle(image,(x,y+sayac*35+10),(x+k[0][0],y+sayac*35-k[0][1]-5),(0,0,0),-1)
            cv2.putText(image,text,(x,y+sayac*35) ,cv2.FONT_HERSHEY_SIMPLEX,S,self.COLOR_GREEN,2,cv2.LINE_AA)
  
            sayac += 1  
            
            print("\n    ",text)
            print(f"{i.name}   - distances : {i.distances}")
        
            


        
        
        cv2.imwrite("guncel_harita.jpg",image)
        
        self.pixmap = QPixmap("guncel_harita.jpg")
        self.screen.setPixmap(self.pixmap)

        

        
    def transport_asset(self): 
        self.text1.text = "alicilar : " +str(self.receiver_nodes.keys())
        self.text2.text = "gonderenler : " + str(self.sender_nodes.keys())  

        # find the path from receiver node to sender_node
        def find_path(sender_node_name,receiver_node_name,distances,path= []):
            target_node_name = distances[sender_node_name][1]
            self.nodes[sender_node_name].color_circle = self.COLOR_GREEN
            self.nodes[receiver_node_name].color_circle = self.COLOR_GREEN
            self.edges[f"{sender_node_name}-{target_node_name}"].color_line = self.COLOR_GREEN
            self.edges[f"{target_node_name}-{sender_node_name}"].color_line = self.COLOR_GREEN
            self.draw_screen()
            time.sleep(0.011)
            self.nodes[sender_node_name].color_circle = self.COLOR_BLACK
            self.nodes[receiver_node_name].color_circle = self.COLOR_BLACK
            self.edges[f"{sender_node_name}-{target_node_name}"].color_line = self.COLOR_GRAY
            self.edges[f"{target_node_name}-{sender_node_name}"].color_line = self.COLOR_GRAY
           
            if target_node_name == receiver_node_name:
                return path
            else:
                path.append(target_node_name)
                return find_path(target_node_name,receiver_node_name,distances,path)





        sorted_receiver_nodes = sorted(self.receiver_nodes.items(),key=lambda x:x[1].demand,reverse=True) #[(NX,NODE),(NX,NODE),(NX,NODE)]
        receiver_node = sorted_receiver_nodes[0][1]
       
        sorted_senders = sorted(receiver_node.distances_to_senders.items(),key=lambda x: x[0].assets,reverse=True) # we are sorting because the node demands from most close node that has assets
        sender_node = sorted_senders[0][0]
        
        self.text3.text = f"islem - tasima : {sender_node.name}-> {receiver_node.name}"
        
        
        for i in range(len(sorted_senders)):
            print("Sıralanmış Gönderen düğümlerin varliklari :",sorted_senders[i][0].assets)
        for i in range(len(sorted_receiver_nodes)):
            print("Siralanmiş düğüm talepleri",sorted_receiver_nodes[i][1].demand)
            
        sender_node.assets -= 1

        if sender_node.assets == 0:
            self.sender_nodes.pop(sender_node.name)
            
            for node in self.receiver_nodes.values():
                node.distances_to_senders.pop(sender_node)
    
        path = find_path(sender_node.name, receiver_node.name, receiver_node.distances)
        print("yol: ",sender_node.name,path,receiver_node.name) 
        
        receiver_node.demand -= 1
        
        if sender_node.name in receiver_node.received.keys():
            receiver_node.received[sender_node.name] += 1
        else:
            receiver_node.received[sender_node.name] = 1
        
        if receiver_node.demand == 0:
            self.receiver_nodes.pop(receiver_node.name)
            self.change_node_property(receiver_node.name, 0, 0)
            
        print("Taşındı\n\n")       
 

        
    """ Bu fonksiyonun açıklaması , Explanation of this method
        receiver_nodestaki en ihtiyaçlı olan node al
        bu nodun senders özelliğindeki nodelara olan mesafesine göre sendersı sırala
        en az mesafedeki sender nodeu al
        sender nodedan receiver nodea olan yolu distances özelliğinden hesapla
        sender nodedan receiver nodea varlıkları gönder (görsel olarakta)
        receiver nodeun received attributena hangi varlıgın nerden geldiğini yaz
        
    """        
        
app = QApplication([])
widget = Gui()
widget.show()
app.exec_()
        









        
        
"""
### HARİTA 1 -MAP1
    def define_nodes(self):
        nodes = {}
        nodes["N1"] = node("N1",(600,350),self.COLOR_ORANGE,self.COLOR_BLACK,10,14,0)
        nodes["N2"] = node("N2",(750,300),self.COLOR_ORANGE,self.COLOR_BLACK,10,14,0)
        nodes["N3"] = node("N3",(750,425),self.COLOR_ORANGE,self.COLOR_BLACK,10,14,0)
        nodes["N4"] = node("N4",(750,700),self.COLOR_ORANGE,self.COLOR_BLACK,10,14,0)
        nodes["N5"] = node("N5",(775,550),self.COLOR_ORANGE,self.COLOR_BLACK,10,14,0)
        nodes["N6"] = node("N6",(1000,575),self.COLOR_ORANGE,self.COLOR_BLACK,10,14,0)
        nodes["N7"] = node("N7",(950,375),self.COLOR_ORANGE,self.COLOR_BLACK,10,14,0)
        nodes["N8"] = node("N8",(1100,450),self.COLOR_ORANGE,self.COLOR_BLACK,10,14,0)
        nodes["N9"] = node("N9",(1150,325),self.COLOR_ORANGE,self.COLOR_BLACK,10,14,0)
        nodes["N10"] = node("N10",(400,300),self.COLOR_ORANGE,self.COLOR_BLACK,10,14,0)
        nodes["N11"] = node("N11",(300,250),self.COLOR_ORANGE,self.COLOR_BLACK,10,14,0)
        nodes["N12"] = node("N12",(350,600),self.COLOR_ORANGE,self.COLOR_BLACK,10,14,0)
        nodes["N13"] = node("N13",(275,150),self.COLOR_ORANGE,self.COLOR_BLACK,10,14,0)
         

                 
        return nodes

    def define_edges(self):
        edges = {}
        edges["N1-N2"] = edge(2, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N1"], self.nodes["N2"])
        edges["N1-N3"] = edge(3, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N1"], self.nodes["N3"])
        edges["N1-N5"] = edge(4, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N1"], self.nodes["N5"])
        edges["N5-N4"] = edge(3, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N5"], self.nodes["N4"])
        edges["N2-N3"] = edge(2, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N2"], self.nodes["N3"])
        edges["N3-N5"] = edge(3, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N3"], self.nodes["N5"])
        edges["N2-N7"] = edge(4, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N2"], self.nodes["N7"])
        edges["N5-N6"] = edge(5, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N5"], self.nodes["N6"])
        edges["N7-N6"] = edge(4, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N7"], self.nodes["N6"])
        edges["N6-N8"] = edge(3, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N6"], self.nodes["N8"])
        edges["N8-N9"] = edge(3, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N8"], self.nodes["N9"])
        edges["N13-N11"] = edge(1, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N13"], self.nodes["N11"])
        edges["N11-N10"] = edge(1, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N11"], self.nodes["N10"])
        edges["N10-N12"] = edge(7, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N10"], self.nodes["N12"])
        edges["N11-N12"] = edge(8, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N11"], self.nodes["N12"])
        edges["N12-N1"] = edge(3, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N12"], self.nodes["N1"])
        edges["N10-N1"] = edge(5, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N10"], self.nodes["N1"])
        edges["N10-N2"] = edge(6, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N10"], self.nodes["N2"])
                
        ## THERE EDGES ARE REVERSE OF ABOVE EDGES   ##YUKARDAKİ KENARLARIN TERS YOLLU HALLERİ
        edges["N2-N1"] = edge(2, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N2"], self.nodes["N1"])
        edges["N3-N1"] = edge(3, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N3"], self.nodes["N1"])
        edges["N5-N1"] = edge(4, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N5"], self.nodes["N1"])
        edges["N4-N5"] = edge(3, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N4"], self.nodes["N5"])
        edges["N3-N2"] = edge(2, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N3"], self.nodes["N2"])
        edges["N5-N3"] = edge(3, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N5"], self.nodes["N3"])
        edges["N7-N2"] = edge(4, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N7"], self.nodes["N2"])
        edges["N6-N5"] = edge(5, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N6"], self.nodes["N5"])
        edges["N6-N7"] = edge(4, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N6"], self.nodes["N7"])
        edges["N8-N6"] = edge(3, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N8"], self.nodes["N6"])
        edges["N9-N8"] = edge(3, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N9"], self.nodes["N8"])
        edges["N11-N13"] = edge(1, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N11"], self.nodes["N13"])
        edges["N10-N11"] = edge(1, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N10"], self.nodes["N11"])
        edges["N12-N10"] = edge(7, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N12"], self.nodes["N10"])
        edges["N12-N11"] = edge(8, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N12"], self.nodes["N11"])
        edges["N1-N12"] = edge(3, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N1"], self.nodes["N12"])
        edges["N1-N10"] = edge(5, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N1"], self.nodes["N10"])
        edges["N2-N10"] = edge(6, self.COLOR_GRAY, self.COLOR_ORANGE, self.nodes["N2"], self.nodes["N10"])
        
        
        return edges





"""