from discord import *
from asyncio import *
from discord.ext.commands import *
from re import *
from time import *
import random as r
import threading as t
import json as j
import os

#Variable
client=Bot(command_prefix="$")
token="Type Token"
Maker=462920963768582145
pilo_uid=847112363081072650
folder="DataBase\\"
data_file=folder+"Pilo_UserDB.json"
stock_file=folder+"Pilo_StockDB.json"
user=[]
stock=[]
unit="$"
tick=0
cycle=120
before_channel=""

def log(title,text):
    print(f"[{title}] : {text}")

#Class
class Stock:
    def __init__(self,name:str,cost:int):
        self.name=name
        self.cost=cost
        self.customer=[]
    def setCustomer(self,customer:dict):
        self.customer=customer
    def getN(self, uid):
        for i in range(len(self.customer)):
            if(self.customer[i]["uid"]==uid):
                return 0
        return None
    def buy(self,uid,count):
        try:
            num=self.getN(uid)
            if(num==None):
                self.customer.append({"uid":uid,"count":count})
            else:
                self.customer[num]["count"]+=count
            log("Buy Stock",f"{uid} -> {self.name}[cnt {count}]")
            return True
        except Exception:
            log("Error Stock",f"Exception in buying {self.name}")
            return False
    def sell(self,uid,count):
        try:
            num=self.getN(uid)
            if(num==None):
                return None
            if(self.customer[num]["count"]<count):
                return False
            log("Sell Stock",f"{uid} -> {self.name}[cnt {count}]")
            self.customer[num]["count"]-=count
            if(self.customer[num]["count"]<=0):
                del(self.customer[num])
            return True
        except Exception:
            log("Error Stock",f"Exception in selling {self.name}")

#Function
def getNum(uid):
    for i in range(len(user)):
        if user[i]["uid"]==uid:
            return i
    return None

def argSplit(arg, findArg):
    args=split(" ",arg)
    for i in range(len(args)):
        if args[i].find(findArg)==-1:
            final=None
        else:
            return (args[i][args[i].find(findArg)+len(findArg):])
    return ""

def toDict(name, uid, money):
    var={
        "name":name,
        "uid":uid,
        "money":money
    }
    return var

def Save():
    global user
    global stock
    j.dump(j.dumps(user),open(data_file,"w"))
    var=[]
    for i in stock:
        data={"name":i.name,"customer":i.customer,"cost":i.cost}
        var.append(data)
    j.dump(j.dumps(var),open(stock_file,"w"))

def Load():
    global user
    global stock
    try:
        user=j.loads(j.load(open(data_file,"r")))
    except FileNotFoundError or FileExistsError:
        j.dump(j.dumps(user),open(data_file,"w"))
    try:
        var=j.loads(j.load(open(stock_file,"r")))
        stock=[]
        for i in var:
            value=Stock(i["name"],i["cost"])
            value.setCustomer(i["customer"])
            stock.append(value)
    except FileNotFoundError or FileExistsError:
        j.dump(j.dumps(stock),open(stock_file,"w"))

def findStock(name:str):
    global stock
    for i in range(len(stock)):
        if(stock[i].name.upper()==name.upper()):
            return i
    return None

def getNumName(name:str):
    global user
    for i in range(len(user)):
        if(user[i]["name"]==name):
            return i
    return None

#Thread Function
def Operate():
    global stock
    global tick
    global cycle
    while True:
        if(tick>=cycle):
            for i in stock:
                i.cost+=r.randint(-r.randint(1,10),r.randint(1,10))
                if(i.cost<1):
                    i.cost=1
            #log("Cycle Stock","Completed")
            tick=0
        tick+=1
        sleep(1)

#Main
Load()
thread1=t.Thread(target=Operate)
thread1.start()
os.system("title PILO")

@client.event
async def on_member_join(user):
    log("On Join",user)

@client.event
async def on_ready():
    log("On Connect","Start PILO_BOT")
    await client.change_presence(activity=Game("??????"))

