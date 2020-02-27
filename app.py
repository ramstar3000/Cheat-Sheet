from flask import Flask, render_template, url_for, request, redirect,session
from datetime import datetime,timedelta
from passlib.hash import sha512_crypt
from flask_pymongo import PyMongo
from re import sub,finditer,findall



#Improve:



app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb+srv://Ramstar:Ramstar@cheat-sheet-rtetw.mongodb.net/test?retryWrites=true&w=majority'
mongo = PyMongo(app)
app.secret_key = 'RamisC00L'



def Renderer(template,tasks=9):
    if tasks==9:
        return(render_template(template,session['username']))
    else:
        return(render_template(template,loopable=[session['username'],tasks]))

def Get_URL(url):
	return(url_root)

    
    
@app.route('/',methods=['POST','GET'])
def index():
	
    if not session:
        return redirect(url_for('login'))
    
    #print((request.url_root))

    
    
    url = request.url
    normal = str(request.url_root)
    
    if "?DLT=" in url:
        url = url.replace(normal,"")
        url = url.replace("?DLT=","")
        url = url.replace(",","")
        url = url.replace("%20"," ")
        url=url.strip()
        #print(url)
        MY_QUERY = {"_id":url}
        #print (MY_QUERY)
        mongo.db.Data.delete_one(MY_QUERY)###############################################
        return redirect("/view")
    
    if url != "normal":
        url = url.replace(normal,"")
        url = url.replace("?info=","")
        url = url.replace("%20"," ")
        url = url.strip()
        
     
        
        task = mongo.db.Data.find({})
        
        for tasks in task:
            if tasks["Content"].strip() in url:
                try:
                    if session['admin']==True or session['username']==tasks["author"]:
                        val = Renderer('Edit.html',tasks)
                        return val
                    else:
			val = render_template("Error.html",message='This feature is not available')
                        return(val)
                except KeyError:
                    if session['username']==tasks["author"]:
                        val = Renderer('Edit.html',tasks)
                        return val
                except:
                    return "Not available"
            
    if request.method == 'POST':
    
    
        try:
            task_name = request.form["Name"]
            task_content = request.form["txt_comments"]
            task_sheet = request.form["sheet"]
            public = request.form["Public"]
            new_task = {"_id":session['username']+task_name,
                            "Name" : task_name,
                            "Content" : task_content.strip(),
                            "Sheet" : task_sheet.strip(),
                            "author":session['username'],
                            "Type":public,
                            "Set":[]}
                
            #print(task_sheet,task_sheet.strip())
            if not task_name:
                return Renderer('index.html')
            if not task_content:
                return Renderer('index.html')
            if not task_sheet:
                return Renderer('index.html')
                    
            task = mongo.db.Data.find({})    
            for item in task:
                if item["_id"] == session['username']+task_name:
                    val = render_template("Error.html",message="This data already exists please choose another")
                    return(val)
                else:pass
                
                
            mongo.db.Data.insert_one(new_task)
            #print("Hello")
            #print("World")          
            #return redirect("/view")
            #return (url_for('Viewing'))


           
        except KeyError:
            task = mongo.db.Data.find({})
            #print(1)
            task_name = request.form['Name_1']
            #print()
            for tasks in task:
                #print(tasks["Name"],task_name)
                if (tasks["Name"]).strip() == task_name:
                    tasks_author = tasks['author']
                    #print("Yay")
            #print(request.form)
            task_content = request.form["txt_comments"]
            task_sheet = request.form["sheet"]
            public = request.form["Public"]
            #name = request.form["Name_Old"]
                
            
            #print (tasks_author)
    
            query = {"_id":tasks_author+task_name} 
            new_task = { "$set":{"Content" : task_content.strip(), "Sheet" : task_sheet.strip(),"Type":public}}
            mongo.db.Data.update_one(query,new_task)
            #print("1111000000002222222999999938884755467")
            return redirect("/Sheets")

        
    
        
    else:


        tasks = mongo.db.Data.find({})
    
        return Renderer('index.html', tasks)#, tasks = tasks)

