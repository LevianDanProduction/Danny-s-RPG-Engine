import random
#from operator import itemgetter
#import copy
#import statusbar
import time
import simpleaudio as sa
import sys
import os

"""
try: color = sys.stdout.shell
except AttributeError: raise RuntimeError("Use IDLE")
"""

class color:
    def write(text, type="stdout",flush=False):
        print(text,end="")
        if flush:
            sys.stdout.flush()

absdirpath = os.path.abspath(os.path.dirname(__file__))
print(absdirpath)
#Game Creator, DannyFramework 1.0
#class, gender, strength/magic/dexterity points, and extra abilities


class s():

    def __init__(self,filename,):
        self.filename = str(absdirpath) + "\\audio\\" + '\\' + filename + ".wav"
        #print(self.filename)
        self.wave_obj = sa.WaveObject.from_wave_file(self.filename)
        self.play_obj = self.wave_obj
    
    def playSound(self,timer=None):
        if timer:
            time.sleep(timer)
        self.play_obj = self.wave_obj.play()
        if not timer == None:
            time.sleep(timer)
        else:
            self.play_obj.wait_done()  # Wait until sound has finished playing

            
    def stopSound(self):
        if self.play_obj.is_playing():
            self.play_obj.stop()
            return True
        else:
            return False
        
    def checkSound(self):
        if self.play_obj.is_playing():
            return True
        else:
            return False


class TargetAI():
    def healingAI(team,move,real,fake): 
        #sort team out by health: lowest first, then slice by the target ammount
        targetlist = []
        for i in real:
            if i.isDead() == False:
                targetlist.append(i)
        targetlist.sort(key=lambda x:x.hp)
        targetlist = targetlist[:move.get('affectammount')]
        return targetlist
    
    def randomAI(team,move,real,fake):
        targetlist = []
        for i in range(move.get('affectammount')):
            while True:
                if False in [x.isDead() for x in real]:
                    if [x.isDead() for x in real].count(False) > 1:
                        decider = random.choice(real)
                        if decider in fake:
                            if decider.isDead() == False:
                                targetlist.append(decider)
                                fake.remove(decider)
                                break
                    elif [x.isDead() for x in real].count(False) <= 1:
                        for i in range(len(real)):
                            if real[i].isDead() == False:
                                targetlist.append(real[i])
                                break
                        break
        return targetlist

class Effect():
    
    def Sleep(attackdmg,target,user,time):

        if time == 3:
            print("ZZZ")
            attacksound = s('debuff')
            attacksound.playSound()
            user.willSkipTurn = True
            target.statustag = " (Sleep)"
            targetfullname = str(target.name + " ")
            print(targetfullname,"was put to sleep.")
                             
        if time > 0 and not time == 3:
            print("ZZZ")
            attacksound = s('debuff')
            attacksound.playSound()
            target.statustag = " (Sleep -> " + str(time) + ")"
            targetfullname = str(target.name + " ")
            print(targetfullname,"is asleep.")
        if time == 0:
            print("Yawn")
            attacksound = s('heal')
            attacksound.playSound()
            user.willSkipTurn = False
            target.statustag = ""
            targetfullname = str(target.name + " ")
            print(targetfullname,"is awake.")

        
    def Bcry(attackdmg,target,user,time):
        if time == 4:
            print("YES!")
            attacksound = s('scare')
            attacksound.playSound()
            user.statApply(Effect.effects[1])
            user.statCheck()
            target.statustag = " (Attack buff Defence debuff Health Buff)"
            targetfullname = str(target.name + " ")
            print(targetfullname,"is ready to rumble.")
        if time > 0 and not time == 4:
            print("YES!")
            attacksound = s('scare')
            attacksound.playSound()
            target.statustag = " (Attack +40﹪ Defence -20﹪ Health +20﹪ -> " + str(time) + ")"
            targetfullname = str(target.name + " ")
            print(targetfullname,"is riled up.")
        if time == 0:
            print("hehe")
            attacksound = s('debuff')
            attacksound.playSound()
            target.statustag = ""
            user.setDefaultStats()
            user.statRemoveAll()
            user.statReApply()
            targetfullname = str(target.name + " ")
            print(targetfullname,"is calm.")

    def Tough(attackdmg,target,user,time):
        if time == 5:
            print("Buff!")
            attacksound = s('scare')
            attacksound.playSound()
            user.statApply(Effect.effects[1])
            user.statCheck()
            target.statustag = " (Defence +50﹪ -> " + str(time) + ")"
            targetfullname = str(target.name + " ")
            print(targetfullname,"is ready to rumble.")
        if time > 0 and not time == 5:
            print("Great!")
            attacksound = s('scare')
            attacksound.playSound()
            target.statustag = " (Defence +50﹪ -> " + str(time) + ")"
            targetfullname = str(target.name + " ")
            print(targetfullname,"is braced for any attack.")
        if time == 0:
            print("phew")
            attacksound = s('debuff')
            attacksound.playSound()
            target.statustag = ""
            user.setDefaultStats()
            user.statRemoveAll()
            user.statReApply()
            targetfullname = str(target.name + " ")
            print(targetfullname,"is relaxed.")
        
                                 
                             

    
    effects =[
        {
        'name': 'Sleep',
        'description': 'ZZZ, makes the enemy sleep for 3 turns',
        'type': 'PassiveSkill',
        'tags': ['skipTurn'],
        'time': 3,
        'damage': 0,
        'function':Sleep,
        'contfunction':Sleep,
        'flags':['SkipTurn']
        
        },{
        'name': 'Battle Cry',
        'description': 'Increase strength,defence and health',
        'type': 'PassiveSkill',
        'tags': ['Buff'],
        'time': 4,
        'damage': 0,
        'function':Bcry,
        'contfunction':Bcry,
        'flags':['Buff'],
        'statchange':[('strength','*',1.4),('defence','*',1.2),('max_hp','*',1.2)] #[('strength','+',30),('defence','-',10),('max_hp','+',500)]
        },{
        'name': 'Toughen Up',
        'description': 'Increase defence',
        'type': 'PassiveSkill',
        'tags': ['Buff'],
        'time': 5,
        'damage': 0,
        'function':Tough,
        'contfunction':Tough,
        'flags':['Buff'],
        'statchange':[('defence','*',1.5)] #[('strength','+',30),('defence','-',10),('max_hp','+',500)]
        }
        ]
    

