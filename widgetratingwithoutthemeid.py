# this code considers the data from db and give ratings to all the widget in a website for all website information that db contains (same theme can be repeated mutiple times as the theme id condition is not specified)

from pymongo import MongoClient
from collections import defaultdict

client = MongoClient()
client = MongoClient("mongodb://43.252.89.89:27017/")
db=client.Widgets.sites
cursor= db.find()
for document in cursor:
    url=document["url"]
    doc= document['elements']
    Screenwidth= document["screenWidth"]
    Screenheight=document["screenHeight"]
    Object_id= document["_id"]
    print '\n',url,'-',Object_id,'\n'
    Screenheight =Screenheight-80      # minus 80 in order to ignore the task bar
    divhorizontal=Screenwidth/4        #dividing the screen into four vertical parts
    divvertical=Screenheight/4         #dividing the screen into four horizontal parts
    widgetname=[]
    ratingarray=[]
    if(doc):
        for element in doc:
            display=element["display"]
            left= element["left"]
            top=element["top"]
            height=element["height"]
            width=element["width"]
            area=height*width
            arearate=area/1429
            
            if display=='true':       # if the widget is visible 
                if ((left <=(divhorizontal*2)) & (top <=(divvertical*2))):
                    rating = 200+(arearate*4)
                elif(((left >(divhorizontal*2))and (top <=(divvertical*2))) or (((top > (divvertical*2)) and(top<=(divvertical*3))))):
                    rating = 150+(arearate*3)
                elif(top > (divvertical*3)) and (top <(divvertical*4)):
                    rating = 50+(arearate*2)
                elif (top >= (divvertical*4)):
                    rating = 10+(1*arearate)
            else:                     # if the widget is not visible
                if ((left <=(divhorizontal*2)) & (top <=(divvertical*2))):
                    rating = 100+(arearate*4)/2
                elif(((left >(divhorizontal*2))and (top <=(divvertical*2))) or (((top > (divvertical*2)) and(top<=(divvertical*3))))):
                    rating = 75+(arearate*3)/2
                elif(top > (divvertical*3)) and (top <(divvertical*4)):
                    rating = 25+(arearate*2)/2
                elif (top >= (divvertical*4)):
                    rating = (1*arearate)/2
        #print element["widgetName"],rating     #if we print here, the widget repeating for n times will appear n times with their individual ratings
            widget=element["widgetName"]
            widgetname.append(widget)
            ratingarray.append(rating)
    final=[]
    final.append([])
    for i, x in enumerate(widgetname):
        if(widgetname.count(x)==1):            # if the widget is repeated only for once then it gets printed here
            final[0].append([x,ratingarray[i]])
    def list_duplicates(widgetname):
        tally = defaultdict(list)
        for i,item in enumerate(widgetname):
            tally[item].append(i)
        return((key,locs) for key,locs in tally.items() 
                            if len(locs)>1)
    #finalrating=[]
    array=[]
    for dup in (list_duplicates(widgetname)):   # if the widget is repeated then the indices are obtained
        indices=dup[1]
    
        for i in indices:
            array.append(ratingarray[i])        #the widget repeating multiple times, the ratings are added
        for j in range(1,len(array)):
            array[j]=(array[j]/j)
        sumarray=sum(array)
        #avgrating=sumarray/(len(array))
        #finalrating.append(avgrating)
    
        #final[0].append([dup[0],avgrating])
    
        final[0].append([dup[0],sumarray])
    
        del array[: ]
        # here the rating array(ratings of the same widget for more than once) is deleted so that the next widget repeating for multiple times uses the same array 
    a=[]
    b=[]
    # a array is for ratings and b for widgetnames
    for i in range(0,len(final[0])):
        temp= final[0][i]
        a.append(temp[1])
        b.append(temp[0])
    n=sorted(range(len(a)),key=lambda x:a[x])
    k=len(n)-1
    for i in range(0,len(n)):
        j=n[k]
        k-=1
        print b[j],'-',a[j]

        
        
    
    
