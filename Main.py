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
client=Bot(command_prefix="$", intents=Intents.all())
token="NzQ3MzQ4Njk0ODk4MDQ5MDg0.GM4lhz.eW4KAM9mLuu737cJ6YjBc0SjNzyvgH5CdpKI4s"
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
    await client.change_presence(activity=Game("주식"))

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
                    log("Data Modify", f"{user[i]['name']} → {name}")
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
        if(text.find("안녕")!=-1 or text.find("안농")!=-1 or text.find("ㅎㅇ")!=-1):
            if host:
                await msg.channel.send("창조자님!!!")
                await msg.add_reaction("🍀")
            else:
                await msg.channel.send("반가워요!")
        if(text.find("필로")!=-1 or text.upper().find("PILO")!=-1 or metion):
            await msg.channel.send("누가 절 부르셨나요??")
        
        #Command
        if(cmd==";help"):
            embed=Embed(title="PILO",color=0x6BA6FF)
            embed.add_field(name="$info",value=f"당신의 데이터를 출력합니다.",inline=False)
            embed.add_field(name="$buy",value=f"주식을 삽니다.",inline=False)
            embed.add_field(name="$sell",value=f"주식을 팝니다.",inline=False)
            await msg.channel.send(embed=embed)
        elif(cmd==";info"):
            embed=Embed(title="INFO",color=0xC19CF5)
            embed.add_field(name="Name",value=f"**{name}**",inline=False)
            embed.add_field(name="Money",value=f"**{user[num]['money']}{unit}**",inline=False)
            for i in stock:
                for j in i.customer:
                    if(j["uid"]==uid):
                        embed.add_field(name=f"{i.name}",value=f"**Count** : {j['count']}\n**Cost** : {i.cost}{unit}",inline=True)
                        break
            await msg.channel.send(embed=embed)
        elif(cmd==";data" and host):
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
        elif(cmd==";show"):
            embed=Embed(title="STOCK",color=0xF4FF99)
            for i in stock:
                embed.add_field(name=f"{i.name}",value=f"**Cost** : {i.cost}{unit}",inline=True)
            embed.add_field(name=f"Cycle",value=f"{cycle-tick}s",inline=False)
            await msg.channel.send(embed=embed)
        #Arg Command
        if(arg!=None):
            if(cmd==";stock"):
                if(arg.find("-host")!=-1):#Host
                    name=argSplit(arg, "name:")
                    if(arg.find("-help")!=-1 or name==""):
                        await msg.channel.send("**사용법** : $stock -host -[create/delete] name:[str] cost:[num]")
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
                                    await msg.channel.send("이미 있는 이름이에요!")
                                else:
                                    stock.append(Stock(name,cost))
                                    log("Host Stock",f"Craeted '{name}'")
                                    await msg.channel.send(f"'{name}'라는 이름의 주식을 만들었습니다! [주가:{cost}{unit}]")
                            except ValueError:
                                await msg.channel.send("cost는 정수형이여야 해요!")     
                        if(arg.find("-delete")!=-1):
                            try:
                                stock_num=-1
                                for i in range(len(stock)):
                                    if(stock[i].name==name):
                                        stock_num=i
                                        break
                                if(stock_num==-1):
                                    await msg.channel.send("없는 이름이에요!")
                                else:
                                    for i in stock[stock_num].customer:
                                        user[getNum(i["uid"])]['money']+=i["count"]*stock[stock_num].cost
                                        stock[stock_num].sell(i["uid"],i["count"])
                                    del(stock[stock_num])
                                    log("Host Stock",f"Deleted '{name}'")
                                    await msg.channel.send(f"'{name}'라는 이름의 주식을 삭제했어요!")
                            except Exception:
                                log("Error Stock",f"Exception in deleting {name}'")
                                await msg.channel.send(f"주식을 삭제하는중 오류가 났습니다...")                        
            if(cmd==";buy"):
                name=argSplit(arg, "name:")
                count=argSplit(arg, "count:")
                stock_num=findStock(name)
                if(arg.find("-help")!=-1 or name=="" or count==""):
                    await msg.channel.send(f"**사용법** : $buy name:[str] count:[num/num{unit}]")
                else:
                    if(stock_num==None):
                            await msg.channel.send(f"'{name}'라는 이름의 주식이 없어요...")
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
                            await msg.channel.send(f"count는 정수 또는 돈({unit})을 적어야해요!")
                        else: 
                            pay=stock[stock_num].cost*count
                            if(user[num]["money"]<pay):
                                await msg.channel.send(f"당신의 돈이 모자라요![주가:{stock[stock_num].cost}{unit}]")
                            else:
                                if(stock[stock_num].buy(uid,count)==True):
                                    user[num]["money"]-=pay
                                    await msg.channel.send(f"주식 '{name}'을 {count}개 샀습니다! [남은 돈:{user[num]['money']}{unit}]")
                                else:
                                    await msg.channel.send(f"주식 '{name}'을 사는것을 실패했어요. ToT")
            elif(cmd==";sell"):
                name=argSplit(arg, "name:")
                count=argSplit(arg, "count:")
                stock_num=findStock(name)
                if(arg.find("-help")!=-1 or name=="" or count==""):
                    await msg.channel.send("**사용법** : $sell name:[str] count:[num]")
                else:
                    if(stock_num==None):
                        await msg.channel.send(f"'{name}'라는 이름의 주식이 없어요...")
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
                        await msg.channel.send("count는 1이상의 정수만 적어야해요!")
                    else:
                        complete=stock[stock_num].sell(uid,count)
                        if(complete==None):
                            await msg.channel.send(f"당신은 이 주식을 가지고 있지 않아요!")
                        elif(complete==False):
                            await msg.channel.send(f"그만큼의 주식을 가지고 있지 않아요!")
                        else:
                            user[num]['money']+=count*stock[stock_num].cost
                            await msg.channel.send(f"주식 '{name}'을 {count}개 팔았습니다! [남은 돈:{user[num]['money']}{unit}]")
            if(cmd==";modify" and host): 
                if(arg.find("-money")!=-1):
                    target_name=argSplit(arg,"name:")
                    target_value=argSplit(arg,"value:")
                    try:
                        target_num=getNumName(target_name)
                        target_value=int(target_value)
                        if(target_num==None):
                            await msg.channel.send(f"'{target_name}'라는 이름의 데이터가 없어요!")
                        if(arg.find("-help")!=-1 or target_name=="" or target_value==""):
                            await msg.channel.send("**사용법** : $modify -money -[set/add] name:[str] value:[num]")
                        elif(arg.find("-set")!=-1):
                            user[target_num]["money"]=target_value
                            log("Modify Money",f"<Set> {target_name} -> {target_value}{unit}")
                            await msg.channel.send(f"'{target_name}'이라는 유저의 돈을 {target_value}{unit}로 설정했습니다!")
                        elif(arg.find("-add")!=-1):
                            user[target_num]["money"]+=target_value
                            log("Modify Money",f"<Add> {target_name} -> {target_value}{unit}")
                            await msg.channel.send(f"'{target_name}'이라는 유저에게 {target_value}{unit}를 지급했어요! [돈:{user[target_num]['money']}{unit}]")      
                    except ValueError:
                        await msg.channel.send("value는 정수를 써야해요!")
                    
                elif(arg.find("-help")!=-1):
                    await msg.channel.send("**사용법** : $modify -[money]")

              
        Save()

client.run(token)