class Skill():
    
    def Attack(attackdmg,targetnumber,target,user):
        print("")
        print("POW!")
        attacksound = s('attack')
        attacksound.playSound()
        finaldamage = attackdmg * (user.strength/2)
        finaldamage = round(finaldamage)
        finaldamage = int(finaldamage * (0.97**target.defence))
        target.takeDamage(finaldamage)
        #print (targetnumber)
        targetfullname = str(target.name + " " + str(targetnumber+1))
        print(targetfullname,"lost",finaldamage,"health")
        
    def Bash(attackdmg,targetnumber,target,user):
        print("")
        print("BOSH!")
        attacksound = s('attack')
        attacksound.playSound()
        finaldamage = attackdmg * (user.strength/1.9)
        finaldamage = round(finaldamage)
        finaldamage = int(finaldamage * (0.97**target.defence))
        target.takeDamage(finaldamage)
        #print (targetnumber)
        targetfullname = str(target.name + " " + str(targetnumber+1))
        print(targetfullname,"lost",finaldamage,"health")
        time.sleep(0.2)
        if random.randint(1,100) < 40:
            print(user.name + " was able to hit of a crit!")
            time.sleep(0.4)
            finaldamage = attackdmg * (user.strength/4)
            finaldamage = round(finaldamage)
            finaldamage = int(finaldamage * (0.97**target.defence))
            target.takeDamage(finaldamage)
            print(targetfullname,"lost",finaldamage,"health")

    def Heal(attackdmg,targetnumber,target,user):
        print("")
        attacksound = s('heal')
        attacksound.playSound()
        print("Ahh")
        finaldamage = attackdmg * (user.intellect/5)
        finaldamage = round(-finaldamage)
        targetfullname = str(target.name + " " + str(targetnumber+1))
        target.giveHealth(finaldamage)
        print(targetfullname,"gained",finaldamage,"health")

    def Cleave(attackdmg,targetnumber,target,user):
        print("")
        print("Slash!")
        attacksound = s('cleave')
        attacksound.playSound()
        finaldamage = attackdmg * (user.strength/2)
        finaldamage = round(finaldamage)
        finaldamage = int(finaldamage * (0.95**target.defence))
        target.takeDamage(finaldamage)
        #print (targetnumber)
        targetfullname = str(target.name + " " + str(targetnumber+1))
        print(targetfullname,"lost",finaldamage,"health")
        
    def Zap (attackdmg,targetnumber,target,user):
        print("")
        print("Zip!")
        attacksound = s('blast')
        attacksound.playSound()
        finaldamage = attackdmg * (user.intellect/3)
        finaldamage = round(finaldamage)
        finaldamage = int(finaldamage * (0.95**target.magic_defence))
        target.takeDamage(finaldamage)
        #print (targetnumber)
        targetfullname = str(target.name + " " + str(targetnumber+1))
        print(targetfullname,"lost",finaldamage,"health")

    def Lullaby (attackdmg,targetnumber,target,user):
        print("")
        print("La la la...")
        attacksound = s('song')
        attacksound.playSound()
        target.giveState(Effect.effects[0],target)
        #print (targetnumber)
        targetfullname = str(target.name + " " + str(targetnumber+1))
        print(targetfullname,"took a sleepy spell.")

    def Bcry(attackdmg,targetnumber,target,user):
        print("")
        print("HEHEHE!")
        attacksound = s('ouchie')
        attacksound.playSound()
        target.giveState(Effect.effects[1],target)
        #print (targetnumber)
        targetfullname = str(target.name + " " + str(targetnumber+1))
        print(targetfullname," s ready to rumble.")

    def Tough(attackdmg,targetnumber,target,user):
        print("")
        print("Hugh!")
        attacksound = s('ouchie')
        attacksound.playSound()
        target.giveState(Effect.effects[2],target)
        #print (targetnumber)
        targetfullname = str(target.name + " " + str(targetnumber+1))
        print(targetfullname," s all toughened up.")
        
        

    skills =[
        {
        'name': 'Attack',
        'description': 'Basic Attack',
        'type': 'ActiveSkill',
        'affects': 'target',
        'affectammount':1,
        'damage': 10,
        'damage-type': ['melee'],
        'cooldown': 0,
        'mp-cost': 0,
        'chance':94,
        'function': Attack,
        'EAI': TargetAI.randomAI
        },
        {
        'name':'Heal',
        'description': 'Gain 30 health',
        'type': 'StatusSkill',
        'affects': 'team', # possible = target, user, team
        'affectammount':1,
        'damage': -30,
        'damage-type': ['heal'],
        'cooldown': 0,
        'mp-cost': 20,
        'chance':100,
        'function': Heal,
        'EAI': TargetAI.healingAI
        },
        {
        'name': 'Cleave',
        'description': 'Wide attack',
        'type': 'ActiveSkill',
        'affects': 'target',
        'affectammount':2,
        'damage': 5,
        'damage-type': ['melee'],
        'cooldown': 0,
        'mp-cost': 5,
        'chance':85,
        'function': Cleave,
        'EAI': TargetAI.randomAI
        },
        {
        'name': 'Zap',
        'description': 'Small magic bolt of electricity',
        'type': 'ActiveSkill',
        'affects': 'target',
        'affectammount':1,
        'damage': 50,
        'damage-type': ['magic'],
        'cooldown': 0,
        'mp-cost': 200,
        'chance':90,
        'function': Zap,
        'EAI': TargetAI.randomAI
        },
        {
        'name': 'Lullaby',
        'description': 'Sleeping Song',
        'type': 'StatusSkill',
        'affects': 'target',
        'affectammount':1,
        'damage': 0,
        'damage-type': ['magic'],
        'cooldown': 0,
        'mp-cost': 80,
        'chance':70,
        'function': Lullaby,
        'EAI': TargetAI.randomAI
        },{
        'name': 'Battle Cry',
        'description': 'Attack Song, +40﹪ attack, -20﹪ defence, +20﹪ health for 4 turns',
        'type': 'StatusSkill',
        'affects': 'user',
        'affectammount':1,
        'damage': 0,
        'damage-type': ['melee'],
        'cooldown': 0,
        'mp-cost': 100,
        'chance':100,
        'function': Bcry,
        'EAI': TargetAI.randomAI
        },{
        'name': 'Bash',
        'description': 'Bashes into the target',
        'type': 'ActiveSkill',
        'affects': 'target',
        'affectammount':1,
        'damage': 12,
        'damage-type': ['melee'],
        'cooldown': 0,
        'mp-cost': 0,
        'chance':90,
        'function': Bash,
        'EAI': TargetAI.randomAI
        },{
        'name': 'Toughen Up',
        'description': 'Braces for impact 50﹪ defence for 3 turns', 
        'type': 'StatusSkill',
        'affects': 'user',
        'affectammount':1,
        'damage': 0,
        'damage-type': ['melee'],
        'cooldown': 0,
        'mp-cost': 100,
        'chance':100,
        'function': Tough,
        'EAI': TargetAI.randomAI
        }
        ]

        

class Item():

    def HealthPotion(attackdmg,targetnumber,target,user):
        print("")
        attacksound = s('heal1.0')
        attacksound.playSound(0.2)
        attacksound2 = s('heal')
        attacksound2.playSound()
        print("Glug Glug!")
        finaldamage = attackdmg 
        finaldamage = round(-finaldamage)
        targetfullname = str(target.name + " " + str(targetnumber+1))
        target.giveHealth(finaldamage)
        target.healthBar(20,"Normal",0.06)
        print(targetfullname,"gained",finaldamage,"health")
        
    def ManaPotion(attackdmg,targetnumber,target,user):
        print("")
        attacksound = s('heal1.0')
        attacksound.playSound(0.2)
        attacksound2 = s('mana')
        attacksound2.playSound()
        print("Glug Glug!")
        finaldamage = attackdmg 
        finaldamage = round(-finaldamage)
        targetfullname = str(target.name + " " + str(targetnumber+1))
        target.giveMagic(finaldamage)
        target.healthBar(15,"MP",0.06)
        print(targetfullname,"gained",finaldamage,"Magic Points")

    
    items = [{
        'name': 'Health Potion',
        'description': 'Regain 50 Health',
        'type': 'Item',
        'tags': ['destroy-on-use'],
        'target': 'team',
        'affectammount':1,
        'damage': -150,   # negative damage is health gain
        'inventory-space': 1,
        'order':1,
        'function':HealthPotion
        },{
        'name': 'Magic Potion',
        'description': 'Regain 50 MP',
        'type': 'Item',
        'tags': ['destroy-on-use'],
        'target': 'team',
        'affectammount':1,
        'damage': -150,   # negative damage is mana gain
        'inventory-space': 1,
        'order':1,
        'function':ManaPotion
        },{
        'name': 'Leather Cap',
        'description': 'Worn out Cap',
        'type': 'Gear',
        'tags': ['equip'],
        'slot':'head',
        'inventory-space': 1,
        'order':3,
        'statchange':[('max_hp','+',100),('defence','+',2)]
        },
        ]

class ClassID():
    id1 = [
        {
        'name':'Mage',
        'highestGrowth':'intellect',
        'lowestGrowth':'strength',
        'startingSkills':[ Skill.skills[1] , Skill.skills[3] ]
        },{
        'name':'Warrior',
        'highestGrowth':'strength',
        'lowestGrowth':'intellect',
        'startingSkills':[Skill.skills[2] , Skill.skills[4] , Skill.skills[5]]
        },{
        'name':'Paladin',
        'highestGrowth':'strength',
        'lowestGrowth':'dex',
        'startingSkills':[Skill.skills[6] , Skill.skills[7]]
        }
        ]


        
        
    classes = {
        'Mage':id1[0],
        'Warrior':id1[1],
        'Paladin':id1[2],
        'checked':False
        }