@app.route('/view',methods=['POST','GET'])
def Viewing():
    
    if not session:
        return redirect(url_for('login'))
    #print((request.url_root))
    #print(request.base_url)

    if request.method == 'GET':
        
        url = request.url
        normal = (request.base_url)
        if url != normal:
            url = url.replace(normal,"")
            url = url.replace("?info=","")
            url = url.replace("%20"," ")
            url = url.strip()
            task = mongo.db.Data.find({})
            avail = []
            if "val=True" in url:
                avail = []
                tasks = mongo.db.Data.find({})
                for item in tasks:
                    if item["Type"]=="Private" and item["author"]==session["username"]:
                        avail.append(item)
                val =  Renderer('view_database.html', avail)
                return val
                
            
            if "val=False" in url:
     
                url = url.replace("&&val=False","")
                
                for item in task:
                    if (item["Content"]).strip() in url:
                        item["Sheet"]=item["Sheet"].strip()
                        #print(item["Sheet"])
                    
                        val = render_template('output.html',loop=[item,True])
                        #val = render_template('output.html',loop=[item])
                        return (val)
                    else:
                        pass
                    
            for tasks in task:
                #print(1)
                if (tasks["Content"]).strip() == url:
                    tasks["Sheet"]=tasks["Sheet"].strip()
                    #print(tasks["Sheet"])
                    
                    val =  render_template('output.html', loop = [tasks,False])
                    #val = render_template('output.html',loop=[tasks])
                    return val
            
            if "Search" in url:
                Filter = url.replace("?Search","")
                Filter=Filter.upper()
                avail = []
                #Filter = request.form["Search"].upper()
                tasks = mongo.db.Data.find({})
                for item in tasks:
                    if item["Type"]=="Public":
                        avail.append(item)
                        
                listl = []
                for item in avail:
                    #print(item["Name"].upper(),Filter)
                    if item["Name"].upper() in Filter:
                        listl.append(item)
                        
                if listl:
                    
                    val =  Renderer('view_database.html', listl )
                    return(val)
                else:
                    val =  Renderer('view_database.html', avail)
                    return val
                    
            else:
                tasks = mongo.db.Data.find({})
                avail = []
                for item in tasks:
                    if item["Type"]=="Public":
                        avail.append(item)
		
                val = Renderer('view_database.html', avail)#\\\\\\\\
                return val
            
        else:

            print("Running View func")
        
 
            avail = []
            tasks = mongo.db.Data.find({})
            for item in tasks:
                if item["Type"]=="Public":
                        avail.append(item)
                        
            
            val = Renderer('view_database.html', avail)
            return val
    else:
        x=0
##        
##        if "Save" in request.form:
##            print(1)
##        else:
##            print(2)
##        
        for element in request.form:
            if element=="Save":
                x=1
            else:pass
	
        if x==1:
            
            
            
            
            listl = []
            print(request.form)
            for card in request.form:
                if card != "Save":
                    listl.append(card)
                else:
                    sets = request.form[card]
            tasks = mongo.db.Data.find({})
            
            Real_sets=[]
            for item in tasks:
                for valu in item["Set"]:
                    Real_sets.append(valu)
            Real_sets = set(Real_sets)
            if sets in Real_sets:
                val = render_template("Error.html",message="Please create a more unique set name \n \n e.g. Add your username at the end")
                return(val)#Perhaps use username scheme to reduce likelihood
            print (listl)
            for element in range(len(listl)):
                length = len(listl[element])
                print(length)
                print(listl[element],end='')
                tasks = mongo.db.Data.find({})#pointer error if
                for item in tasks:
                    comp = (item["_id"][0:length])
                    if listl[element]==comp:
                        print("Pass")
                        value = item["Set"]
                        value.append(sets)
                        query = {"_id":item["_id"]}
                        new_task = { "$set":{"Set" : value}}
                        print(query,new_task)
                        mongo.db.Data.update_one(query,new_task)
                        y = 1
                        break
 
                        
                    else:
                        pass
            return (redirect("/"))

            
        
        if x==0:
            #print(request.form)
            x = (len(request.form))
            loop=[]
            x=[]
            
            for num in request.form:
                x.append(num)
            for element in range(len(x)):
                tasks = mongo.db.Data.find({})#pointer error if
                #print(x[element])
                for item in tasks:
                    #print(x[element],item["_id"])
                    if x[element]==item["_id"]:
                        loop.append(item)
                    else:pass
            #print(loop)
            
            for element in loop:
                element["Sheet"] = (element["Sheet"].strip())
            #print(loop)
            if loop:
                z=0
##                if session["admin"]==True:
##                    z=1
                val = render_template("Cheat-Sheet.html",loop=["",loop,True,z])
            else:
                val = redirect("/view")
            return val
            

                

     
            
@app.route('/register',methods=['POST','GET'])
def register():
    if request.method == 'POST':
        name = request.form.get("name")
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        users = mongo.db.Credentials.find({})
        for item in users:
            if item["User"] == username:
                val = render_template("Error.html",message="This username already exists please choose another")
                return render_template("Error.html",message="Bad username")
            else:pass
        secure_password = sha512_crypt.hash(str(password))
        creds = {"Name":name,"User":username,"Pass":secure_password,"Admin":False}
        if password == confirm:
            mongo.db.Credentials.insert_one(creds)
            return redirect(url_for('index'))       
        else:
            return render_template("Error.html",message="Oh No!!!!")
        
    else:
        return render_template("Registration.html")


@app.route('/login',methods=['POST','GET'])
def login():
    if session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        
        tasks = mongo.db.Credentials.find({})
        username = request.form.get("name")
        pswd = request.form.get("password")
        for element in tasks:
            if element["User"]== username:
                x = (element["Pass"])
                if (sha512_crypt.verify(str(pswd), str(x))):
                    session['username'] = username
                    session['admin'] = element["Admin"]
                    session.permanent = True
                    app.permanent_session_lifetime = timedelta(minutes=10)
                    return redirect(url_for('index'))

            else:pass
                #return("Wrong username or password")
        return render_template("Error.html",message="Wrong username or password")
    else:
        return render_template("login.html")