@client.event
async def on_message(msg):
    global user
    global stock
    global Maker
    global unit
    global tick
    global cycle
    global before_channel
    text=msg.content
    name=str(msg.author)
    ID=str(msg.author)
    uid=msg.author.id
    name=name[:name.find("#")]
    host=(uid==Maker)
    metion=(text.find(f"<@!{pilo_uid}>")!=-1)

    if uid!=pilo_uid:
        if text.find(" ")!=-1:
            empty=text.find(" ")
            cmd=text[:empty]
            arg=text[empty+1:]
        else:
            cmd=text
            arg=None

        #DataBase
        exist_bool=False
        for i in range(len(user)):
            if user[i]["uid"]==uid:
                exist_bool=True
                if(user[i]["name"]!=name):
                    log("Data Modify", f"{user[i]['name']} ??? {name}")
                    user[i]["name"]=name
                break
        if(exist_bool==False):
            log("Add User", ID)
            #ADD EVENT
            user.append(toDict(name,uid,0))

        num=getNum(uid)

        #Key Test
        while True:
            try:
                key=["name","uid","money"]
                for i in range(len(key)):
                    err_k=key[i]
                    a=user[num][key[i]]
                break
            except KeyError:
                log("Key Error", f"({ID}){err_k}")
                user[num][err_k]=0

        #Money ADD
        user[num]["money"]+=1

        #Channel
        channel=str(msg.channel).replace(":","_")
        if before_channel!=channel:
            print(f"\n[{channel}]")
            before_channel=channel
        print(f"{ID} >> {text}")

        #Chat
        if(text.find("??????")!=-1 or text.find("??????")!=-1 or text.find("??????")!=-1):
            if host:
                await msg.channel.send("????????????!!!")
                await msg.add_reaction("????")
            else:
                await msg.channel.send("????????????!")
        if(text.find("??????")!=-1 or text.upper().find("PILO")!=-1 or metion):
            await msg.channel.send("?????? ??? ?????????????????")
        
        #Command
        if(cmd=="$help"):
            embed=Embed(title="PILO",color=0x6BA6FF)
            embed.add_field(name="$info",value=f"????????? ???????????? ???????????????.",inline=False)
            embed.add_field(name="$buy",value=f"????????? ?????????.",inline=False)
            embed.add_field(name="$sell",value=f"????????? ?????????.",inline=False)
            await msg.channel.send(embed=embed)
        elif(cmd=="$info"):
            embed=Embed(title="INFO",color=0xC19CF5)
            embed.add_field(name="Name",value=f"**{name}**",inline=False)
            embed.add_field(name="Money",value=f"**{user[num]['money']}{unit}**",inline=False)
            for i in stock:
                for j in i.customer:
                    if(j["uid"]==uid):
                        embed.add_field(name=f"{i.name}",value=f"**Count** : {j['count']}\n**Cost** : {i.cost}{unit}",inline=True)
                        break
            embed.set_thumbnail(url=msg.author.avatar_url)
            await msg.channel.send(embed=embed)
        elif(cmd=="$data" and host):
            embed=Embed(title="USER DATA",color=0xF3AAFF)
            for i in user:
                string=f"**Money** : {i['money']}{unit}"
                for j in stock:
                    for k in j.customer:
                        if(k["uid"]==i['uid']):
                            string+=f"\n**{j.name}** : {k['count']}"
                            break
                embed.add_field(name=f"[{i['name']}]",value=string,inline=True)
            await msg.channel.send(embed=embed)
        elif(cmd=="$show"):
            embed=Embed(title="STOCK",color=0xF4FF99)
            for i in stock:
                embed.add_field(name=f"{i.name}",value=f"**Cost** : {i.cost}{unit}",inline=True)
            embed.add_field(name=f"Cycle",value=f"{cycle-tick}s",inline=False)
            await msg.channel.send(embed=embed)
               
        #Arg Command
        if(arg!=None):
            if(cmd=="$stock"):
                if(arg.find("-host")!=-1 and host):#Host
                    name=argSplit(arg, "name:")
                    if(arg.find("-help")!=-1 or name==""):
                        await msg.channel.send("**?????????** : $stock -host -[create/delete] name:[str] cost:[num]")
                    else:
                        if(arg.find("-create")!=-1):
                            cost=argSplit(arg, "cost:")
                            try:
                                cost=int(cost)
                                overlap=False
                                for i in stock:
                                    if(i.name==name):
                                        overlap=True
                                        break
                                if(overlap==True):
                                    await msg.channel.send("?????? ?????? ???????????????!")
                                else:
                                    stock.append(Stock(name,cost))
                                    log("Host Stock",f"Craeted '{name}'")
                                    await msg.channel.send(f"'{name}'?????? ????????? ????????? ??????????????????! [??????:{cost}{unit}]")
                            except ValueError:
                                await msg.channel.send("cost??? ?????????????????? ??????!")     
                        if(arg.find("-delete")!=-1):
                            try:
                                stock_num=-1
                                for i in range(len(stock)):
                                    if(stock[i].name==name):
                                        stock_num=i
                                        break
                                if(stock_num==-1):
                                    await msg.channel.send("?????? ???????????????!")
                                else:
                                    for i in stock[stock_num].customer:
                                        user[getNum(i["uid"])]['money']+=i["count"]*stock[stock_num].cost
                                        stock[stock_num].sell(i["uid"],i["count"])
                                    del(stock[stock_num])
                                    log("Host Stock",f"Deleted '{name}'")
                                    await msg.channel.send(f"'{name}'?????? ????????? ????????? ???????????????!")
                            except Exception:
                                log("Error Stock",f"Exception in deleting {name}'")
                                await msg.channel.send(f"????????? ??????????????? ????????? ????????????...")                        
            if(cmd=="$buy"):
                name=argSplit(arg, "name:")
                count=argSplit(arg, "count:")
                stock_num=findStock(name)
                if(arg.find("-help")!=-1 or name=="" or count==""):
                    await msg.channel.send(f"**?????????** : $buy name:[str] count:[num/num{unit}]")
                else:
                    if(stock_num==None):
                            await msg.channel.send(f"'{name}'?????? ????????? ????????? ?????????...")
                    else:
                        
                        count_err=False
                        try:
                            count=int(count)
                            if(count<=0):
                                count_err=True
                        except ValueError:
                            count_err=True
                            if(count=="all"):
                                count=user[num]['money']//stock[stock_num].cost  
                                count_err=False
                            elif(count.find(unit)!=-1):
                                try:
                                    count=int(count.replace(unit,""))//stock[stock_num].cost
                                    count_err=False
                                except ValueError:
                                    count_err=True
                        if(count_err==True):
                            await msg.channel.send(f"count??? ?????? ?????? ???({unit})??? ???????????????!")
                        else: 
                            pay=stock[stock_num].cost*count
                            if(user[num]["money"]<pay):
                                await msg.channel.send(f"????????? ?????? ????????????![??????:{stock[stock_num].cost}{unit}]")
                            else:
                                if(stock[stock_num].buy(uid,count)==True):
                                    user[num]["money"]-=pay
                                    await msg.channel.send(f"?????? '{name}'??? {count}??? ????????????! [?????? ???:{user[num]['money']}{unit}]")
                                else:
                                    await msg.channel.send(f"?????? '{name}'??? ???????????? ???????????????. ToT")
            elif(cmd=="$sell"):
                name=argSplit(arg, "name:")
                count=argSplit(arg, "count:")
                stock_num=findStock(name)
                if(arg.find("-help")!=-1 or name=="" or count==""):
                    await msg.channel.send("**?????????** : $sell name:[str] count:[num]")
                else:
                    if(stock_num==None):
                        await msg.channel.send(f"'{name}'?????? ????????? ????????? ?????????...")
                    else:
                        count_err=False
                        try:
                            count=int(count)
                            if(count<=0):
                                count_err=True
                        except ValueError:
                            count_err=True
                            if(count=="all"):
                                count=stock[stock_num].customer[stock[stock_num].getN(uid)]["count"]
                                count_err=False
                            elif(count.find(unit)!=-1):
                                try:
                                    count=int(count.replace(unit,""))//stock[stock_num].cost
                                    count_err=False
                                except ValueError:
                                    count_err=True
                    if(count_err==True):
                        await msg.channel.send("count??? 1????????? ????????? ???????????????!")
                    else:
                        complete=stock[stock_num].sell(uid,count)
                        if(complete==None):
                            await msg.channel.send(f"????????? ??? ????????? ????????? ?????? ?????????!")
                        elif(complete==False):
                            await msg.channel.send(f"???????????? ????????? ????????? ?????? ?????????!")
                        else:
                            user[num]['money']+=count*stock[stock_num].cost
                            await msg.channel.send(f"?????? '{name}'??? {count}??? ???????????????! [?????? ???:{user[num]['money']}{unit}]")
            if(cmd=="$modify" and host): 
                if(arg.find("-money")!=-1):
                    target_name=argSplit(arg,"name:")
                    target_value=argSplit(arg,"value:")
                    try:
                        target_num=getNumName(target_name)
                        target_value=int(target_value)
                        if(target_num==None):
                            await msg.channel.send(f"'{target_name}'?????? ????????? ???????????? ?????????!")
                        if(arg.find("-help")!=-1 or target_name=="" or target_value==""):
                            await msg.channel.send("**?????????** : $modify -money -[set/add] name:[str] value:[num]")
                        elif(arg.find("-set")!=-1):
                            user[target_num]["money"]=target_value
                            log("Modify Money",f"<Set> {target_name} -> {target_value}{unit}")
                            await msg.channel.send(f"'{target_name}'????????? ????????? ?????? {target_value}{unit}??? ??????????????????!")
                        elif(arg.find("-add")!=-1):
                            user[target_num]["money"]+=target_value
                            log("Modify Money",f"<Add> {target_name} -> {target_value}{unit}")
                            await msg.channel.send(f"'{target_name}'????????? ???????????? {target_value}{unit}??? ???????????????! [???:{user[target_num]['money']}{unit}]")      
                    except ValueError:
                        await msg.channel.send("value??? ????????? ????????????!")
                    
                elif(arg.find("-help")!=-1):
                    await msg.channel.send("**?????????** : $modify -[money]")

              
        Save()

client.run(token)