class Character():
    state = None
    startEffect = None

    

    def __init__(self,name,gender):
        self.name = name
        self.gender = gender
        self.hp = 100
        self.mp = 100
        self.defence = 5
        self.magic_defence = 5
        self.speed = 5
        self.damage = 0
        self.inventory = []
        self.lvl = 1
        self.targetlist = []
        self.currentSkill = 0
        self.attacksound = 0
        self.tag = ""
        self.statustag = ""
        self.max_inventory = 999
        self.current_inventory = 0
        self.optionlist = []
        self.statesList = []
                        

#uses - what i can change about character
        
#---battle
    def checkForSkill(self,chosenSkill):
        self.trueSkill = False
        for i in Skill.skills:
            if i.get('name') == chosenSkill:
                self.currentSkill = i.copy()
                self.trueSkill = True
                #print("valid - can find move in database")
        if self.trueSkill == False:
            print("invalid - cant find move in database")
            self.currentSkill = i.copy()
        #print(self.currentSkill)

    def checkForItem(self,chosenItem):
        self.trueItem = False
        for i in Item.items:
            if i.get('name') == chosenItem:
                self.currentItem = i.copy()
                self.trueItem = True
                #print("valid - can find move in database")
        if self.trueItem == False:
            print("invalid - cant find move in database")
            self.currentItem = i.copy()
        #print(self.currentSkill)
        
    def autopickTarget(self,targetGroup,targetAmmount,use="skill"):
        
        self.clearTargets()
        print("Here are your choices:\n")
        for i in range (0,len(targetGroup)):
            if targetGroup[i].isDead() == False:
                print("\n>>> ",targetGroup[i].statustag,targetGroup[i].tag + targetGroup[i].name , str(i+1))
                self.optionlist.append(str(i+1))
    
                if targetGroup[i].tag == "Boss ":
                    targetGroup[i].healthBar(35,colour="Normal")
                else:
                    targetGroup[i].healthBar(20,colour="Normal")
                if not isinstance(targetGroup[i],Enemy) == True:
                    targetGroup[i].healthBar(15,colour="MP")
                    
        if use == "skill":            
            self.rounds =  self.currentSkill.get('affectammount')
        elif use == "item":
            self.rounds =  self.currentItem.get('affectammount')
        
        for i in range (targetAmmount):
            if targetAmmount > 1 and i > 0:
                self.choice = input("\nwhat other target do you want to choose?(give a number starting from 1)")
            else:    
                self.choice = input("\nwhich target do you want to choose?(give a number starting from 1)")
            self.attacksound = s('choose')
            self.attacksound.playSound(0.01)
            
            if str(self.choice) == "":
                self.choice = ""
                break
            if self.optionlist.count(self.choice) == 0:
                self.choice = ""
                break
            if int(self.choice) <= 0:
                self.choice = ""
                break
            if type(eval(self.choice)) == float:
                self.choice = ""
                break
            if self.choice == "" or self.choice == None or targetGroup[(int(self.choice)-1)].isDead() == True:
                self.choice = ""
                break
                                      
                                         
            self.choice = int(self.choice)
            self.choice = targetGroup[self.choice-1]
            self.pickTarget(self.choice)
            if i == targetAmmount:
                break
            if len(self.targetlist) == self.rounds:
                break
            if i == self.rounds:
                break

            
        if len(self.targetlist) >= self.rounds:
            return True
        if len(self.targetlist) == self.rounds:
            return True
        elif self.choice == "" :
            return False
        self.attacksound = s('back')
        self.attacksound.playSound(0.01)  
        #print(self.targetlist)

                                
    def pickTarget(self,target):
        if not target.isDead():
            self.targetlist.append(target)
        else:
            pass

    def clearTargets(self):
        self.targetlist = []
        
    def useSkill(self,user,targetgroup,position=-1):
        #print(targetgroup)
        self.lineposition = position
        if self.lineposition == -1:
            self.lineposition = ""
        else:
            self.lineposition = self.lineposition + 1
        if self.missCalculator(self.currentSkill) == True:
            for i in range(len(self.targetlist)):
                #print(i)
                print(user.name,str(self.lineposition),"used",self.currentSkill['name'],"on",self.targetlist[i].name)
                #print(self.targetlist[i].name)
                #print(self.targetlist[i].name)
                #print(targetgroup.index(self.targetlist[i]))
                print("")
                if self.currentSkill.get('mp-cost') > 0:
                    self.mp = self.mp - self.currentSkill.get('mp-cost')
                    if self.mp < 0:
                        self.mp = 0
                    user.healthBar(15,"MP",0.015)    
                
                self.currentSkill['function'](self.currentSkill['damage'],targetgroup.index(self.targetlist[i]),self.targetlist[i],self)
                self.targetlist[i].healthBar(20,"Normal",0.06)
                print("")
                if self.targetlist[i].isDead() == True:
                    print(str(self.targetlist[i].name),str(targetgroup.index(self.targetlist[i])+1),"was defeated")
                else:
                    pass
            
        else:
            print("But",user.name,"missed!")
            self.attacksound = s('miss')
            self.attacksound.playSound()  
        self.clearTargets()
        #print("skill done")


    def missCalculator(self,skillUsed):
        miss = random.randint(1,100)
        misschance = 100 - skillUsed['chance']
        if miss <= misschance:
            return False
        else:
            return True
    
    def giveHealth(self,ammount):
        self.hp += ammount
        if self.hp > self.max_hp:
            self.hp = self.max_hp
    def setHealth(self,ammount):
        self.hp = ammount
        if self.hp > self.max_hp:
            self.hp = self.max_hp
    
    def giveMagic(self,ammount):
        self.mp += ammount
        if self.mp > self.max_mp:
            self.mp = self.max_mp
    def setMagic(self,ammount):
        self.mp = ammount
        if self.mp > self.max_mp:
            self.mp = self.max_mp
            
    def fullRecover(self):
        self.hp = self.max_hp
        self.mp = self.max_mp
        
    def fleeBattle(self,usergroup,enemygroup):
        self.totalteamlevel = 0
        self.totalenemylevel = 0
        for i in usergroup:
            self.totalteamlevel += i.lvl
        for i in enemygroup:
            self.totalenemylevel += i.lvl
        self.totalteamlevel *= 2    
        self.totalganglvl = self.totalteamlevel + round(self.totalenemylevel/2)
        miss = random.randint(1,100)
        misschance = self.totalganglvl - self.totalenemylevel
        if miss <= misschance:
            print("\nEscape Sucsessful\n\n")
            return False 
        else:
            print("\nEscape Unsuccsessful\n\n")
            return True
            
        
    
    def takeDamage(self,damage):
        self.hp -= damage
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        if self.hp < 0:
            self.hp = 0

    def partyAliveCount(self,team):
        self.partycounter = 0
        for i in range(len(team)):
            if team[i].isDead() == False:
                self.partycounter += 1
        print(">>>",self.partycounter)
        
        return self.partycounter



    def healthBar(self,barPoint=30,colour="Normal",speed = 0.001):
        barPoint = barPoint
        if colour == "MP":
            self.barPercentage = self.mp/self.max_mp
        else:
            self.barPercentage = self.hp/self.max_hp
            
        self.barPercent = int(self.barPercentage*barPoint)
        self.barDisplay = int(self.barPercentage*100)
        color.write(" |","SYNC")
        self.attacksound = s('bar')
        for i in range(barPoint):
            time.sleep(speed)
            if (i % 4) == 0:
                self.attacksound.playSound(0.005)  
            if i >= barPoint-self.barPercent:
                if colour == "Normal":
                    color.write("\033[32m■\033[0m","STRING",flush=True)
                if colour == "MP":
                    color.write("\033[34m■\033[0m","stdout",flush=True)
            else:
                if colour == "Normal":
                    color.write("\033[31m□\033[0m","COMMENT",flush=True)
                if colour == "MP":
                    color.write("□","COMMENT",flush=True)
            
        color.write("|  ","SYNC")
        if self.hp < int(self.max_hp/3):
            color.write(str(self.barDisplay),"COMMENT")
            color.write("%\n\n","SYNC")
        else:
            if colour == "MP":
                color.write(str(self.barDisplay),"stdout")
            else:
                color.write(str(self.barDisplay),"STRING")
            color.write("%\n\n","SYNC")
        