@app.route('/Logout',methods=['GET'])
def Logout():
    session.clear()
    return redirect("/login")


@app.route('/CheatSheet',methods=['GET','POST'])
def Big_View():
    
    
  
    
    if request.method=='POST':

        listl = []
        for card in request.form:
            if card != "Save":
                card.append(listl)
            else:
                x = card
        
        return redirect('/')
    else:
        tasks = mongo.db.Data.find({})
        url = request.url
        if "True" in url:
            #print("One") 
                
        
            avail = []
            for item in tasks:
                if item["Type"]=="Public":
                    avail.append(item)

            loop = []
            for item in avail:
                item['Sheet']=item['Sheet'].strip()
                #print(item['Sheet'])
                loop.append(item)
                
                
            x=0
            if session["admin"]==True:
                x=1
            
            
            val = render_template("Cheat-Sheet.html",loop=["",loop,True,x])
            return val
        else:

            avail = []
            for item in tasks:
                if item["Type"]=="Private" and item["author"]==session["username"]:
                    avail.append(item)

            loop = []
            for item in avail:
                item['Sheet']=item['Sheet'].strip()
                #print(item['Sheet'])
                loop.append(item)
                #print(avail)
            
            
            x=0
            if session["admin"]==True:
                x=1
            val = render_template("Cheat-Sheet.html",loop=["",loop,True,x])
            return val
        
@app.route('/Sheets',methods=['GET','POST'])
def Sheets():
    if request.method == 'POST':
        url = request.url
        normal =  str(request.base_url)+"?info="
        url = url.replace(normal,"")
        names = []
        sets2d = []
        print(request.form)
        for element in request.form:
            tasks = mongo.db.Data.find({})
            length = len(element)
            for item in tasks:
                comp = (item["_id"][0:length])
                if element==comp:
                    names.append(item["_id"])
                    sets2d.append(item["Set"])
        for value  in sets2d:
            for item in value:
                if item == url:
                    value.remove(url)
##        return(str(sets2d))
                    
        print(names)
        for counter in range (len(names)):       
            query = {"_id":names[counter]} 
            new_task = { "$set":{"Set":sets2d[counter]}}
            #print (str([query,new_task]))
            mongo.db.Data.update_one(query,new_task)
        return redirect("/Sheets")
  
    
    else:
        url = request.url
        normal = str(request.base_url)
        tasks = mongo.db.Data.find({})
        name = request.form.get("Save")
        
        if url == normal:
            sets = []
            
            for listl in tasks:
                for item in listl["Set"]:
                    sets.append(item)
            sets = [x for x in sets if x]
            sets = set(sets)
            

            
            return render_template("view_sheets.html",sets = sets)
        url = url.replace(normal,"")
        pattern = r"%[2-7]."
        url = sub(pattern,"",url)
        
        if "?info" in url:     
     
            url = url.replace("?info=","") 
            #print(url)
            
            sets = url
            new = []
            
            
            for listl in tasks:
                for item in listl["Set"]:
                    #print(item)
                    if item == sets:
                        #print(item)
                        new.append(listl)
            #print(new)
            #print(sets)
            x=0
            if session["admin"]==True:
                x=1
            
            
            return render_template("Cheat-Sheet.html",loop=[sets,new,False,x])
                        
        elif "?Search" in url:


            Filter = url.replace("?Search=","")
            #print (Filter)
                    
     
            listl = []
            for item in tasks:
                for element in item["Set"]:
                    if  element in Filter:
                        listl.append(element)    
            if listl:
                listl= set(listl)
                val =  render_template('view_sheets.html', sets = listl )
                return(val)
        

            
        return render_template("view_sheets.html")
    

@app.route('/Print',methods=['GET','POST'])
def Print():

         global count
         url = request.url

         if "data" in url:

            url = url.replace("data1","")  
            count += 1 
         else:
            count = 0



         normal = str(request.base_url)
         tasks = mongo.db.Data.find({})

        
     
         sets = []
            
         for listl in tasks:
             for item in listl["Set"]:
                 sets.append(item)
             sets = [x for x in sets if x]
         sets = set(sets)

            
    
         url = url.replace(normal,"")
         pattern = r"%[2-7]."
         url = sub(pattern,"",url)
     
         url = url.replace("?info=","")        

         sets = url
         new = []

         tasks = mongo.db.Data.find({})
         for listl in tasks:
            for item in listl["Set"]:
                 if item == sets:
                     new.append(listl)
  


             
         return render_template("print.html",loop=[sets,new,False,0,1]) 



    



if __name__ == "__main__":
    app.secret_key = 'RamisC00L'
    app.run(debug = True)




