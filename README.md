# distributor-to-disaster-areas-with-dijsktra-algorithm-
# Ön Açıklama
### Language
#### I tried to write english and turkish for explanetions , My english level can has some deficiency ,so ı am sorry about that
This project inspired by the earthqueake in turkey in 2023,that disaster cause a logistic problems , we tried send helping tracks and earth movers to earthquake zone but we were dont know which area needs more help.
Some ways are damaged aspecially hatay way was not usable.
#### Bu proje 2023'te yaşadığımız Maraş depreminden esinlenerek , simüle etmeye çalıştığım bir projedir.Yaşanan koordinasyon problemleri bilgisayar ile nasıl şekilde çözülebilir sorusu üzerinde bu şekilde bir optimizasyon çözümü bulmmaya çalıştım.Yollardaki problemler ve bölgelerdeki hasarlar hesaba katılarak en iyi şekilde optimizasyon nasıl sağlanırın cevabını aradım.

# How can i test it? /  Nasıl Test edebilirim?
Go _define_nodes()_ method and add node like node(name,location,,color_text,color_circle,radius_small,radius_big,demand,assets) and after go _define_edges()_ add like edge(weight,color_line,color_text,tail_node,head_node)
you can use it defined colors

 _define_nodes()_ metoduna git ve node(name,location,,color_text,color_circle,radius_small,radius_big,demand,assets) gibi düğümleri ekle ardından  go _define_edges()_ edge(weight,color_line,color_text,tail_node,head_node)
gibi kenarları ekle , önceden tanımlanmış renkleri kullanabilirsin _self.COLORS_RED_ gibi

# Amaç / Purpose
#### Moving assets in the most convenient way, starting from the most needed area
#### En ihtiyaçlı bölgeden başlayarak en uygun yoldan varlıkları taşımak

# Yöntem / Method

#### Her ihtiyaç sahibi düğümün diğer düğümlere olan uzaklıklarını Dijkstra algoritmasını kullanarak bulup , en ihtiyaç sahibinden en az ihtiyaç sahibi düğüme doğru sıralayarak ve bu sırayı sürekli güncel tutarak en yakın varlıklı düğümden varlık transfer etme

#### For each node , Determinining distances of the node to other nodes with dijkstra algorithm and use those distances for transportation,   implementing process starting wtih most needy node to least needy node 

# Sonuç / Result
#### Results includes for each node distances to other nodes ( _node.distances_ attribute ) and which assets ,coming from who and how much coming (_node.received_ attribute)
#### Sonuç olarak şunları elde edebiliriz: düğümlerin diğer düğümlere en kısa uzaklıkları ve ihtiyaç sahibi düğümlerin hangi varlığı nerden aldıkları.

####
<img src="https://raw.githubusercontent.com/rag0nn/distributor-to-disaster-areas-with-dijsktra-algorithm/master/images/results_screen.jpg">
<img src="https://raw.githubusercontent.com/rag0nn/distributor-to-disaster-areas-with-dijsktra-algorithm/master/images/results_terminal.jpg">

# Examples  / Örnekler
<img src="https://raw.githubusercontent.com/rag0nn/distributor-to-disaster-areas-with-dijsktra-algorithm/master/images/normal_node_map.jpg">
<img src="https://raw.githubusercontent.com/rag0nn/distributor-to-disaster-areas-with-dijsktra-algorithm/master/images/drawn_with_weights_map.jpg">
<img src="https://github.com/rag0nn/distributor-to-disaster-areas-with-dijsktra-algorithm/blob/master/images/gif.gif">