#---items    
    def useItem(self,item):
        self.checkForItem(self,item)

        if item.get("target") == "team":
            self.oneAutoTarget = self.autopickTarget(team,self.inventory[self.choice].get("affectammount"),"item")
            
        elif item.get("target") == "user":
            self.oneAutoTarget = self.pickTarget(self)
                
        elif item.get("target") == "target":
            self.oneAutoTarget = self.autopickTarget(opposition,self.inventory[self.choice].get("affectammount"),"item")
            
#-------------------------------------------

        if item.get("target") == "team":
            self.useItemb(self,team)
            
        elif item.get("target") == "user":
            self.useItemb(team,self)
            
        elif item.get("target") == "target":
            self.useItemb(self,opposition)
        
        self.consumeItem()
        
    def gainItem(self,item,quantity):
        for i in range(quantity):
            self.inventory.append(item)
        
    
    def removeItem(self,item,quantity):
        for i in range(quantity):
            if self.inventory.count(item) > 0:
                self.inventory.remove(item)
        
    def sortItems(self):
        pass
    
    def consumeItem(self,target=None):
        if target == None:
            target = self.currentItem
        if self.currentItem.get('tags').count('destroy-on-use') > 0:
            self.inventory.remove(target)

    def useItemb(self,user,targetgroup,position=-1):
        #print(targetgroup)
        self.lineposition = position
        if self.lineposition == -1:
            self.lineposition = ""
        else:
            self.lineposition = self.lineposition + 1
            
        for i in range(len(self.targetlist)):
            #print(i)
            print(user.name,str(self.lineposition),"used",self.currentItem['name'],"on",self.targetlist[i].name)
            #print(self.targetlist[i].name)
            #print(self.targetlist[i].name)
            #print(targetgroup.index(self.targetlist[i]))
            print("")   
            
            self.currentItem['function'](self.currentItem['damage'],targetgroup.index(self.targetlist[i]),self.targetlist[i],self)
            print("")
            if self.targetlist[i].isDead() == True:
                print(str(self.targetlist[i].name),str(targetgroup.index(self.targetlist[i])+1),"was defeated")
        self.clearTargets()
        self.consumeItem()
        
                    


#checks - to check whether a character is doing something i want
    def isThereStartingStatus(self):
        pass
    
    def isDead(self):
        if self.hp <= 0:
            self.hp = 0
            return True
        else:
            return False
        
    def sumInventory(self):
        self.current_inventory = 0
        for i in range(len(self.inventory)):
            self.current_inventory += self.inventory[i].get('inventory-space')
        return self.current_inventory
    
    def organiseInventory(self,query):
        if query == "battle":
            self.inventory.sort(key=lambda x:x.get('order'))
            return self.inventory
            
        

class Player(Character):

    class StatusRunner():

        def __init__(self,state,user):
            self.name = state.get('name')
            self.effect = state
            self.effectFunction = state.get('function')
            self.contFunction = state.get('contfunction')
            self.counter = state.get('time')
            self.effectFunction(self.effect['damage'],user,user,self.counter)
            self.flag = self.effect.get('flags')
            self.user = user
            #print(">>>>>>>>>>>> flag is " + str(self.flag))
            

        def effectCheck(self,flag):
            if self.counter <= 0:
                #print(self.effect)
                #print("deleted here")
                self.user.statesList.remove(self)
                self.contFunction(self.effect['damage'],self.user,self.user,self.counter)
                del self
                return
                
            elif len(self.flag) > 0:
                if 'SkipTurn' in flag:
                    self.counter -= 1
                    color.write("________________________________________________________________________________________\n\n","KEYWORRD")
                    self.contFunction(self.effect['damage'],self.user,self.user,self.counter)
                    color.write("\n\n________________________________________________________________________________________\n\n","stderr")
                    return True
                elif "Buff" in flag:
                    self.counter -= 1
                    color.write("________________________________________________________________________________________\n\n","KEYWORRD")
                    self.contFunction(self.effect['damage'],self.user,self.user,self.counter)
                    color.write("\n\n________________________________________________________________________________________\n\n","stderr")
                    return True
                    
                    
                elif flag == 'RandomTarget':
                    pass
                elif flag == 'TurnDamage':
                    pass
            else:
                return False
        
                

        
    
    class StatsChange():
        def __init__(self):
            self.body = {
                'head':'',
                'body':'',
                'legs':'',
                'boots':'',
                'weapon':'',
                'accessories':''
                }
            self.stats = {
                'extra_max_hp':[],
                'extra_max_mp':[],
                'extra_strength':[],
                'extra_dex':[],
                'extra_intellect':[],
                'extra_defence':[],
                'extra_magic_defence':[],
                'extra_speed':[]
                }
            self.statsSave = {
                'max_hp':[],
                'max_mp':[],
                'strength':[],
                'dex':[],
                'intellect':[],
                'defence':[],
                'magic_defence':[],
                'speed':[]
                }


    expCap = 100
    lvlCap = 100
    
    def __init__(self,name,gender,Class,tag=""):
        super().__init__(name,gender)
        self.lvl = 1
        self.exp = 0
        self.name = name
        self.gender = gender
        self.Class = Class #class
        self.hp = 0
        self.mp = 0
        self.max_hp = 0 #health points
        self.max_mp = 0 #magic points
        self.strength = 0 # strength
        self.dex = 0 # dexterity
        self.intellect = 0 # intellegence
        multi_level = {}
        self.tag = tag
        self.statesList = []

        #condition switches
        self.willSkipTurn = False
        self.willRandomTarget = False
        self.willTakeTurnDamage = False

        self.max_hp = 100
        self.max_mp = 100
        self.hp = self.max_hp
        self.mp = self.max_mp
        self.strength = 5
        self.dex = 5
        self.intellect = 5
        self.inventory = [Item.items[1]]
        self.max_inventory = 10
        self.current_inventory = self.sumInventory()
        self.gainItem(Item.items[0],3)
        self.gainItem(Item.items[1],4)
        self.gainItem(Item.items[2],1)
        self.StatsChanger = self.StatsChange()
        
        if not isinstance(self,Enemy) == True:
            self.class_system = ClassID.classes.get(Class)
            self.skills = self.class_system.get('startingSkills')
            self.setInitialStats()
            self.stat_change()
           

    def removeState(self,stateid):
        pass

    def giveState(self,stateid,target):
        #print(self.statesList)
        self.statesList.append(self.StatusRunner(stateid,target))
        #print(self.statesList)

    def checkAllStates(self):
        self.cstatcount = 0
        if len(self.statesList) > 0:
            for i in self.statesList:
                #print(self.statesList)
                #print(i)
                self.checkedallstates = i.effectCheck(i.flag)
                if self.checkedallstates == True:
                    self.cstatcount =+ 1
        if self.cstatcount > 0:
            return True
        else:
            return False
    
    #statchecker 'statchange':[('hp','+',100),('defence','+',2)]

    def statApply(self,applicant):
        self.stat_ri = applicant.get('statchange')
        self.stat_ri_applier = 0
        self.statdirectory = self.StatsChanger.stats
        for i in range(len(self.stat_ri)):
            for j in range(3):
                if j == 0:
                    self.stat_ri_applier = self.statdirectory['extra_'+ str(self.stat_ri[i][0])] 
                    print()
                    self.stat_r_applier = self.stat_ri[i][j]
                    self.statkeyer = 'extra_'+ str(self.stat_ri[i][0])
                if j == 1:
                    self.stat_ri_type = self.stat_ri[i][j]
                if j == 2:
                    self.new_stat_r = getattr(self, self.stat_r_applier)
                    self.new_stat_ri = getattr(self, self.stat_r_applier)
                    
                    if self.stat_ri_type == '+':
                        self.new_stat_r += self.stat_ri[i][j]
                    if self.stat_ri_type == '-':
                        self.new_stat_r -= self.stat_ri[i][j]
                    if self.stat_ri_type == '*':
                        self.new_stat_r *= self.stat_ri[i][j]
                    if self.stat_ri_type == '/':
                        self.new_stat_r /= self.stat_ri[i][j]

                    #print(self.statdirectory)
                    #print(self.statkeyer)
                    #print(self.statdirectory[self.statkeyer])
                    self.official_changer = -1*(self.new_stat_ri - self.new_stat_r)

                    self.statdirectory[self.statkeyer].append((self.official_changer, applicant,False))
                    
                        
         
        
    
    def statCheck(self,remover=False):
        for x in self.StatsChanger.stats:
            self.stat_ineedtochange = x[6:len(x)]
            
            if self.StatsChanger.stats[x] == [] or remover == True:
                setattr(self,self.stat_ineedtochange,self.StatsChanger.statsSave.get(self.stat_ineedtochange))
            else:
                for i in range(len(self.StatsChanger.stats[x])):
                    if self.StatsChanger.stats[x][i][2] == False:
                        #print(self.StatsChanger.stats[x][i][2])
                        #print(">>",getattr(self,self.stat_ineedtochange))
                        #print("...",self.StatsChanger.stats[x][i][0])
                        self.finalStatChange = self.StatsChanger.stats[x][i][0] + int(getattr(self,self.stat_ineedtochange))
                        #if self.StatsChanger.statsSave[self.stat_ineedtochange] == getattr(self, self.stat_ineedtochange):
                        setattr(self,self.stat_ineedtochange,self.finalStatChange)
                        self.L2L2 = list(self.StatsChanger.stats[x][i])
                        self.L2L2[2] = True
                        self.StatsChanger.stats[x][i] = self.L2L2
                        
        
    def statRemoveAll(self):
        self.setDefaultStats()
        for x in self.StatsChanger.stats:
            self.StatsChanger.stats[x] = []

    def statRemoveByItem(self,item):
        for x in self.StatsChanger.stats: #max hp 
            for y in range(len(self.StatsChanger.stats[x])): #1 (0)
                for z in range(len(self.StatsChanger.stats[x][y])): #0,2 
                    if z == 1:
                        if self.StatsChanger.stats[x][y][z] == item:
                            self.StatsChanger.stats[x].remove(self.StatsChanger.stats[x][y])
                            
                        
        

    def statReApply(self):
        for x in self.StatsChanger.body:
            try:
                self.equipGear(self.StatsChanger.body[x])
            except:
                pass
        for y in self.statesList:
            if 'statchange' in y.effect:
                self.statApply(y.effect)
                self.statCheck()

    def setDefaultStats(self):
        for x in self.StatsChanger.statsSave:
            setattr(self,x,self.StatsChanger.statsSave[x])

    def setInitialStats(self):
        for x in self.StatsChanger.statsSave:
            self.StatsChanger.statsSave[x] = getattr(self,x)
            
                        
    #---gear    
    def equipGear(self,gear):
        if not gear == "":
            self.removeItem(gear,1)
            if not self.StatsChanger.body[(gear.get('slot'))] == '':
                self.unequip(self.StatsChanger.body[(gear.get('slot'))])
            self.StatsChanger.body[(gear.get('slot'))] = gear
            self.statApply(gear)
            self.statCheck()
        
    
    def unequipGear(self,gearSlot):
        self.currentDegear = self.StatsChanger.body.get(gearSlot)
        self.setDefaultStats()
        self.gainItem(self.currentDegear,1)
        self.currentDegear = []
        self.statRemoveAll()
        self.statReApply()

        print("max hp: ",self.max_hp)
        print("defence: ",self.defence)
        





    
            
    def level_up(self):
        if self.exp >= self.expCap and self.lvl < self.lvlCap:
            self.lvl += 1
            self.exp = self.exp - self.expCap
            if self.exp < 0:
                self.exp = 0
            self.expCap *= 1.225
            self.expCap = int(self.expCap)
            self.stat_change()
            print("")
            print('hp:',"%d/%d" % (self.hp,self.max_hp))
            print('mp:',"%d/%d" % (self.mp,self.max_mp))
            print('str:',self.strength)
            print('int:',self.intellect)
            print('dex:',self.dex)
            print("")
            return True
        else:
            return False

    def gain_exp(self, exp):
        self.exp += exp
        print(self.name + " gained %d XP" % exp)
        if self.level_up():
            if self.exp >= self.expCap:
                while self.exp >= self.expCap:
                    self.level_up()
            print("Congratulations,",self.name,"leveled up!\nYour current level is %d\n" % self.lvl)
            self.attacksound = s('levelup')
            self.attacksound.playSound()  
            print(self.name + "'s current XP is %d/%d\n" % (self.exp, self.expCap))
            print(self.name + "'s current HP is %d/%d\n" % (self.hp, self.max_hp))
        else:
            print(self.name + "'s current XP is %d/%d\n" % (self.exp, self.expCap))
            if self.exp >= self.expCap:
                while self.exp >= self.expCap:
                    self.level_up()

    def stat_change(self):
        #print(self.StatsChanger.statsSave)
        if ClassID.classes['checked'] == False:
            self.class_system = ClassID.classes.get(self.Class)
            self.hgrow = self.class_system.get('highestGrowth')
            self.lgrow = self.class_system.get('lowestGrowth')

        self.statRemoveAll()
        self.setDefaultStats()
#level up base increase
        self.intellect += random.randint(2,4)
        self.strength += random.randint(2,4)
        self.dex += random.randint(2,4)
        self.max_hp *= 1 + (random.randint(400,600)/2000)
        self.max_hp = round(self.max_hp)
        self.max_mp += random.randint(5,15)
        self.magic_defence += random.randint(1,2)
        self.defence += random.randint(1,2)
        self.speed += random.randint(1,2)
#level up class increase
        if self.hgrow == "intellect":
            self.intellect += random.randint(2,4)
            self.max_mp += random.randint(10,20)
            self.magic_defence += random.randint(3,5)
        elif self.lgrow == "intellect":
            self.strength -= random.randint(0,2)
            self.magic_defence -= random.randint(0,2)

        if self.hgrow == "strength":
            self.strength += random.randint(2,4)
            self.max_hp += random.randint(10,20)
            self.defence += random.randint(3,5)
        elif self.lgrow == "strength":
            self.intellect -= random.randint(0,3)
            self.defence -= random.randint(0,1)

        if self.hgrow == "dex":
            self.dex += random.randint(3,6)
            self.max_hp += random.randint(10,15)
        elif self.lgrow == "dex":
            self.dex -= random.randint(0,2)
            self.defence -= random.randint(0,1)

        self.setInitialStats()
        self.statReApply()
            
    def battleMenu(self,opposition,team,activated=True):
        if self.isDead() == True:
            pass
        elif self.willSkipTurn == True:
            pass
        else:
            while True:
                print("\n It's " + self.name +"'s turn")
                color.write("________________________________________________________________________________________\n\n","SYNC")
                color.write(str(self.name),"stdout")
                if not self.statustag == "":
                    color.write(" " + self.statustag,"stdout")
                color.write("   LVL: ","TODO")
                color.write(str(self.lvl),"stdout")
                print("")
                print("  HP : %d/%d" % (self.hp, self.max_hp))
                self.healthBar()
                print("  MP : %d/%d" % (self.mp, self.max_mp))
                self.healthBar(25,"MP")
                color.write("\n________________________________________________________________________________________\n","SYNC")
                print("\n     What would you like to do?")
                color.write(" 1:Attack\n","console")
                color.write(" 2:Skill\n","console")
                color.write(" 3:Items\n","console")
                color.write(" 4:Flee\n\n","console")
                color.write("________________________________________________________________________________________\n\n","SYNC")
                self.choice = input(">>>>:")
                self.attacksound = s('choose')
                self.attacksound.playSound(0.01)
                color.write("________________________________________________________________________________________\n","SYNC")

                if self.choice == "1": #ATTACK
                    #print("targetgroup: ",opposition[0].name)
                    self.checkForSkill('Attack')
                    
                    self.oneAutoTarget = self.autopickTarget(opposition,1)
                    
                    color.write("________________________________________________________________________________________\n\n","SYNC")
                    if self.oneAutoTarget == False:
                        pass
                    elif self.oneAutoTarget == True:
                        color.write("________________________________________________________________________________________\n\n","stderr")
                        self.currentSkill = Skill.skills[0].copy()
                        self.useSkill(self,opposition)
                        color.write("________________________________________________________________________________________\n\n","stderr")
                        break
                if self.choice == "2": #SKILL
                    self.optionlist = []
                    color.write("\n________________________________________________________________________________________\n","SYNC")
                    print("\n     What skill would you like to use? - type the number and write a D next to it for a\n full description\n")
                    for i in range(0,len(self.skills)):
                        self.skillnamer = (" " + str(self.skills.index(self.skills[i])+1)+ ": " + str(self.skills[i].get("name")))
                        color.write(str(self.skillnamer),"console")
                        
                        if self.mp < self.skills[i].get("mp-cost"):
                            color.write("    MP:" +"   " + str(self.skills[i].get("mp-cost")),"stdout")
                        else:
                            color.write("    MP:" +"   " + str(self.skills[i].get("mp-cost")),"stdout")
                        print("")
                        self.optionlist.append(str(self.skills.index(self.skills[i])+1))
                            
                    color.write("\n\n________________________________________________________________________________________\n","SYNC")                                      
                    self.choice = input("\n\n\n>>>>:")

                    if self.choice == "":
                        pass
                    
                    elif self.optionlist.count(self.choice) == 0:
                        self.choice = ""

                    elif len(self.skills) < int(self.choice):
                        self.choice = ""
                    
                    elif not type(eval(self.choice)) == int:
                        self.choice = ""
                    
                    elif str(self.choice) == "":
                        self.choice = ""
                
                    elif int(self.choice) <= 0:
                        self.choice = ""

                    if self.choice == "":
                        pass
                    else:
                        self.attacksound = s('choose')
                        self.attacksound.playSound(0.01)  
                        self.choice = int(self.choice)
                        self.choice = self.choice - 1
                        #print(self.choice)
                        color.write("________________________________________________________________________________________\n","SYNC")
                        self.choiceref = self.choice
                        self.checkForSkill(self.skills[self.choice].get("name"))
                        if self.skills[self.choiceref].get('mp-cost') > self.mp:
                            print("Not enough MP to use this skill")
                            pass
                        else:
                            if self.skills[self.choiceref].get("affects") == "team":
                                self.oneAutoTarget = self.autopickTarget(team,self.skills[self.choice].get("affectammount"))
                                
                            elif self.skills[self.choiceref].get("affects") == "user":
                                self.oneAutoTarget = self.pickTarget(self)
                                self.oneAutoTarget == True
                                
                            elif self.skills[self.choiceref].get("affects") == "target":
                                self.oneAutoTarget = self.autopickTarget(opposition,self.skills[self.choice].get("affectammount"))

                                
                            if self.oneAutoTarget == False:
                                pass
                            elif self.oneAutoTarget == True:
                                color.write("________________________________________________________________________________________\n\n","stderr")
                                #print(self.choice)
                                self.currentSkill = self.skills[self.choiceref]
                            if self.skills[self.choiceref].get("affects") == "team":
                                self.useSkill(self,team)
                            elif self.skills[self.choiceref].get("affects") == "user":
                                self.useSkill(self,team)
                            elif self.skills[self.choiceref].get("affects") == "target":
                                self.useSkill(self,opposition)
                                color.write("________________________________________________________________________________________\n\n","stderr")
                                return   
                        
                if self.choice == "3": #ITEM
                    self.organiseInventory("battle")
                    #for i in range(len(self.inventory)):
                        #print(self.inventory[i].get('name'))
                    color.write("\n________________________________________________________________________________________\n","SYNC")
                    self.choicelist = []
                    self.optionlist = []
                    print("\n     What item would you like to use? - type the number and write a D next to it for a\n full description\n")
                    
                    for i in range(len(self.inventory)):
                        
                        if self.inventory[i] in self.choicelist:
                            break
                        if not self.inventory[i].get('order') == 1:
                            break
                        
                        self.itemnamer = (" " + str(self.inventory.index(self.inventory[i])+1)+ ": " + str(self.inventory[i].get("name")))
                        color.write(str(self.itemnamer),"console")
                        color.write("    Quantity:" +"   " + str(self.inventory.count(self.inventory[i])),"stdout")
                        print("")
                        
                        self.optionlist.append(str(self.inventory.index(self.inventory[i])+1))
                        
                        if self.choicelist.count(self.inventory[i]) == 0:
                            self.choicelist.append(self.inventory[i].copy())
                        
                            
                    color.write("\n\n________________________________________________________________________________________\n","SYNC")                                      
                    self.choice = input("\n\n\n>>>>:")

                    if self.choice == "":
                        self.choice = ""
                        
                    if self.optionlist.count(self.choice) == 0:
                        self.choice = ""
                    
                    elif not type(eval(self.choice)) == int:
                        self.choice = ""
                    
                    elif str(self.choice) == "":
                        self.choice = ""
                
                    elif int(self.choice) <= 0:
                        self.choice = ""

                    if self.choice == "":
                        pass
                    else:  
                        self.attacksound = s('choose')
                        self.attacksound.playSound(0.01)  
                        self.choice = int(self.choice)
                        self.choice = self.choice - 1
                        color.write("________________________________________________________________________________________\n","SYNC")
                        self.choiceref = self.choice
                        self.checkForItem(self.inventory[self.choice].get("name"))

                        if self.inventory[self.choiceref].get("target") == "team":
                            self.oneAutoTarget = self.autopickTarget(team,self.inventory[self.choice].get("affectammount"),"item")
                                
                        elif self.inventory[self.choiceref].get("target") == "user":
                            self.oneAutoTarget = self.pickTarget(self)
                            self.oneAutoTarget = True
                                
                        elif self.inventory[self.choiceref].get("target") == "target":
                            self.oneAutoTarget = self.autopickTarget(opposition,self.inventory[self.choice].get("affectammount"),"item")

                        if self.oneAutoTarget == False:
                                pass
                        elif self.oneAutoTarget == True:
                            color.write("________________________________________________________________________________________\n\n","stderr")
                            #print(self.choice)
                            self.currentItem = self.inventory[self.choiceref]
                            
                            if self.inventory[self.choiceref].get("target") == "team":
                                self.useItemb(self,team)
                            elif self.inventory[self.choiceref].get("target") == "user":
                                self.useItemb(self,team)
                            elif self.inventory[self.choiceref].get("target") == "target":
                                self.useItemb(self,opposition)
                                color.write("________________________________________________________________________________________\n\n","stderr")
                                return

                    
                if self.choice == "4":
                    print(self.name," is trying to escape")
                    self.isflee = self.fleeBattle(team,opposition)
                    if self.isflee == False:
                        activated = False
                        return False
                    else:
                        return True
                
                    
                    
                        
                    
                

class Enemy(Player):
    
    def __init__(self,name,lvl,tag=""):
        print(name)
        self.identname = 0
        super().__init__(name=name,gender="",Class="")
        self.description = ""
        self.stat_list = ['name','description','gender','max_hp','max_mp','strength','dex','intellect','defence','magic_defence','speed']
        self.stat_list2 = [self.name,self.description,self.gender,self.max_hp,self.max_mp,self.strength,self.dex,self.intellect,self.defence,self.magic_defence,self.speed]    
        self.lvl = lvl
        self.tag = tag
        print("Enemy",self.name,"spawn")

    def enemyStatSet(self):
        for i in range(0,len(self.enemies)):
            #print(i)
            if self.enemies[i].get('name') == self.name:
                self.identity = self.enemies[i].copy()
                self.identname = 1
        if self.identname == 0:
            #print("invalid - cant find enemy in database")
            self.identity = self.enemies[0].copy()
        
        for x in range(len(self.identity)-2):
            #print(x)
            keys = list(self.identity.keys())
            key = keys[x] 
            #print(key, ' = ', x)
            if x == len(self.stat_list):
                break
            self.__dict__[self.stat_list[x]] = self.identity.get(key)
            #setattr(self,str(self.stat_list2[x]),self.identity.get(str(key)))

        for x in range (3,len(self.stat_list2)):
            #print(self.identity.get('lvl_stat_multiplier'))
            #print(self.__dict__[self.stat_list[x]])
            self.__dict__[self.stat_list[x]] *= round(((self.identity.get('lvl_stat_multiplier'))**self.lvl)) #library of 
            #self.stat_list2[x] *= ((self.identity.get('lvl_stat_multiplier'))**self.lvl)
            #setattr(self,self.stat_list2[x],round(self.stat_list2[x]))

        self.hp = self.max_hp
        self.mp = self.max_mp
        #print("")
        #print('hp:',"%d/%d" % (self.hp,self.max_hp))
        #print('mp:',"%d/%d" % (self.mp,self.max_mp))
        #print('str:',self.strength)
        #print('int:',self.intellect)
        #print('dex:',self.dex)
        #print('def:',self.defence)
        #print('mdef:',self.magic_defence)
        #print('spd:',self.speed)
        #print("")
            
            
    def randomAttack(self,targetgroup,indexlocation,based_on_what=None,own=None):
        #print("Enemy",self.name,"is attacking")
        #print("1")
        if self.isDead() == True:
            #print("2")
            pass
        elif self.willSkipTurn == True:
            #print('2b')
            pass
        else:
            print("Enemy",self.name,"is making a move")
            #print("3")
            self.movelist = self.identity.get('skills')
            #temp mana ccheck

            for i in self.movelist:
                if self.mp < i.get('mp-cost'):
                    self.movelist.remove(i)
            #print("4")
            #print(targetgroup)
            #print("---",self.pseudogroup)
            
            if based_on_what == None :
                #print("5")
                self.currentMove = self.movelist[random.randint(0,len(self.movelist)-1)]
                self.checkForSkill(self.currentMove.get('name'))

                #print("6")
                if self.currentMove.get('affects') == "user":
                    self.oneAutoTarget = self.pickTarget(self)
                    self.pseudogroup = []
                    targ = []
                elif self.currentMove.get('affects') == "team":
                    self.pseudogroup = own.copy()
                    self.realgroup = own.copy()
                    self.realgroup = list(self.realgroup)
                    targ = self.currentMove['EAI'](own,self.currentMove,self.realgroup,self.pseudogroup)
                else:
                    self.pseudogroup = targetgroup.copy()
                    self.realgroup = targetgroup.copy()
                    self.realgroup = list(self.realgroup)
                    targ = self.currentMove['EAI'](targetgroup,self.currentMove,self.realgroup,self.pseudogroup)

                for i in targ:
                    self.pickTarget(i)            
                color.write("________________________________________________________________________________________\n\n","SYNC")
                
                #color.write("________________________________________________________________________________________\n\n","BUILTIN")
                self.currentSkill = self.currentMove
                #print("12")
                if self.currentMove.get('affects') == "team" or self.currentMove.get('affects') == "user":
                    self.useSkill(self,own,indexlocation)
                else:
                    self.useSkill(self,targetgroup,indexlocation)
                #print("13")
                color.write("________________________________________________________________________________________\n\n","BUILTIN")
            else:
                pass
            return
        
    def calculateExp(self):
        self.expGive = int(self.identity.get('exp') * (1.185**self.lvl))
        if self.expGive <= 0:
            self.expGive = self.identity.get('exp')
        return self.expGive



    #name,gender,lvl,hp,mp,strength,dex,intellect,defence,magic_defence,speed
    enemies = [
        {
            #initial stats (level 1)
        'name':'Goblin',
        'description': 'Vile green thing',
        'gender':'Male',
        'max_hp':80,
        'max_mp':10,
        'strength': 10,
        'dex': 6,
        'intellect': 2,
        'defence': 4,
        'magic_defence': 2,
        'speed': 5,
        'lvl_stat_multiplier': 1.05,
        'skills': [Skill.skills[0]],
        'exp':30,
        'loot':[(Item.items[0],5)]

        },{
            #initial stats (level 1)
        'name':'Orc',
        'description': 'Big Tough Hog',
        'gender':'Male',
        'max_hp':450,
        'max_mp':100,
        'strength': 95,
        'dex': 10,
        'intellect': 1,
        'defence': 15,
        'magic_defence': 2,
        'speed': 3,
        'lvl_stat_multiplier': 1.05,
        'skills': [Skill.skills[0],Skill.skills[2]],
        'exp':100,
        'loot':[(Item.items[0],5)]

        },{
            #initial stats (level 1)
        'name':'Jason',
        'description': 'Demon Slayer Lord',
        'gender':'Male',
        'max_hp':350,
        'max_mp':100,
        'strength': 13,
        'dex': 7,
        'intellect': 10,
        'defence': 5,
        'magic_defence': 5,
        'speed': 6,
        'lvl_stat_multiplier': 1.051,
        'skills': [Skill.skills[0],Skill.skills[3]],
        'exp':99999999999999999999999,
        'loot':[(Item.items[0],5)]

        },{
        #initial stats (level 1)
        'name':'Gangsta',
        'description': 'building street cred',
        'gender':'Male',
        'max_hp':130,
        'max_mp':30,
        'strength': 15,
        'dex': 9,
        'intellect': 2,
        'defence': 6,
        'magic_defence': 6,
        'speed': 8,
        'lvl_stat_multiplier': 1.052,
        'skills': [Skill.skills[0],Skill.skills[1]],
        'exp':30,
        'loot':[(Item.items[1],2)]
        }

        ]
        
    
            
class team:
    
    def partySort_speed(partygroup):
        partygroup.sort(key=lambda x:x.speed, reverse=True)
        return partygroup

    def partyAdd(partygroup,added):
        partygroup.append(added) 

    def partyRemove(partygroup,removed):
        partygroup.append(removed)

    def partyHeal(partygroup):
        for i in range(len(partygroup)):
            partygroup[i].fullRecover()
            

class battle:

    def teamName(group):
        teamlister = ""
        for i in range (0,(len(group))):
            #print(i)
            #print(group[i].name)
            if len(group) > 1 and i > 0 :
                teamlister = teamlister + " and " + group[i].statustag + " " +group[i].tag + group[i].name
            else:
                teamlister = teamlister + "" + group[i].statustag + " " +group[i].tag + group[i].name
                
        #print(teamlister)
        return teamlister
        

    def isPartyAllDead(party):
        counter = 0
        for i in range(len(party)):
            if party[i].isDead() == True:
                counter += 1
        if counter == len(party):
            return True
        else:
            return False
            

def Battle(playerParty,enemyParty,theme):
    battleStatus = True
    pParty = ""
    eParty = ""
    expgain = 0
    playerwin=False
    print("\n\n")
    color.write("______________________________________________________________________________________\n\n","SYNC")
    #print(enemyParty[0].name)
    print("This is a battle :",battle.teamName(playerParty), "against", battle.teamName(enemyParty))
    attacksound = s(theme)
    attacksound.playSound(1)
    while True:
        #print("1")
        p_partyStatus = battle.isPartyAllDead(enemyParty)
        e_partyStatus = battle.isPartyAllDead(playerParty)
        #print("2")
        if battleStatus == False:
            print("yikes, you left")
            break
        #print("3")
        if e_partyStatus == True:
            attacksound.stopSound()
            attacksound = s('losebattle')
            attacksound.playSound()
            break
        #print("4")
        if p_partyStatus == True:
            color.write("______________________________________________________________________________________\n","SYNC")
            print("\n\n                                   !Victory!       ")
            print("")
            color.write("______________________________________________________________________________________\n","SYNC")
            print("")
            print("")
            attacksound.stopSound()
            attacksound = s('winbattle')
            attacksound.playSound(0.5)
            input("")
            playerwin = True
            break
        #print("5")

        p = playerParty
        e = enemyParty
        attackorder = playerParty + enemyParty
        attackorder = team.partySort_speed(attackorder)
        #print("6")
        
        for i in range(len(attackorder)):
            #print("7")
            if attacksound.checkSound() == True:
                pass
            else:
                attacksound.playSound(1)
            #print("8")    
            #print("list number:",i)
            
                #print(j.name + " is " + str(startingstatchecker ))
            
            if isinstance(attackorder[i],Enemy) == True:
                #print("e9")
                attackorder[i].checkAllStates()
                attackorder[i].randomAttack(playerParty,enemyParty.index(attackorder[i]),own=enemyParty)
                
            elif isinstance(attackorder[i],Player) == True:
                attackorder[i].checkAllStates()
                #print("p9")
                theAttack = attackorder[i].battleMenu(enemyParty,playerParty)
                
                if theAttack == False:
                    #print("10")
                    battleStatus = False
                    print("battle over")
                    attacksound.stopSound()
                    #sa.stop_all()
                    attacksound = s('dash')
                    attacksound.playSound()
                    return
                
            #print("11")    
            p_partyStatus = battle.isPartyAllDead(enemyParty)
            e_partyStatus = battle.isPartyAllDead(playerParty)
            #print("12")
            if battleStatus == False:
                #print("13")
                break
            if e_partyStatus == True:
                #print("13")
                break
            if p_partyStatus == True:
                #print("13")
                break
            #print("13")

    #print("14")        
    attacksound.stopSound()
    #print("15")
    if playerwin == True:
        attacksound = s("spoils")
        battleendsound = s('choose')
        attacksound.playSound(0.5)
        for j in enemyParty:
            expgain += j.calculateExp()
        expgain = int(expgain/len(playerParty))
        for i in playerParty:
            multi = 1
            color.write("______________________________________________________________________________________\n\n","SYNC")
            if i.isDead() == True:
                print(i.name + " is unable to receive all the experience due to being unconcious")
                multi = 0.1
            i.gain_exp(expgain*multi)
            input("\n      press anything to continue \n")
            battleendsound.playSound(0.01)
            color.write("______________________________________________________________________________________\n","SYNC")
    attacksound.stopSound()    
    color.write("______________________________________________________________________________________\n","SYNC")
    #print("battle over")

    if playerwin == True:
        return True
    else:
        return False
      
"""
#Game itself        553exp = lvl 5


#mc = leon, Valin, Crysela, Petra

#main1 = Player("Leon","M","Mage","☆ ") #spawns in leon

playerParty = []
#playerParty.append(main1)

#main2 = Player("Valin","M","Warrior","☆ ") #spawns in valin

#playerParty.append(main2)

#main3 = Player("Crysela","F","Mage","☆ ") #spawns in crysela

#playerParty.append(main3)

main4 = Player("Ethan","M","Paladin","☆ ") #spawns in petra

playerParty.append(main4)

for i in playerParty:
    i.gain_exp(2000)

playerParty = team.partySort_speed(playerParty)

for i in playerParty:
    i.fullRecover()

#enemies

enemy2 = Enemy("Goblin",30,"Crazy ")
enemy3 = Enemy("Goblin",30,"Lazy ")
enemy4 = Enemy("Gangsta",30,"Brazy ")
enemy5 = Enemy("Gangsta",30,"Fugazi ")

crazy = [enemy2,enemy3,enemy4,enemy5]
for i in crazy:
    i.enemyStatSet()

Battle(playerParty,crazy,'battle')


"""

"""           
p1 = Player("Daniel","M","Mage","☆ ") #spawns in daniel
playerParty = [p1]


p2 = Player("Danielle","F","Warrior","☆ ") #spawns in lucy
playerParty.append(p2)

print(p1.name)
print(p1.Class,p1.hp)
print(Skill.skills[0].get("name"))
#print(Item.id1.get("name"))
p1.exp = 100
print(p1.lvl)
p1.level_up()
print(p1.lvl)
print(p1.expCap)
p1.gain_exp(1200)
p2.gain_exp(1200)

for x in range(len(playerParty)): 
    print (playerParty[x].name),
    
playerParty = team.partySort_speed(playerParty)

for x in range(len(playerParty)): 
    print (playerParty[x].name),

p1.fullRecover()
p2.fullRecover()

p3 = Enemy("Goblin",5,"Weak ")
p3.enemyStatSet()
p4 = Enemy("Goblin",1,"Lil Bro ")
p4.enemyStatSet()
p5 = Enemy("Goblin",15,"Big Bro ")
p5.enemyStatSet()
p6 = Enemy("Orc",15,"Boss ")
p6.enemyStatSet()

p666 = Enemy("Jason",30,"Demon Slayer ")
p666.enemyStatSet()

sound = s('story')
sound = s('story')

enemyGroup = [p3]
enemyGroup2 = [p4,p5]
enemyGroup3 = [p6]
Jason = [p666]


color.write("______________________________________________________________________________________\n","SYNC")

print("max hp: ",p1.max_hp)
print("defence: ",p1.defence)
p1.equipGear(Item.items[2])
print("max hp: ",p1.max_hp)
print("defence: ",p1.defence)
p1.unequipGear('head')
print("max hp: ",p1.max_hp)
print("defence: ",p1.defence)


color.write("______________________________________________________________________________________\n","SYNC")


print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
sound.playSound(0.5)
print("walking in the fields...")
input("\n      press anything to continue \n")
print("whoah!")
sound.stopSound()
time.sleep(2)
Battle(playerParty,enemyGroup,'battle')
sound.playSound(0.5)
print("\n\n you find yourself at the entrance of a creepy cave...")
input("\n      press anything to continue \n")
sound.stopSound()
print("whoah!")
time.sleep(2)
cbattle = Battle(playerParty,enemyGroup2,'battle')
if cbattle == True:
    pass
elif cbattle == False:
    while True:
        print("Goblin Bros : Jajajjajajjajajajajajajajjajajajajajajajajjajajajajajajajajjajajajajajaj")
        time.sleep(0.2)


team.partyHeal(playerParty)

print("\n\n It's the end of the creepy cave...")
input("\n      press anything to continue \n")
print("It's the boss!")
time.sleep(2)
cbattle = Battle(playerParty,enemyGroup3,'boss')

if cbattle == True:
    pass
elif cbattle == False:
    while True:
        print("Orc : uguguguguguguguguuguguguguguguguguguguugugugugugugugugugu")
        time.sleep(0.2)

sound.playSound(0.5)

print("\n\n After finally defeating the goblins, you take a rest")
input("\n      press anything to continue \n")
print("...")
time.sleep(2)
print("...")
time.sleep(2)
print("...")
time.sleep(2)
print("...")
time.sleep(2)
sound.stopSound()
team.partyHeal(playerParty)
print("Jason has awoken")
time.sleep(2)
finalbattle = Battle(playerParty,Jason,'jason')

if cbattle == True:
    print("Jason has been defeated, but so has this demo")
    print("Thanks 4 playing")
elif cbattle == False:
    while True:
        print("Jason: Jajajjajajjajajajajajajajjajajajajajajajajjajajajajajajajajjajajajajajaj")
        time.sleep(0.2)

"""

