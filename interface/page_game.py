# By: Andrew C.
# Date: 2024-12-07
# Program Details: This Program is a fully functional wave based attack game WITH a miniboss and a final boss it is called resonance and you collect music discs and items for power

#Options for code to view 
#1. SETUP CODE
#2. HEALTHPOT CODE
#3. WAVE CODE
#4. BOSS CODE
#5. MINIBOSS CODE
#6. ENEMY CODE
#7. ATTACK CODE
#8. MOVEMENT CODE
#9. INVENTORY CODE
#10. PAUSE CODE
#11. MIXER CODE
#12. DISC CODE
#13. CLASSES CODE
#14. STARTSCREEN CODE
#15. YOUDIED CODE

import os, sys, ULTIMATE_DEFS, enemies, random, items
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import manager
from PySide6.QtWidgets import QMainWindow
from gui.page_game_ui import Ui_MainWindow
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QListWidgetItem, QListWidget, QLabel, QWidget
from pygame import mixer

if __name__ == "__main__":    
    manager.start()

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        with manager.image_gui_path():
            self.setupUi(self)
        
        mixer.init()
        self.play_music("audio/bgmusic.mp3")
        self.setWindowTitle("Resonance")
        self.musiccheckertimer = QTimer()
        self.musiccheckertimer.timeout.connect(self.loop_music)
        self.musiccheckertimer.start(500)
        
#SETUP CODEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE
    def setup(self):
        self.pause_buttons = [self.btn_resume, self.btn_title, self.lbl_titlename, self.btn_exit]
        for i, button in enumerate(self.pause_buttons):
            button.setVisible(False)
        self.ui = [self.lbl_bosshealthbarbg, self.lbl_bosshealthbar, self.lbl_bossheartnobg, self.lbl_bosshealth, self.lbl_bossname, self.lbl_healthbarbg,  self.lbl_healthbar, self.lbl_heartnobg, self.lbl_playerhealth, self.lbl_player, self.lbl_wave, self.lbl_yapyapyap, self.lbl_weapon_1, self.lbl_weapon_2, self.lbl_weapon_3, self.lbl_weapon_4, self.lbl_weapon_5, self.lbl_weapon_6, self.lbl_weapon_7, self.lbl_weapon_8, self.lbl_bowcooldown, self.lbl_bowability, self.lbl_score, self.lbl_scorename, self.lbl_wave, self.lbl_wavename, self.lbl_wavename_2]
        self.choices = [self.lbl_choice1_backround, self.lbl_choice1_title, self.lbl_choice1_image, self.lbl_choice1_description, self.btn_choice1, self.lbl_choice2_backround, self.lbl_choice2_title, self.lbl_choice2_image, self.lbl_choice2_description, self.btn_choice2, self.lbl_choice3_backround, self.lbl_choice3_title, self.lbl_choice3_image, self.lbl_choice3_description, self.btn_choice3]
        for i, name in enumerate(self.choices):
            name.setVisible(False)
            name.lower()
        self.fuzziepositionnumber = 1 #miniboss ranged attack
        self.lbl_bosshealth.setVisible(False)
        self.lbl_bosshealthbar.setVisible(False)
        self.lbl_bosshealthbarbg.setVisible(False)
        self.lbl_bossheartnobg.setVisible(False)
        self.lbl_bossname.setVisible(False)
        self.enter = True #making sure  you can only press enter when you need to
        self.lbl_wave.setText("0")
        self.lbl_yapyapyap.setText("Welcome to Resonance! \n A wave based RPG in which you fight against hordes of enemies, collecting power ups along the way \n the first enemy you'll be fighting is the mighty slime, the most basic of all enemies moderate damage but still a warmup...\n click up arrow to attack and WASD to move \n GLHF! \n (click enter to start first wave)")
        self.lbl_yapyapyap.setVisible(True)
        self.pausestate = True
        self.slime = enemies.Slime(10, 5, 0, QPixmap(u"images/blue_slime.gif"), 2)
        self.hauntedarmor = enemies.HauntedArmor(40, 5, 4, QPixmap(u"images/hauntedarmor.png"), 1)
        self.mage = enemies.Mage(10, 1, 0, QPixmap(u"images/mage.png"), 1, 5)
        self.sonic = enemies.Sonic(20, 10, 4, QPixmap(u"images/sonic.png"), 4)
        self.tangela = enemies.Tangela(30, 5, 3, QPixmap(u"images/tangela.png"), 0)
        self.allenemies = [self.slime, self.hauntedarmor, self.mage, self.sonic, self.tangela]
        self.timer_player=QTimer()
        self.timer_player.start(5)
        self.timer_player.timeout.connect(self.player_move)
        self.enemyclass_list = []    #classes
        self.enemylabels_list = []   #labels
        self.enemyhplabels_list = [] #hp labels
        self.enemyintlist = [] #classifying each enemy
        self.boss_labels = [] #boss labels
        self.boss_enemies = [0, 1, 4] #boss enemies
        self.bossclasslist = [] #boss classes
        self.warning_labels = [] #warning labels
        self.minibossattacknumber = 0 #counting how much miniboss attacked
        self.bossattacknumber = 0 #counting how much boss attacked
        self.bossdead = True
        self.minibossdead = True
        self.playerconfused = False
        self.timer_enemy=QTimer()
        self.timer_enemy.start(20) #need to lower the more you add
        self.timer_enemy.timeout.connect(self.enemy_movement)
        self.sonicIN = False
        self.keypress = [] #list of keys pressed
        self.attacknumber = 5 #where you start
        self.inventorynames = [self.lbl_melee, self.lbl_ranged, self.lbl_armor, self.lbl_boots, self.lbl_lifeforce, self.lbl_disc1, self.lbl_disc2, self.lbl_disc3]
        self.inventory() #initializing inventory
        self.inventory_part = 1 #which part of inventory u on
        self.item_text_list = ["blank", "bow", "CD", "bow", "armor", "boots", "sword", "sword", "lifeforce"]
        self.attack_list = [self.lbl_weapon_1, self.lbl_weapon_2, self.lbl_weapon_3, self.lbl_weapon_4, self.lbl_weapon_5, self.lbl_weapon_6, self.lbl_weapon_7, self.lbl_weapon_8] 
        self.tab_part = 1 #which tab part u on
        self.rangedvalid = True #starting off being able to attack
        self.meleevalid = True #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        self.enemy_rangedvalid = True #ensures ranged attacks can run on start
        self.playerhealth = 100 
        self.maxhealth = 100
        self.playerdefense = 0
        self.playerattackdmg = 5
        self.rangedattackdmg = 3 
        self.playerspeed = 1
        self.score = 0
        self.lbl_score.setText(str(self.score))
        self.enemy_ranged_attacks()
        self.enemy_ranged_timers = []  # List to store timers for mages 
        self.enemy_checking_timer = QTimer()
        self.enemy_checking_timer.start(500)
        self.enemy_checking_timer.timeout.connect(self.enemy_checking)
        self.tangelalist = list(range(-101, 101))
        self.itemchoicevalidness = True #ensures items can run once
        #swords
        timesword = items.item(QPixmap(u"images/timesword.jpg"), "timesword.jpg", "timesword", "Time Sword", "A sword once \n once wielded by kronos \n himself, increases attack \n by 3 and speed by 1", "background-color: rgb(255, 0, 0);", 3, 0, 0, 1, 0)
        mosquitorapier = items.item(QPixmap(u"images/mosquito_rapier.jpg"), "mosquito_rapier.jpg", "mosquitorapier", "T Mos Rapier", "A rapier forged out of \n the beak of a mighty \n tiger mosquito \n decreases attack by 1 \n but enables lifesteal", "background-color: rgb(255, 0, 0);", -1, 0, 0, 0, 0)
        #bows
        futurebow = items.item(QPixmap(u"images/futurebow.png"), "futurebow.png", "futurebow", "Future Bow", "A bow that shoots \n arrows that pierce \n through time and space \n increases ranged damage \n by 7", "background-color: rgb(140, 0, 0);", 0, 7, 0, 0, 0)
        slimebow = items.item(QPixmap(u"images/slimebow.jpg"), "slimebow.jpg", "slimebow", "Slime Bow", "A bow that shoots \n bouncy arrows that \n knock enemies back \n and increases ranged \n damage by 4 \n (Note: knockback doesn't \n affect bosses or mages)", "background-color: rgb(140, 0, 0);", 0, 4, 0, 0, 0)
        #armor
        ironarmor = items.item(QPixmap(u"images/iron_armor.jpg"), "iron_armor.jpg", "ironarmor", "Iron Armor", "A set of armor that \n is said to be \n unbreakable, increases \n defense by 5", "background-color: rgb(0, 170, 255);", 0, 0, 5, 0, 0)
        thornmail = items.item(QPixmap(u"images/thornyarmor.png"), "thornyarmor.png", "thornmail", "Thornmail", "a light set of armor \n that has sharp points \n along its body increasing \n defense by 2 and \n enabling thorns \n making enemies take 3 \n damage to attack you \n (not affected by def)", "background-color: rgb(0, 170, 255);", 0, 0, 2, 0, 0)
        #boots
        wingedrunners = items.item(QPixmap(u"images/wingedrunners.png"), "wingedrunners.png", "wingedrunners", "W Runners", "A set of running shoes \n  that almost gives you \n flight, jetting you \n across the battlefield \n increasing speed by 4", "background-color: rgb(0, 255, 127);", 0, 0, 0, 4, 0)
        ironboots = items.item(QPixmap(u"images/ironboots.jpg"), "ironboots.jpg", "ironboots", "Iron Boots", "a set of sturdy iton \n boots that increase \n defense by 2", "background-color: rgb(0, 255, 127);", 0, 0, 2, 0, 0)
        #lifeforce
        armoredheart = items.item(QPixmap(u"images/armoredheart.jpg"), "armoredheart.jpg", "armoredheart", "Armor Heart", "A heart that can be \n used to increase max \n health by 100", "background-color: rgb(255, 85, 255);", 0, 0, 0, 0, 100)
        cyborgheart = items.item(QPixmap(u"images/cyborgheart.jpg"), "cyborgheart.jpg", "cyborgheart", "Cyborg Heart", "A mechanical heart that \n increases efficiency of \n all bodily systems, \n raises all stats by 1", "background-color: rgb(255, 85, 255);", 1, 1, 1, 1, 0)
        #discs
        backinblack = items.item(QPixmap(u"images/backinblack.png"), "backinblack.png", "backinblack", "Back in Black", "A special disc that \n when equipped can be \n used to activate \n damaging pillars of fire \n that periodically deal \n damage for 15 seconds \n (not affected by def)", "background-color: rgb(170, 170, 255);", 0, 0, 0, 0, 0)
        thickofit = items.item(QPixmap(u"images/thickofit.jpg"), "thickofit.jpg", "thickofit", "Thick of It", "A special disc that \n when equipped can be \n used to repel minor \n enemies for 30 seconds \n when enemies reach an \n edge they will be \n knocked to middle", "background-color: rgb(170, 170, 255);", 0, 0, 0, 0, 0)
        imstillstanding = items.item(QPixmap(u"images/imstillstanding.jpg"), "imstillstanding.jpg", "imstillstanding", "I S Standing", "A special disc that \n when equipped can be \n used to revive \n yourself on 25 hp if \n you take a fatal blow \n and making you \n invincible for 10 seconds", "background-color: rgb(170, 170, 255);", 0, 0, 0, 0, 0)
        sixhundredstrike = items.item(QPixmap(u"images/sixhundredstrike.jpg"), "sixhundredstrike.jpg", "sixhundredstrike", "600 Strike", "A special disc that \n when equipped can be \n used to deal 10 damage \n periodically to the \n highest health enemy on \n screen (note only works if \n there are enemies present)", "background-color: rgb(170, 170, 255);", 0, 0, 0, 0, 0)
        #healthpot
        healthpot = items.healthpot(QPixmap(u"images/healthpot.jpg"), "Health Potion", "A potion that heals \n 50 health instantly", "background-color: rgb(204, 0, 153);")
        self.allitems = [timesword,  mosquitorapier, futurebow, slimebow, ironarmor, thornmail, wingedrunners, ironboots, armoredheart, cyborgheart, backinblack, thickofit, imstillstanding, sixhundredstrike, healthpot, healthpot, healthpot, healthpot, healthpot, healthpot]
        #self.allitems = [timesword, futurebow, thornmail]
        self.fireball_list = []
        self.fireball_timers = [QTimer()]*10
        self.sonic_movement()
        self.lbl_playerhealth.setText(str(self.playerhealth))
        self.lbl_healthbar.setFixedSize(self.playerhealth * 4, 41)
        self.playerlifesteal = False
        self.playerrangedknockback = False
        self.playerthorns = False
        self.backinblack_cooldown = False
        self.BIBvalid = True
        self.backinblackused = False
        self.BIBcompleted = True
        self.thickofitmovement = False
        self.thickofitused = False
        self.TOIcompleted = True
        self.imstillstandingused = False
        self.ISScompleted = True
        self.playerinvicible = False
        self.sixhundredstrikeused = False
        self.SHScompleted = True
        self.sixhundredstrikevalid = True
        self.sixhundredstrikecooldown = False
        self.inventoryunequipchecker()
        #self.lbl_wave.setText("4")

#HEALTHPOT CODEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE
    def healthpot(self):
        self.playerhealth += 50
        if self.playerhealth > self.maxhealth:
            self.playerhealth = self.maxhealth
        self.lbl_playerhealth.setText(str(self.playerhealth))
        if self.maxhealth == 100:
            self.lbl_healthbar.setFixedSize(self.playerhealth * 4, 41)#the times four is because self.playerhealth is 4 times as big as the players hp
        elif self.maxhealth == 200:
            self.lbl_healthbar.setFixedSize(self.playerhealth * 2, 41) 
        
#WAVE CODEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE
    def wave(self):
        if self.lbl_wave.text() == "1":
            for i in range(2):
                self.enemy_creation(0) #creating 2 slimes
        elif self.lbl_wave.text() == "2":
            for i in range(3):
                self.enemy_creation(0) #creating 3 slimes
            for i in range(2):
                self.enemy_creation(2) #creating 2 mages
        elif self.lbl_wave.text() == "3":
            for i in range(5):
                self.enemy_creation(2) #creating 5 mages
        elif self.lbl_wave.text() == "4":
            for i in range(4):
                self.enemy_creation(1) #creating 4 haunted armors
            for i in range(2):
                self.enemy_creation(2) #creating 2 mages
        elif self.lbl_wave.text() == "5":
            self.miniboss()
        elif self.lbl_wave.text() == "6":
            for i in range(1):
                self.enemy_creation(3) #creating 1 sonic
                self.sonicIN = True
            for i in range(5):
                self.enemy_creation(1) #creating 5 haunted armors
            for i in range(3):
                self.enemy_creation(0) #creating 3 slimes
        elif self.lbl_wave.text() == "7":
            for i in range(1):
                self.enemy_creation(3) #creating 1 sonic
                self.sonicIN = True
            for i in range(8):
                self.enemy_creation(1) #creating 8 haunted armors
            for i in range(5):
                self.enemy_creation(0) #creating 3 slimes
        elif self.lbl_wave.text() == "8":
            for i in range(1):
                self.enemy_creation(3) #creating 1 sonic
                self.sonicIN = True
            for i in range(10):
                self.enemy_creation(1) #creating 10 haunted armors
            for i in range(5):
                self.enemy_creation(0) #creating 5 slimes
            for i in range(2):
                self.enemy_creation(4) #creating 2 tangelas
        elif self.lbl_wave.text() == "9":
            for i in range(1):
                self.enemy_creation(3) #creating 1 sonic
                self.sonicIN = True
            for i in range(15):
                self.enemy_creation(1) #creating 15 haunted armors
            for i in range(15):
                self.enemy_creation(0) #creating 15 slimes
            for i in range(6):
                self.enemy_creation(4) #creating 6 tangelas
        elif self.lbl_wave.text() == "10":
            self.boss()
        for i, name in enumerate(self.enemyintlist):
            if name == 4:
                self.enemyhplabels_list[i].move(self.enemylabels_list[i].pos().x()+90, self.enemylabels_list[i].pos().y()-20)
                self.enemyhplabels_list[i].raise_()
            if name == 2:
                self.enemyhplabels_list[i].move(self.enemylabels_list[i].pos().x()+17, self.enemylabels_list[i].pos().y()-30)
                self.enemyhplabels_list[i].raise_()
            if name == 1:
                self.enemyhplabels_list[i].move(self.enemylabels_list[i].pos().x()+22, self.enemylabels_list[i].pos().y()-30)
                self.enemyhplabels_list[i].raise_()

    def dialogue(self):
        if self.lbl_wave.text() == "0":
            self.reseting_yapsession()
            self.lbl_wave.setText("1")
            self.wave()
        elif self.lbl_wave.text() == "1":
            self.reseting_yapsession()
            self.lbl_wave.setText("2")  
            self.wave()
        elif self.lbl_wave.text() == "2":
            self.reseting_yapsession()
            self.lbl_wave.setText("3")
            self.wave()
        elif self.lbl_wave.text() == "3":
            self.reseting_yapsession()
            self.lbl_wave.setText("4")
            self.wave()
        elif self.lbl_wave.text() == "4":
            self.reseting_yapsession()
            self.lbl_wave.setText("5")
            self.wave()
        elif self.lbl_wave.text() == "5":
            self.reseting_yapsession()
            self.lbl_wave.setText("6")
            self.wave()
        elif self.lbl_wave.text() == "6":
            self.reseting_yapsession()
            self.lbl_wave.setText("7")
            self.wave()
        elif self.lbl_wave.text() == "7":
            self.reseting_yapsession()
            self.lbl_wave.setText("8")
            self.wave()
        elif self.lbl_wave.text() == "8":
            self.reseting_yapsession()
            self.lbl_wave.setText("9")
            self.wave()
        elif self.lbl_wave.text() == "9":
            self.reseting_yapsession()
            self.lbl_wave.setText("10")
            self.wave()
            
    def enemy_checking(self):  
        if 3 in self.enemyintlist:
            self.sonicIN = True     
        if self.enemylabels_list == [] and self.lbl_wave.text() == "1":
            self.lbl_yapyapyap.setVisible(True) 
            self.lbl_yapyapyap.setText("That right there was equipment click tab to enter your inventory \n you can click and drop items to their slots and use em' \n you can also use ranged attacks by pressing the right arrow key \n finally you can use your disc slots by pressing z, x, and c, \n (note only 1 disc can be used at a time) \n now lets see some more enemies")
            if self.itemchoicevalidness == True:
                self.itemchoicevalidness = False
                self.itemchoice()
        elif self.enemylabels_list == [] and self.lbl_wave.text() == "2":
            self.lbl_yapyapyap.setVisible(True) 
            self.lbl_yapyapyap.setText("Mages are pretty cool huh. \n its almost like I put my blood sweat and tears into their attack.........\n lets see some more of em")
            if self.itemchoicevalidness == True:
                self.itemchoicevalidness = False
                self.itemchoice()
        elif self.enemylabels_list == [] and self.lbl_wave.text() == "3":
            self.lbl_yapyapyap.setVisible(True)
            self.lbl_yapyapyap.setText("at this point your probably a little fireballed out \n maybe a bit singed even... \n but don't worry your like at least somewhat close to losi- \n I mean winning! \n This next enemy was very easy to code, but I dont think you'll like her...\n they are strong, fortified you could say... \n Good luck!")
            if self.itemchoicevalidness == True:
                self.itemchoicevalidness = False
                self.itemchoice()
        elif self.enemylabels_list == [] and self.lbl_wave.text() == "4":
            self.lbl_yapyapyap.setVisible(True)
            self.lbl_yapyapyap.setText("I'm suprised you made it this far... \n I mean I guess I shouldn't be, you are the player after all... \n but still... \n lets throw something a bit harder at you... \n quick tip: you will defintley NOT be able to outrun her \n hint: red = very bad")
            if self.itemchoicevalidness == True:
                self.itemchoicevalidness = False
                self.itemchoice()
        elif self.boss_labels == [] and self.lbl_wave.text() == "5":
            self.lbl_yapyapyap.setVisible(True)
            self.lbl_yapyapyap.setText("Wow, nice job... \n I guess even the fastest can be put down \n well you've made it to act 2 \n starting off heres a new enemy, \n they like speed too \n have fun...")
            if self.itemchoicevalidness == True:
                self.itemchoicevalidness = False
                self.itemchoice()
        elif self.enemylabels_list == [] and self.lbl_wave.text() == "6":
            self.lbl_yapyapyap.setVisible(True)
            self.lbl_yapyapyap.setText("Isnt he cool? \n sonic got zooted and now hes attacking you! \n crazy experiences \n anyway hopefully your having fun \n I'm running out of things to show you \n lets see what you can do with more chaos...")
            if self.itemchoicevalidness == True:
                self.itemchoicevalidness = False
                self.itemchoice()
        elif self.enemylabels_list == [] and self.lbl_wave.text() == "7":
            self.lbl_yapyapyap.setVisible(True)
            self.lbl_yapyapyap.setText("SOO...I bet your tired of fast things \n , what about something that doesnt move? \n I bet itll be great for you! enjoy...")
            if self.itemchoicevalidness == True:
                self.itemchoicevalidness = False
                self.itemchoice()
        elif self.enemylabels_list == [] and self.lbl_wave.text() == "8":
            self.lbl_yapyapyap.setVisible(True)
            self.lbl_yapyapyap.setText("so uhm....yeah those vine thingys hurt \n also yes it is a pokemon #188 \n hopefully your enjoying your powerups \n lets make this harder...")
            if self.itemchoicevalidness == True:
                self.itemchoicevalidness = False
                self.itemchoice()
        elif self.enemylabels_list == [] and self.lbl_wave.text() == "9":
            self.lbl_yapyapyap.setVisible(True)
            self.lbl_yapyapyap.setText("you have made it far.... \n fought many a horde from lowly slimes to the great ghost \n now you will face her... \n the final boss... \n I'm rooting for you")
            if self.itemchoicevalidness == True:
                self.itemchoicevalidness = False
                self.itemchoice()
        elif self.boss_labels == [] and self.lbl_wave.text() == "10":
            self.lbl_yapyapyap.setVisible(True)
            self.lbl_yapyapyap.setText("I can't beleive you did it! \n you beat resonance, congrats! \n click esc and the button that appears \n to go back to the main menu")
    
    def reseting_yapsession(self):
        self.lbl_yapyapyap.setVisible(False)
        self.lbl_yapyapyap.setText("")
        self.enter = False
    
    def itemchoice(self):
        for i, name in enumerate(self.choices):
            name.setVisible(True)
            name.raise_()
        self.choice1 = random.choice(self.allitems)
        self.lbl_choice1_title.setText(self.choice1.title)
        self.lbl_choice1_image.setPixmap(self.choice1.pixmap)
        self.lbl_choice1_description.setText(self.choice1.description)
        self.lbl_choice1_backround.setStyleSheet(self.choice1.stylesheet)
        self.allitems.pop(self.allitems.index(self.choice1))
        self.choice2 = random.choice(self.allitems)
        self.lbl_choice2_title.setText(self.choice2.title)
        self.lbl_choice2_image.setPixmap(self.choice2.pixmap)
        self.lbl_choice2_description.setText(self.choice2.description)
        self.lbl_choice2_backround.setStyleSheet(self.choice2.stylesheet)
        self.allitems.pop(self.allitems.index(self.choice2))
        self.choice3 = random.choice(self.allitems)
        self.lbl_choice3_title.setText(self.choice3.title)
        self.lbl_choice3_image.setPixmap(self.choice3.pixmap)
        self.lbl_choice3_description.setText(self.choice3.description)
        self.lbl_choice3_backround.setStyleSheet(self.choice3.stylesheet)
        self.allitems.pop(self.allitems.index(self.choice3))
    
    def btn_choice1_a(self):
        self.chosen = self.choice1
        if self.chosen.title == "Health Potion":
            self.healthpot()
        else:
            self.done = False
            for i, slot in enumerate(self.slot_list):
                if self.done == False and slot.item(0).text() == "blank":
                    self.addinventoryitem(self.choice1.slot_pixmap, slot, self.choice1.type)  
                    self.done = True
        self.allitems.append(self.choice2)
        self.allitems.append(self.choice3)
        self.enter = True
        self.hide_choices()
        for i, name in enumerate(self.fireball_list):
            try:
                name.setVisible(False)
                name.deleteLater()
            except:
                pass
        for i, name in enumerate(self.fireball_timers):
            try:
                name.stop()
            except:
                pass
            

    def btn_choice2_a(self):
        self.chosen = self.choice2
        if self.chosen.title == "Health Potion":
            self.healthpot()
        else:
            self.done = False
            for i, slot in enumerate(self.slot_list):
                if self.done == False and slot.item(0).text() == "blank":
                    self.addinventoryitem(self.choice2.slot_pixmap, slot, self.choice2.type)  
                    self.done = True
        self.allitems.append(self.choice1)
        self.allitems.append(self.choice3)
        self.enter = True
        self.hide_choices()
        for i, name in enumerate(self.fireball_list):
            try:
                name.setVisible(False)
                name.deleteLater()
            except:
                pass
        for i, name in enumerate(self.fireball_timers):
            try:
                name.stop()
            except:
                pass
    
    def btn_choice3_a(self):
        self.chosen = self.choice3
        if self.chosen.title == "Health Potion":
            self.healthpot()
        else:
            self.done = False
            for i, slot in enumerate(self.slot_list):
                if self.done == False and slot.item(0).text() == "blank":
                    self.addinventoryitem(self.choice3.slot_pixmap, slot, self.choice3.type)  
                    self.done = True
        self.allitems.append(self.choice1)
        self.allitems.append(self.choice2)
        self.enter = True
        self.hide_choices()
        for i, name in enumerate(self.fireball_list):
            try:
                name.setVisible(False)
                name.deleteLater()
            except:
                pass
        for i, name in enumerate(self.fireball_timers):
            try:
                name.stop()
            except:
                pass
        
    def hide_choices(self):
        for i, name in enumerate(self.choices):
            name.setVisible(False)
            name.lower()
            
#BOSS CODEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE

    def boss(self):
        #addinghealthbar
        self.lbl_bosshealth.setVisible(True)
        self.lbl_bosshealthbar.setVisible(True)
        self.lbl_bosshealthbarbg.setVisible(True)
        self.lbl_bossheartnobg.setVisible(True)
        self.lbl_bossname.setVisible(True)
        self.lbl_bossname.setText("Mycoria: The Blooming Tyrant")
        #creation
        self.bossdead = False
        self.bossclass = enemies.Boss(300, 15, 5,  QPixmap(u"images/final_boss.png"), 1, 10)
        self.lbl_bosshealth.setText(str(self.bossclass.health))
        self.boss_label = QLabel(self.centralwidget)
        self.boss_label.setFixedSize(300, 400)
        self.boss_label.setPixmap(self.bossclass.pixmap)
        self.boss_label.setScaledContents(True)
        self.boss_label.move(550, 275)
        self.boss_label.setVisible(True)
        self.boss_labels.append(self.boss_label)
        self.bossclasslist.append(self.bossclass)
        self.attacking_boss()

    def attacking_boss(self):
        if self.bossdead == False:
            if self.bossattacknumber > 0:
                self.tired.setVisible(False)
            attack = random.randint(1, 5)
            if attack == 1:
                self.sporeslam()
            elif attack == 2:
                self.boss_confusion()
            elif attack == 3:
                self.spawn_enemy()
            elif attack == 4:
                self.vinecluster()
            elif attack == 5:
                self.hyperbeam()
            self.bossattacknumber += 1 

#def spawning enemies
    def spawn_enemy(self):
        if self.bossdead == False:
            for i in range(2):
                enemy = random.choice(self.boss_enemies) #choosing random enemy
                self.enemy_creation(enemy)
                if enemy == 4:
                    self.enemyhplabels_list[i].move(self.enemylabels_list[i].pos().x()+90, self.enemylabels_list[i].pos().y()-20)
                    self.enemyhplabels_list[i].raise_()
            self.boss_cooldown()
            
#confusion
    def boss_confusion(self):
        self.warning_label1 = QLabel(self.centralwidget)
        self.warning_labels.append(self.warning_label1)
        self.warning_label2 = QLabel(self.centralwidget)
        self.warning_labels.append(self.warning_label2)
        self.warning_label3 = QLabel(self.centralwidget)
        self.warning_labels.append(self.warning_label3)
        self.warning_label4 = QLabel(self.centralwidget)
        self.warning_labels.append(self.warning_label4)
        for i, name in enumerate(self.warning_labels):
            name.setStyleSheet("background-color: rgb(255, 0, 0);")
            name.setVisible(True)
        self.warning_label1.setFixedSize(591, 200)
        self.warning_label2.setFixedSize(200, 301)
        self.warning_label3.setFixedSize(631, 200)
        self.warning_label4.setFixedSize(200, 301)
        self.warning_label1.move(-2, 340)
        self.warning_label2.move(610, -30)
        self.warning_label3.move(850, 340)
        self.warning_label4.move(610, 650)
        if self.bossdead == False:
            QTimer.singleShot(1000, lambda: self.boss_confusion2())
    
    def boss_confusion2(self):
        for i, name in enumerate(self.warning_labels):
            name.deleteLater()
        self.warning_labels.clear()
        self.spore_label1 = QLabel(self.centralwidget)
        self.warning_labels.append(self.spore_label1)
        self.spore_label2 = QLabel(self.centralwidget)  
        self.warning_labels.append(self.spore_label2) 
        self.spore_label3 = QLabel(self.centralwidget)
        self.warning_labels.append(self.spore_label3)
        self.spore_label4 = QLabel(self.centralwidget)
        self.warning_labels.append(self.spore_label4)
        for i, name in enumerate(self.warning_labels):
            name.setFixedSize(200, 200)
            name.setPixmap(QPixmap(u"images/sporecloud.png"))
            name.setVisible(True)
            try:
                name.move(self.boss_label.x()+45, self.boss_label.y()+70)
            except:
                pass
        self.confusionvalid = True
        if self.bossdead == False:
            self.sporecloudtimer = QTimer()
            self.sporecloudtimer.start(5)
            self.sporecloudtimer.timeout.connect(lambda: self.boss_confusion3())
        
    def boss_confusion3(self):
        self.spore_label1.move(self.spore_label1.x()-5, self.spore_label1.y())
        self.spore_label2.move(self.spore_label2.x(), self.spore_label2.y()-5)
        self.spore_label3.move(self.spore_label3.x()+5, self.spore_label3.y())
        self.spore_label4.move(self.spore_label4.x(), self.spore_label4.y()+5)
        if self.playerinvicible == False:
            if ULTIMATE_DEFS.collision(self.spore_label1, self.lbl_player) or ULTIMATE_DEFS.collision(self.spore_label2, self.lbl_player) or ULTIMATE_DEFS.collision(self.spore_label3, self.lbl_player) or ULTIMATE_DEFS.collision(self.spore_label4, self.lbl_player):
                if self.confusionvalid == True and self.playerconfused == False:
                    self.confused = QLabel(self.centralwidget)
                    self.confused.setFixedSize(100, 50)
                    self.confused.setPixmap(QPixmap(u"images/confusedeffect.png"))
                    self.confused.setScaledContents(True)
                    self.confused.move(self.lbl_player.x(), self.lbl_player.y()-50)
                    self.confused.setVisible(True)
                    self.playerconfused = True
                    self.confusionvalid = False
                    QTimer.singleShot(10000, lambda: self.boss_confusionend())
                    self.dmg = self.bossclass.rangedattack-self.playerdefense
                    if self.dmg < 0:
                        self.dmg = 0
                    self.playerhealth -= self.dmg
                    self.lbl_healthbar.setFixedSize(self.playerhealth * 4, 41)
                    self.lbl_playerhealth.setText(str(self.playerhealth))
                    if self.playerhealth <= 0:
                        if self.imstillstandingequipped == True and self.imstillstandingused == False and self.TOIcompleted == True and self.BIBcompleted:
                            mixer.music.stop()
                            self.play_music("audio/imstillstanding.mp3")
                            self.imstillstanding()
                        else:
                            self.gameover()
        if self.spore_label1.x() < -100 and self.spore_label2.y() < -100 and self.spore_label3.x() > 1500 and self.spore_label4.y() > 1000:
            self.sporecloudtimer.stop()
            if self.bossdead == False:
                for i, name in enumerate(self.warning_labels):
                    name.deleteLater()
                self.warning_labels.clear()
                self.boss_cooldown()
    
    def boss_confusionend(self):
        self.confused.deleteLater()
        self.playerconfused = False  
                  
#vine cluster
    def vinecluster(self):
        self.vineclustervalid = True
        self.vineclustertimerstarted = False
        self.warning_label1 = QLabel(self.centralwidget)
        self.warning_labels.append(self.warning_label1)
        self.warning_label2 = QLabel(self.centralwidget)
        self.warning_labels.append(self.warning_label2)
        self.warning_label3 = QLabel(self.centralwidget)
        self.warning_labels.append(self.warning_label3)
        self.warning_label4 = QLabel(self.centralwidget)
        self.warning_labels.append(self.warning_label4)
        for i, name in enumerate(self.warning_labels):
            name.setStyleSheet("background-color: rgb(255, 0, 0);")
            name.setVisible(True)
        self.warning_label1.setFixedSize(351, 651)
        self.warning_label2.setFixedSize(261, 121)
        self.warning_label3.setFixedSize(351, 651)
        self.warning_label4.setFixedSize(261, 161)
        self.warning_label1.move(240, 150)
        self.warning_label2.move(590, 150)
        self.warning_label3.move(850, 150)
        self.warning_label4.move(590, 640)
        if self.bossdead == False:
            QTimer.singleShot(2000, lambda: self.vinecluster2())
    
    def vinecluster2(self):
        try:
            if self.bossdead == False:
                for i, name in enumerate(self.warning_labels):
                    name.setPixmap(QPixmap(u"images/vinecluster.png"))
                    name.setScaledContents(True)
                    name.setStyleSheet("")
                    if ULTIMATE_DEFS.collision(name, self.lbl_player):
                        self.bosscollision()
        except:
            pass
        if self.bossdead == False and self.vineclustertimerstarted == False:
            QTimer.singleShot(3000, lambda: self.vinecluster3())
        if self.vineclustervalid == True:
            QTimer.singleShot(500, lambda: self.vinecluster2())
        self.vineclustertimerstarted = True
    
    def vinecluster3(self):
        self.vineclustervalid = False
        if self.bossdead == False:
            for i, name in enumerate(self.warning_labels):
                name.deleteLater()
            self.warning_labels.clear()
            self.boss_cooldown()
            
#hyperbeam
    def hyperbeam(self):
        self.hyperbeamtimerstarted = False
        self.hyperbeamvalid = True
        self.warning_label1 = QLabel(self.centralwidget)
        self.warning_label1.setStyleSheet("background-color: rgb(255, 0, 0);")
        self.warning_label1.setVisible(True)
        self.warning_labels.append(self.warning_label1)
        if self.boss_label.x() > self.lbl_player.x():
            self.warning_label1.setFixedSize(591, 651)
            self.warning_label1.move(0, 150)
            self.hyperbeamimage = "hyperbeam_L.png"
        elif self.boss_label.x() < self.lbl_player.x():
            self.warning_label1.setFixedSize(671, 651)
            self.warning_label1.move(810, 150)
            self.hyperbeamimage = "hyperbeam_R.png"
        if self.bossdead == False:
            QTimer.singleShot(2000, lambda: self.hyperbeam2())
    
    def hyperbeam2(self):
        try:
            if self.bossdead == False:
                self.warning_label1.setPixmap(QPixmap(f"images/{self.hyperbeamimage}"))
                self.warning_label1.setScaledContents(True)
                self.warning_label1.setStyleSheet("")
            if self.playerinvicible == False:
                if ULTIMATE_DEFS.collision(self.warning_label1, self.lbl_player):
                    self.dmg = self.bossclass.rangedattack+-self.playerdefense
                    if self.dmg < 0:
                        self.dmg = 0
                    self.playerhealth -= self.dmg
                    self.lbl_healthbar.setFixedSize(self.playerhealth * 4, 41)
                    self.lbl_playerhealth.setText(str(self.playerhealth))
                    if self.lbl_playerhealth.text() <= "0":
                        if self.imstillstandingequipped == True and self.imstillstandingused == False and self.TOIcompleted == True and self.BIBcompleted:
                            mixer.music.stop()
                            self.play_music("audio/imstillstanding.mp3")
                            self.imstillstanding()
                        else:
                            self.gameover()
        except:
            pass
        if self.bossdead == False and self.hyperbeamtimerstarted == False:
            QTimer.singleShot(5000, lambda: self.hyperbeam3())
        if self.hyperbeamvalid == True:
            QTimer.singleShot(500, lambda: self.hyperbeam2())
        self.hyperbeamtimerstarted = True
    
    def hyperbeam3(self):
        self.hyperbeamvalid = False
        self.warning_labels.clear()
        if self.bossdead == False:
            self.warning_label1.deleteLater()
            self.boss_cooldown()
        
#sporeslam
    def sporeslam(self):
        self.warning_label1 = QLabel(self.centralwidget)
        self.warning_labels.append(self.warning_label1)
        self.warning_label2 = QLabel(self.centralwidget)
        self.warning_labels.append(self.warning_label2)
        self.warning_label3 = QLabel(self.centralwidget)
        self.warning_labels.append(self.warning_label3)
        self.warning_label4 = QLabel(self.centralwidget)
        self.warning_labels.append(self.warning_label4)
        self.warning_label5 = QLabel(self.centralwidget)
        self.warning_labels.append(self.warning_label5)
        self.warning_label6 = QLabel(self.centralwidget)
        self.warning_labels.append(self.warning_label6)
        for i, name in enumerate(self.warning_labels):
            name.setFixedSize(300, 300)
            name.setStyleSheet("background-color: rgb(255, 0, 0);")
            name.setVisible(True)
        self.warning_label1.move(100, 70)
        self.warning_label2.move(100, 570)
        self.warning_label3.move(590, 70)
        self.warning_label4.move(590, 570)
        self.warning_label5.move(1100, 70)
        self.warning_label6.move(1100, 570)
        if self.bossdead == False:
            QTimer.singleShot(1500, lambda: self.sporeslam2())
    
    def sporeslam2(self):
        for i, name in enumerate(self.warning_labels):
            name.setPixmap(QPixmap(u"images/sporeslam.png"))
            name.setScaledContents(True)
            name.setStyleSheet("")
            if ULTIMATE_DEFS.collision(name, self.lbl_player):
                self.bosscollision()
        if self.bossdead == False:
            QTimer.singleShot(300, lambda: self.sporeslam3())
    
    def sporeslam3(self):
        for i, name in enumerate(self.warning_labels):
            name.setVisible(False)
        self.warning_labels.clear()
        self.boss_cooldown()
    
#cooldown
    def boss_cooldown(self):
        self.tired = QLabel(self.centralwidget)
        self.tired.setFixedSize(150, 100)
        self.tired.setPixmap(QPixmap(u"images/exhaustion_clouds.png"))
        self.tired.setScaledContents(True)
        self.tired.move(630, 275)
        self.tired.setVisible(True)
        if self.bossdead == False:
            QTimer.singleShot(1000, lambda: self.attacking_boss())

#collision    
    def bosscollision(self):
        if self.playerinvicible == False:
            self.playerhealth -= self.bossclass.attack+self.playerdefense
            try:
                if self.maxhealth == 100:
                    self.lbl_healthbar.setFixedSize(self.playerhealth * 4, 41)
                elif self.maxhealth == 200:
                    self.lbl_healthbar.setFixedSize(self.playerhealth * 2, 41)
            except:
                pass
            self.lbl_playerhealth.setText(str(self.playerhealth))
            if self.lbl_playerhealth.text() <= "0":
                if self.imstillstandingequipped == True and self.imstillstandingused == False and self.TOIcompleted == True and self.BIBcompleted:
                    mixer.music.stop()
                    self.play_music("audio/imstillstanding.mp3")
                    self.imstillstanding()
                else:
                    self.gameover()
            if self.playerthorns == True:
                self.dmg = (int(self.lbl_bosshealth.text())-3)
                if self.dmg < 0:
                    self.dmg = 0
                self.lbl_bosshealth.setText(str(self.dmg)) #0 cuz there can only be 1 boss
                try:
                    self.lbl_bosshealthbar.setFixedSize(int(self.lbl_bosshealth.text())*2, 41)
                except:
                    pass
                if int(self.lbl_bosshealth.text()) <= 0:
                    self.bossdeath()
#death
    def bossdeath(self):
        #score
        self.score += 10000
        self.lbl_score.setText(str(self.score))
        #miniboss death
        self.bossdead = True
        #miniboss removal
        self.boss_label.deleteLater()
        try:
            self.tired.deleteLater()    
        except:
            pass
        self.boss_labels.remove(self.boss_label)
        self.bossclasslist.remove(self.bossclass)
        #healthbar
        self.lbl_bossname.setVisible(False)
        self.lbl_bosshealth.setVisible(False)
        self.lbl_bosshealthbar.setVisible(False)
        self.lbl_bosshealthbarbg.setVisible(False)
        self.lbl_bossheartnobg.setVisible(False)
        self.lbl_bosshealthbar.setFixedSize(600, 41)
        #removing labels
        while self.warning_labels:
            self.warning_labels[0].deleteLater()
            self.warning_labels.pop(0)
        #timers stopping
        try:
            self.sporecloudtimer.stop()
        except:
            pass
        
#MINIBOSS CODEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE
    def miniboss(self):
        #addinghealthbar
        self.lbl_bosshealth.setVisible(True)
        self.lbl_bosshealthbar.setVisible(True)
        self.lbl_bosshealthbarbg.setVisible(True)
        self.lbl_bossheartnobg.setVisible(True)
        self.lbl_bossname.setVisible(True)
        self.lbl_bossname.setText("The Ghost of the Forest")
        #creation
        self.minibossdead = False
        self.minibossclass = enemies.Miniboss(100, 15, 4, QPixmap(u"images/miniboss_L.png"), 1, 10)
        self.miniboss_label = QLabel(self.centralwidget)
        self.miniboss_label.setFixedSize(100, 150)
        self.miniboss_label.setPixmap(self.minibossclass.pixmap)
        self.miniboss_label.setScaledContents(True)
        self.miniboss_label.move(700, 400)
        self.miniboss_label.setVisible(True)
        self.boss_labels.append(self.miniboss_label)
        self.bossclasslist.append(self.minibossclass)
        self.minibosspixmaptimer = QTimer()
        self.minibosspixmaptimer.start(100)
        self.minibosspixmaptimer.timeout.connect(self.miniboss_pixmap)
        self.attacking_miniboss()
    
    def attacking_miniboss(self):
        if self.minibossdead == False:
            if self.minibossattacknumber > 0:
                self.tired.setVisible(False)
            attack = random.randint(1, 3)
            if attack == 1:
                self.sprintpartH = 1
                self.sprintvalidH = True
                self.miniboss_sprinthorizontal() #sprint attack
            elif attack == 2:
                self.fuzzierangedpart = 1
                self.miniboss_fuzzieranged() #fuzzie inspired ranged attack
            elif attack == 3:
                self.miniboss_sprintvertical()
            self.minibossattacknumber += 1
        
#sprint vertical code
    def miniboss_sprintvertical(self):
        warning_label1 = QLabel(self.centralwidget)
        self.warning_labels.append(warning_label1)
        warning_label2 = QLabel(self.centralwidget)
        self.warning_labels.append(warning_label2)
        warning_label3 = QLabel(self.centralwidget)
        self.warning_labels.append(warning_label3)
        warning_label4 = QLabel(self.centralwidget)
        self.warning_labels.append(warning_label4)
        warning_label5 = QLabel(self.centralwidget)
        self.warning_labels.append(warning_label5)
        for i, name in enumerate(self.warning_labels):
            name.setFixedSize(151, 951)
            name.setStyleSheet("background-color: rgb(255, 0, 0);")
            name.setVisible(True)
        warning_label1.move(40, 0)
        warning_label2.move(350, 0)
        warning_label3.move(660, 0)
        warning_label4.move(970, 0)
        warning_label5.move(1280, 0)
        self.miniboss_label.move(1500, 1500)
        if self.minibossdead == False:
            QTimer.singleShot(1000, lambda: self.miniboss_sprintV2())

    def miniboss_sprintV2(self):
        for i, name in enumerate(self.warning_labels):
            name.deleteLater()
        self.warning_labels.clear()
        self.sprintpartV = 1
        self.sprintvalidV = True
        self.sprinttimerV = QTimer()
        self.sprinttimerV.start(5)
        self.sprinttimerV.timeout.connect(lambda: self.miniboss_sprintV3())
    
    def miniboss_sprintV3(self):
        if self.pausestate == False:
            if self.sprintpartV == 1:
                if self.sprintvalidV == True:
                    self.miniboss_label.move(40, -100)
                    self.sprintvalidV = False
                self.miniboss_label.move(self.miniboss_label.x(), self.miniboss_label.y()+15)
                if self.miniboss_label.y() > 1000:
                    self.sprintpartV = 2
                    self.sprintvalidV = True
            elif self.sprintpartV == 2:
                if self.sprintvalidV == True:
                    self.miniboss_label.move(350, 1000)
                    self.sprintvalidV = False
                self.miniboss_label.move(self.miniboss_label.x(), self.miniboss_label.y()-15)
                if self.miniboss_label.y() < -100:
                    self.sprintpartV = 3
                    self.sprintvalidV = True
            elif self.sprintpartV == 3:
                if self.sprintvalidV == True:
                    self.miniboss_label.move(660, -100)
                    self.sprintvalidV = False
                self.miniboss_label.move(self.miniboss_label.x(), self.miniboss_label.y()+15)
                if self.miniboss_label.y() > 1000:
                    self.sprintpartV = 4
                    self.sprintvalidV = True
            elif self.sprintpartV == 4:
                if self.sprintvalidV == True:
                    self.miniboss_label.move(970, 1000)
                    self.sprintvalidV = False
                self.miniboss_label.move(self.miniboss_label.x(), self.miniboss_label.y()-15)
                if self.miniboss_label.y() < -100:
                    self.sprintpartV = 5
                    self.sprintvalidV = True
            elif self.sprintpartV == 5:
                if self.sprintvalidV == True:
                    self.miniboss_label.move(1280, -100)
                    self.sprintvalidV = False
                self.miniboss_label.move(self.miniboss_label.x(), self.miniboss_label.y()+15)
                if self.miniboss_label.y() > 1000:
                    self.sprinttimerV.stop()
                    self.miniboss_label.move(700, 400)
                    self.miniboss_cooldown()
            self.minibossattackcollision()
        
#ranged code
    def miniboss_fuzzieranged(self):
        warning_label1 = QLabel(self.centralwidget)
        self.warning_labels.append(warning_label1)
        warning_label2 = QLabel(self.centralwidget)
        self.warning_labels.append(warning_label2)
        warning_label3 = QLabel(self.centralwidget)
        self.warning_labels.append(warning_label3)
        warning_label4 = QLabel(self.centralwidget)
        self.warning_labels.append(warning_label4)
        for i, name in enumerate(self.warning_labels):
            name.setStyleSheet("background-color: rgb(255, 0, 0);")
            name.setVisible(True)
        warning_label1.setFixedSize(1381, 131)
        warning_label2.setFixedSize(151, 591)
        warning_label3.setFixedSize(1381, 131)
        warning_label4.setFixedSize(151, 591)
        warning_label1.move(50, 50)
        warning_label2.move(50, 180)
        warning_label3.move(50, 770)
        warning_label4.move(1280, 180)
        self.miniboss_label.move(1500, 1500)
        for i, name in enumerate(self.ui):
            name.raise_()
        if self.minibossdead == False:
            QTimer.singleShot(1000, lambda: self.miniboss_fuzzieranged2())
    
    def miniboss_fuzzieranged2(self):
        for i, name in enumerate(self.warning_labels):
            name.deleteLater()
        self.warning_labels.clear()
        self.miniboss_label.move(50, 50)
        for i, name in enumerate(self.ui):
            name.raise_()
        self.miniboss_fuzzierangedtimer = QTimer()
        self.miniboss_fuzzierangedtimer.start(1000)
        self.miniboss_fuzzierangedtimer.timeout.connect(lambda: self.fuzzies_ranged_attack())
        self.fuzzierangedtimer = QTimer()
        self.fuzzierangedtimer.start(10)
        self.fuzzierangedtimer.timeout.connect(lambda: self.miniboss_fuzzieranged3())
        
    def miniboss_fuzzieranged3(self):
        if self.pausestate == False:
            if self.fuzzierangedpart == 1:
                self.miniboss_label.move(self.miniboss_label.x(), self.miniboss_label.y()+5)
                if self.miniboss_label.y() > 750:
                    self.fuzzierangedpart = 2
            elif self.fuzzierangedpart == 2:
                self.miniboss_label.move(self.miniboss_label.x()+5, self.miniboss_label.y())
                if self.miniboss_label.x() > 1300:
                    self.fuzzierangedpart = 3
            elif self.fuzzierangedpart == 3:
                self.miniboss_label.move(self.miniboss_label.x(), self.miniboss_label.y()-5) 
                if self.miniboss_label.y() < 130:
                    self.fuzzierangedpart = 4
            elif self.fuzzierangedpart == 4:
                self.miniboss_label.move(self.miniboss_label.x()-5, self.miniboss_label.y())
                if self.miniboss_label.x() < 50:
                    self.fuzzierangedpart = 5
            elif self.fuzzierangedpart == 5:
                self.fuzzierangedtimer.stop()
                self.miniboss_fuzzierangedtimer.stop()
                self.miniboss_label.move(700, 400)
                self.miniboss_cooldown()
            self.minibossattackcollision()
    
    def fuzzies_ranged_attack(self):
        self.fuzzievalid = True
        self.fuzzie = QLabel(self.centralwidget)
        self.fuzzie.setFixedSize(50, 50)
        self.fuzzie.setPixmap(QPixmap(u"images/fuzzie.png"))
        self.fuzzie.setScaledContents(True)
        self.fuzzie.setVisible(True)
        self.fuzzie.move(self.miniboss_label.x(), self.miniboss_label.y())
        #getting difference between player and enemy
        difference_x = self.lbl_player.x() - self.miniboss_label.x()
        difference_y = self.lbl_player.y() - self.miniboss_label.y()
        #setting base x and y
        self.fuzzieX = 0
        self.fuzzieY = 0
        #abs value ensures it only pops if needed
        if abs(difference_x) > 100 and self.lbl_player.x() > self.miniboss_label.x():        
            self.fuzzieX = 10
        elif abs(difference_x) > 100 and self.lbl_player.x() < self.miniboss_label.x():
            self.fuzzieX = -10
        if abs(difference_y) > 100 and self.lbl_player.y() > self.miniboss_label.y():
            self.fuzzieY = 10 
        elif abs(difference_y) > 100 and self.lbl_player.y() < self.miniboss_label.y():    
            self.fuzzieY = -10
        self.fuzzieattacktimer = QTimer()
        self.fuzzieattacktimer.start(5)
        self.fuzzieattacktimer.timeout.connect(lambda: self.fuzzies_ranged_movement())

    def fuzzies_ranged_movement(self):
        if self.fuzzievalid == True:
            self.fuzzie.move(self.fuzzie.x() + self.fuzzieX, self.fuzzie.y() + self.fuzzieY)
            if self.fuzzie.x() < 0 or self.fuzzie.x() > 1420 or self.fuzzie.y() < 0 or self.fuzzie.y() > 950:
                self.fuzzieattacktimer.stop()
                self.fuzzie.setVisible(False)
                self.fuzzie.deleteLater()
                self.fuzzievalid = False
            if self.playerinvicible == False:
                if ULTIMATE_DEFS.collision(self.lbl_player, self.fuzzie):
                    if self.pausestate == False:
                        self.fuzzieattacktimer.stop()
                        self.fuzzie.setVisible(False)
                        self.fuzzie.deleteLater()
                        self.fuzzievalid = False
                        self.dmg = self.minibossclass.rangedattack-self.playerdefense
                        if self.dmg < 0:
                            self.dmg = 0
                        self.playerhealth -= self.dmg
                        try:
                            self.lbl_healthbar.setFixedSize(self.playerhealth * 4, 41)
                        except:
                            pass
                        self.lbl_playerhealth.setText(str(self.playerhealth))
                        if self.lbl_playerhealth.text() <= "0":
                            if self.imstillstandingequipped == True and self.imstillstandingused == False and self.TOIcompleted == True and self.BIBcompleted:
                                mixer.music.stop()
                                self.play_music("audio/imstillstanding.mp3")
                                self.imstillstanding()
                            else:
                                self.gameover()
        
#sprinting code 
    def miniboss_sprinthorizontal(self):
        warning_label1 = QLabel(self.centralwidget)
        self.warning_labels.append(warning_label1)
        warning_label2 = QLabel(self.centralwidget)
        self.warning_labels.append(warning_label2)
        warning_label3 = QLabel(self.centralwidget)
        self.warning_labels.append(warning_label3)
        for i, name in enumerate(self.warning_labels):
            name.setFixedSize(1471, 151)
            name.setStyleSheet("background-color: rgb(255, 0, 0);")
            name.setVisible(True)
        warning_label1.move(0, 130)
        warning_label2.move(0, 430)
        warning_label3.move(0, 730)
        self.miniboss_label.move(1500, 1500)
        if self.minibossdead == False:
            QTimer.singleShot(1000, lambda: self.miniboss_sprinthorizontal2())

    def miniboss_sprinthorizontal2(self):
        for i, name in enumerate(self.warning_labels):
            name.deleteLater()
        self.warning_labels.clear()
        self.sprinttimerH = QTimer()
        self.sprinttimerH.start(5)
        self.sprinttimerH.timeout.connect(lambda: self.miniboss_sprinthorizontal3())
    
    def miniboss_sprinthorizontal3(self):
        if self.pausestate == False:
            if self.sprintpartH == 1:
                if self.sprintvalidH == True:
                    self.miniboss_label.move(1550, 130)
                    self.sprintvalidH = False
                self.miniboss_label.move(self.miniboss_label.x()-15, self.miniboss_label.y())
                if self.miniboss_label.x() < -100:
                    self.sprintpartH = 2
                    self.sprintvalidH = True
            elif self.sprintpartH == 2:
                if self.sprintvalidH == True:
                    self.miniboss_label.move(-100, 430)
                    self.sprintvalidH = False
                self.miniboss_label.move(self.miniboss_label.x()+15, self.miniboss_label.y())
                if self.miniboss_label.x() > 1470:
                    self.sprintpartH = 3
                    self.sprintvalidH = True
            elif self.sprintpartH == 3:
                if self.sprintvalidH == True:
                    self.miniboss_label.move(1550, 730)
                    self.sprintvalidH = False
                self.miniboss_label.move(self.miniboss_label.x()-15, self.miniboss_label.y())
                if self.miniboss_label.x() < -100:
                    self.sprinttimerH.stop()
                    self.miniboss_label.move(700, 400)
                    self.miniboss_cooldown()
            self.minibossattackcollision()
    
    def minibossattackcollision(self):
        if self.playerinvicible == False:
            if ULTIMATE_DEFS.collision(self.lbl_player, self.miniboss_label):
                self.dmg = self.minibossclass.attack+-self.playerdefense
                if self.dmg < 0:
                    self.dmg = 0
                self.playerhealth -= self.dmg
                try:
                    if self.maxhealth == 100:
                        self.lbl_healthbar.setFixedSize(self.playerhealth * 4, 41)
                    elif self.maxhealth == 200:
                        self.lbl_healthbar.setFixedSize(self.playerhealth * 2, 41)
                except:
                    pass
                self.lbl_playerhealth.setText(str(self.playerhealth))
                if self.minibosspixmap == 1:
                    self.lbl_player.move(self.lbl_player.x()+100, self.lbl_player.y()+100)
                    for i, attack in enumerate(self.attack_list):
                        attack.move(attack.x()+100, attack.y()+100)
                elif self.minibosspixmap == 2:
                    self.lbl_player.move(self.lbl_player.x()-100, self.lbl_player.y()-100)
                    for i, attack in enumerate(self.attack_list):
                        attack.move(attack.x()-100, attack.y()-100)
                if self.playerthorns == True:
                    self.lbl_bosshealth.setText(str(int(self.lbl_bosshealth.text())-3)) #0 cuz there can only be 1 boss
                    try:
                        self.lbl_bosshealthbar.setFixedSize(int(self.lbl_bosshealth.text())*6, 41)
                    except:
                        pass
                    if int(self.lbl_bosshealth.text()) <= 0:
                        self.minibossdeath()
                if self.lbl_playerhealth.text() <= "0":
                    if self.imstillstandingequipped == True and self.imstillstandingused == False and self.TOIcompleted == True and self.BIBcompleted:
                        mixer.music.stop()
                        self.play_music("audio/imstillstanding.mp3")
                        self.imstillstanding()
                    else:
                        self.gameover()
        
#cooldown
    def miniboss_cooldown(self):
        self.tired = QLabel(self.centralwidget)
        self.tired.setFixedSize(100, 50)
        self.tired.setPixmap(QPixmap(u"images/exhaustion_clouds.png"))
        self.tired.setScaledContents(True)
        self.tired.move(700, 400)
        self.tired.setVisible(True)
        if self.minibossdead == False:
            try:
                QTimer.singleShot(3000, lambda: self.attacking_miniboss())
            except:
                pass

#miniboss pixmap

    def miniboss_pixmap(self):
        if self.miniboss_label.x() < self.lbl_player.x():
            self.miniboss_label.setPixmap(QPixmap(u"images/miniboss_R.png"))
            self.minibosspixmap = 1
        elif self.miniboss_label.x() > self.lbl_player.x():
            self.miniboss_label.setPixmap(QPixmap(u"images/miniboss_L.png"))
            self.minibosspixmap = 2
            
#death
    def minibossdeath(self):
        #miniboss death
        self.minibossdead = True
        #miniboss removal
        self.miniboss_label.deleteLater()
        try:
            self.tired.deleteLater()    
        except:
            pass
        self.boss_labels.remove(self.miniboss_label)
        self.bossclasslist.remove(self.minibossclass)
        #healthbar
        self.lbl_bossname.setVisible(False)
        self.lbl_bosshealth.setVisible(False)
        self.lbl_bosshealthbar.setVisible(False)
        self.lbl_bosshealthbarbg.setVisible(False)
        self.lbl_bossheartnobg.setVisible(False)
        self.lbl_bosshealthbar.setFixedSize(600, 41)
        #timers stopping
        try: #need the try except because timers could be non or off
            self.minibosspixmaptimer.stop()
        except:
            pass
        try:
            self.sprinttimerH.stop()
        except:
            pass
        try:
            self.sprinttimerV.stop()
        except:
            pass
        try:
            self.miniboss_fuzzierangedtimer.stop()
        except:
            pass
        try:
            self.fuzzierangedtimer.stop()
        except:
            pass
        try:
            self.fuzzieattacktimer.stop()
        except:
            pass
        #score
        self.score += 5000
        self.lbl_score.setText(str(self.score))
        
        
#ENEMY CODEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE
    #enemy creation
    
    def enemy_creation(self, enemyint):
        if self.pausestate == False:
            if enemyint == 3:
                self.sonic_label = QLabel(self.centralwidget)
                self.sonichp_label = QLabel(self.centralwidget)
                randx = random.randint(200, 1200)
                randy = random.randint(100, 800)
                self.sonic_label.move(randx, randy)
                self.sonichp_label.move(randx+38, randy-32)
                self.sonic_label.setFixedSize(100, 100)
                self.sonichp_label.setFixedSize(40, 40)
                self.sonic_label.setPixmap(self.sonic.pixmap)
                self.sonic_label.setScaledContents(True)
                self.sonic_label.setVisible(True)
                self.sonichp_label.setVisible(True)
                self.sonichp_label.setText(f"{self.sonic.health}")
                font = self.sonichp_label.font()
                font.setPointSize(12)
                font.setBold(True)
                self.sonichp_label.setFont(font)
                self.enemylabels_list.append(self.sonic_label)
                self.enemyhplabels_list.append(self.sonichp_label)
                self.enemyintlist.append(enemyint)
                self.enemyclass_list.append(self.sonic)
            else:
                self.true = True
                # Create a Label
                enemy = self.allenemies[enemyint]
                enemy_label = QLabel(self.centralwidget)
                enemyhp_label = QLabel(self.centralwidget)
                #scaled contents
                randx = random.randint(200, 1200)
                randy = random.randint(100, 800)
                enemy_label.setScaledContents(True)
                enemyhp_label.setFixedSize(40, 40)
                #each enemy
                if enemyint == 0:
                    enemy_label.setFixedSize(80, 80)
                    enemy_label.setPixmap(self.slime.pixmap)
                    enemy_label.move(randx, randy)
                    enemyhp_label.move(randx+30, randy+8)
                elif enemyint == 1:
                    enemy_label.setFixedSize(50, 100)
                    enemy_label.setPixmap(self.hauntedarmor.pixmap)
                    enemy_label.move(randx, randy)
                    enemyhp_label.move(randx+30, randy-30)
                elif enemyint == 2:
                    enemy_label.setFixedSize(60, 60)
                    enemy_label.setPixmap(self.mage.pixmap)
                    enemy_label.move(randx, randy)
                    enemyhp_label.move(randx+25, randy-30)
                elif enemyint == 4:
                    enemy_label.setFixedSize(200, 200)
                    enemy_label.setPixmap(self.tangela.pixmap)
                    while self.true:
                        randx = random.randint(-400, 400)
                        randy = random.randint(-400, 400)
                        self.true = False
                        if randx in self.tangelalist or randy in self.tangelalist:
                            self.true = True
                    enemy_label.move(self.lbl_player.x()+randx, self.lbl_player.y()+randy)
                # moving labels
                if self.bossdead == False and self.lbl_wave.text() == 10:
                    self.enemyrandx = random.choice([100, 1100])
                    self.enemyrandy = random.choice([70, 570])
                    enemy_label.move(self.enemyrandx, self.enemyrandy)
                    if enemyint == 0:
                        enemyhp_label.move(self.enemyrandx+30, self.enemyrandy+8)
                    elif enemyint == 1:
                        enemyhp_label.move(self.enemyrandx+30, self.enemyrandy-30)
                    elif enemyint == 2:
                        enemyhp_label.move(self.enemyrandx+25, self.enemyrandy-30)
                    elif enemyint == 4:
                        enemyhp_label.move(self.enemyrandx+100, self.enemyrandy-30)
                #font setting
                enemyhp_label.setText(f"{enemy.health}")
                font = enemyhp_label.font()
                font.setPointSize(12)
                font.setBold(True)
                enemyhp_label.setFont(font)
                #visibility  
                enemy_label.setVisible(True)
                enemyhp_label.setVisible(True)
                #appending to lists
                self.enemyclass_list.append(enemy)
                self.enemylabels_list.append(enemy_label)
                self.enemyhplabels_list.append(enemyhp_label)
                self.enemyintlist.append(enemyint)
                enemyhp_label.move(randx+30, randy+8)
            
    def sonic_movement(self):
        try:
            if self.sonicIN == True:
                #setting base values
                randx = -50
                randy = -50
                #warning label
                warning_label1 = QLabel(self.centralwidget)
                #either x or y axis to spawn from
                XorY = random.randint(1,2)
                if XorY == 1:
                    warning_label1.setFixedSize(100, 1200) #self.enemywidth of sonic and self.enemyheight of screen 
                    warning_label1.move(self.lbl_player.x(), 0)
                    self.sonic_label.move(self.lbl_player.x(), -50)
                    self.sonichp_label.move(self.lbl_player.x(), -82)
                elif XorY == 2:
                    randy = random.randint(100, 800)
                    warning_label1.setFixedSize(1700, 100) #self.enemyheight of sonic and self.enemywidth of screen
                    warning_label1.move(0, self.lbl_player.y())
                    self.sonichp_label.move(12, self.lbl_player.y()-32)
                    self.sonic_label.move(-50, self.lbl_player.y())
                warning_label1.setStyleSheet("background-color: rgb(255, 0, 0);")
                warning_label1.setVisible(True)
                QTimer.singleShot(750, lambda: self.sonic_hidinglabels(warning_label1, XorY))
            QTimer.singleShot(3000, lambda: self.sonic_movement())
        except:
            pass
        
    def sonic_hidinglabels(self, warning_label1, XorY):
        warning_label1.setVisible(False)
        self.sonictimer = QTimer()
        self.sonictimer.start(5)
        self.sonictimer.timeout.connect(lambda: self.sonic_attack(XorY))
    
    def sonic_attack(self, XorY):
        try:
            if XorY == 1:
                self.sonic_label.move(self.sonic_label.x(), self.sonic_label.y()+25)
                self.sonichp_label.move(self.sonichp_label.x(), self.sonichp_label.y()+25)
            elif XorY == 2:
                self.sonic_label.move(self.sonic_label.x()+25, self.sonic_label.y())
                self.sonichp_label.move(self.sonichp_label.x()+25, self.sonichp_label.y())
            if self.sonic_label.x() > 1500 or self.sonic_label.y() > 1000:
                self.sonictimer.stop()
                randx = random.randint(200, 1200)
                randy = random.randint(100, 800)
                self.sonic_label.move (randx, randy)
                self.sonichp_label.move(randx+38, randy-32)
            if self.invincible == False:
                if ULTIMATE_DEFS.collision(self.lbl_player, self.sonic_label):
                    self.sonictimer.stop()
                    randx = random.randint(200, 1200)
                    randy = random.randint(100, 800)
                    self.sonic_label.move (randx, randy)
                    self.sonichp_label.move(randx+38, randy-32)
                    self.dmg = self.sonic.attack-self.playerdefense
                    if self.dmg < 0:
                        self.dmg = 0
                    self.playerhealth -= self.dmg
                    try:
                        if self.maxhealth == 100:
                            self.lbl_healthbar.setFixedSize(self.playerhealth * 4, 41)
                        elif self.maxhealth == 200:
                            self.lbl_healthbar.setFixedSize(self.playerhealth * 2, 41)
                        self.lbl_playerhealth.setText(str(self.playerhealth))
                    except:
                        pass
                    if self.playerthorns == True:
                        self.sonichp_label.setText(str(int(self.sonichp_label.text())-3)) 
                        if int(self.sonichp_label.text()) <= 0:
                            for i, name in enumerate(self.enemyintlist):
                                if self.enemyintlist[i] == 3:
                                    self.enemydeath(i)
                    if self.lbl_playerhealth.text() <= "0":
                        if self.imstillstandingequipped == True and self.imstillstandingused == False and self.TOIcompleted == True and self.BIBcompleted:
                            mixer.music.stop()
                            self.play_music("audio/imstillstanding.mp3")
                            self.imstillstanding()
                        else:
                            self.gameover()
        except:
            pass
        
    def enemy_movement(self):
        #checks if there are actually enemies in 
        if self.enemylabels_list != [] and self.pausestate == False:
            for i, enemy in enumerate(self.enemylabels_list):
                if self.enemyintlist[i] != 3:
                    #getting speed
                    speed = self.enemyclass_list[i].speed
                    #getting attack
                    attack = self.enemyclass_list[i].attack
                    #grabbing hp labels
                    hplabel = self.enemyhplabels_list[i]
                    #getting x and y and moving in direction
                    if self.enemyintlist[i] != 2:
                        try:
                            if self.thickofitmovement == False:
                                if enemy.x() < self.lbl_player.x():
                                    #anything else moves towards
                                    enemy.move(enemy.x()+speed,enemy.y())
                                    hplabel.move(hplabel.x()+speed, hplabel.y())
                                    x = -100
                                    y = 0
                                if enemy.x() > self.lbl_player.x():
                                    #anything else moves towards
                                    enemy.move(enemy.x()-speed,enemy.y())
                                    hplabel.move(hplabel.x()-speed, hplabel.y())
                                    x = 100
                                    y = 0
                                if enemy.y() < self.lbl_player.y():
                                    #anything else moves towards
                                    enemy.move(enemy.x(),enemy.y()+speed)
                                    hplabel.move(hplabel.x(), hplabel.y()+speed)
                                    x = 0
                                    y = -100
                                if enemy.y() > self.lbl_player.y():
                                    #anything else moves towards
                                    enemy.move(enemy.x(),enemy.y()-speed)
                                    hplabel.move(hplabel.x(), hplabel.y()-speed)
                                    x = 0
                                    y = 100
                        except:
                            pass
                        try:
                            if self.thickofitmovement == True:
                                if enemy.x() < self.lbl_player.x():
                                    #anything else moves towards
                                    enemy.move(enemy.x()-speed,enemy.y())
                                    hplabel.move(hplabel.x()-speed, hplabel.y())
                                    x = -100
                                    y = 0
                                if enemy.x() > self.lbl_player.x():
                                    #anything else moves towards
                                    enemy.move(enemy.x()+speed,enemy.y())
                                    hplabel.move(hplabel.x()+speed, hplabel.y())
                                    x = 100
                                    y = 0
                                if enemy.y() < self.lbl_player.y():
                                    #anything else moves towards
                                    enemy.move(enemy.x(),enemy.y()-speed)
                                    hplabel.move(hplabel.x(), hplabel.y()-speed)
                                    x = 0
                                    y = -100
                                if enemy.y() > self.lbl_player.y():
                                    #anything else moves towards
                                    enemy.move(enemy.x(),enemy.y()+speed)
                                    hplabel.move(hplabel.x(), hplabel.y()+speed)
                                    x = 0
                                    y = 100
                                if enemy.x() < 30:
                                    enemy.move(700, enemy.y())
                                    if self.enemyintlist[i] == 0:
                                        hplabel.move(700+30, hplabel.y())
                                    elif self.enemyintlist[i] == 1:
                                        hplabel.move(700+30, hplabel.y())
                                if enemy.x() > 1380:
                                    enemy.move(700, enemy.y())
                                    if self.enemyintlist[i] == 0:
                                        hplabel.move(700+30, hplabel.y())
                                    elif self.enemyintlist[i] == 1:
                                        hplabel.move(700+30, hplabel.y())
                                if enemy.y() < 30:
                                    enemy.move(enemy.x(), 400)
                                    if self.enemyintlist[i] == 0:
                                        hplabel.move(hplabel.x(), 400+8)
                                    elif self.enemyintlist[i] == 1:
                                        hplabel.move(hplabel.x(), 400-30)
                                if enemy.y() > 850:
                                    enemy.move(enemy.x(), 400)
                                    if self.enemyintlist[i] == 0:
                                        hplabel.move(hplabel.x(), 400+8)
                                    elif self.enemyintlist[i] == 1:
                                        hplabel.move(hplabel.x(), 400-30)
                        except:
                            pass
                    elif self.enemyintlist[i] == 2: #mage movement
                        try:
                            if enemy.x() < self.lbl_player.x():
                                enemy.move(enemy.x()-speed,enemy.y())
                                hplabel.move(hplabel.x()-speed, hplabel.y())
                                x = 100
                                y = 0
                            if enemy.x() > self.lbl_player.x():
                                enemy.move(enemy.x()+speed,enemy.y())
                                hplabel.move(hplabel.x()+speed, hplabel.y())
                                x = -100
                                y = 0
                            if enemy.y() < self.lbl_player.y():
                                enemy.move(enemy.x(),enemy.y()-speed)
                                hplabel.move(hplabel.x(), hplabel.y()-speed)
                                x = 0
                                y = 100
                            if enemy.y() > self.lbl_player.y():
                                enemy.move(enemy.x(),enemy.y()+speed)
                                hplabel.move(hplabel.x(), hplabel.y()+speed)
                                x = 0
                                y = -100
                        except:
                            pass
                        #if mage gets to borders
                        try:
                            if enemy.x() < 30:
                                enemy.move(enemy.x()+speed, enemy.y())
                                hplabel.move(hplabel.x()+speed, hplabel.y())
                            if enemy.x() > 1380:
                                enemy.move(enemy.x()-speed, enemy.y())
                                hplabel.move(hplabel.x()-speed, hplabel.y())
                            if enemy.y() < 30:
                                enemy.move(enemy.x(), enemy.y()+speed)
                                hplabel.move(hplabel.x(), hplabel.y()+speed)
                            if enemy.y() > 850:
                                enemy.move(enemy.x(), enemy.y()-speed)
                                hplabel.move(hplabel.x(), hplabel.y()-speed)
                        except:
                            pass
                    #code for collision and dealing damage
                    if self.playerinvicible == False:
                        if ULTIMATE_DEFS.collision(self.lbl_player, enemy):
                            if self.enemyintlist[i] != 2 and self.enemyintlist[i] != 4:
                                enemy.move(enemy.x()+x, enemy.y()+y)
                                hplabel.move(hplabel.x()+x, hplabel.y()+y)
                            elif self.enemyintlist[i] == 2:
                                self.lbl_player.move(self.lbl_player.x()+x, self.lbl_player.y()+y)
                                for i, name in enumerate(self.attack_list):
                                    self.attack_list[i].move(self.attack_list[i].x()+x, self.attack_list[i].y()+y)
                                if self.playerconfused == True:
                                    self.confusion.move(self.confusion.x()+x, self.confusion.y()+y)
                            elif self.enemyintlist[i] == 4:
                                self.lbl_player.move(self.lbl_player.x()-x, self.lbl_player.y()-y)
                                for i, name in enumerate(self.attack_list):
                                    self.attack_list[i].move(self.attack_list[i].x()-x, self.attack_list[i].y()-y)
                                if self.playerconfused == True:
                                    self.confusion.move(self.confusion.x()-x, self.confusion.y()-y)
                            self.dmg = attack-self.playerdefense
                            if self.dmg < 0:
                                self.dmg = 0
                            self.playerhealth -= self.dmg
                            try:
                                if self.maxhealth == 100:
                                    self.lbl_healthbar.setFixedSize(self.playerhealth * 4, 41)#the times four is because self.playerhealth is 4 times as big as the players hp
                                elif self.maxhealth == 200:
                                    self.lbl_healthbar.setFixedSize(self.playerhealth * 2, 41) 
                            except:
                                pass
                            self.lbl_playerhealth.setText(str(self.playerhealth))
                            if self.playerthorns == True:
                                self.enemyhplabels_list[i].setText(str(int(self.enemyhplabels_list[i].text())-3)) 
                                if int(self.enemyhplabels_list[i].text()) <= 0:
                                    self.enemydeath(i)
                            if self.lbl_playerhealth.text() <= "0":
                                if self.imstillstandingequipped == True and self.imstillstandingused == False and self.TOIcompleted == True and self.BIBcompleted:
                                    mixer.music.stop()
                                    self.play_music("audio/imstillstanding.mp3")
                                    self.imstillstanding()
                                else:
                                    self.gameover()
                    
    def enemydeath(self, i):
        #score
        self.score += 500
        self.lbl_score.setText(str(self.score))
        #deletion
        self.enemylabels_list[i].deleteLater()
        self.enemyhplabels_list[i].deleteLater()
        self.enemyclass_list.pop(i)
        self.enemylabels_list.pop(i)
        self.enemyhplabels_list.pop(i)
        self.enemyintlist.pop(i)
    

    def enemy_ranged_attacks(self):
        for i, enemy in enumerate(self.enemylabels_list):
            if self.enemyintlist[i] == 2:  # Check if the enemy is a mage
                self.enemy_rangedvalid = True
                #creation
                fireball = QLabel(self.centralwidget)
                #setting size
                fireball.setFixedSize(50, 50)
                #pixmap and scaled contents
                fireball.setPixmap(QPixmap(u"images/fireball.jpeg"))
                fireball.setScaledContents(True)
                #moving to enemy and visibility
                fireball.move(enemy.x(), enemy.y())
                fireball.setVisible(True)
                #timer for movement of fireball (i=i and fireball=fireball are used to ensure ranged_movement calls the right values)
                try:
                    self.fireball_timers[i].stop()
                    self.fireball_timers[i].timeout.connect(lambda i=i, fireball=fireball: self.enemy_ranged_movement(i, fireball))
                    self.fireball_timers[i].start(10)
                except:
                    pass
                #appending timer
        #cooldown
        QTimer.singleShot(5000, self.enemy_ranged_attacks)

    def enemy_ranged_movement(self, i, fireball): 
        self.fireball_list.append(fireball)
        if self.enemy_rangedvalid == True: #ensures that the enemy is still alive
            #setting base x and y
            self.enemyrangedX = 0
            self.enemyrangedY = 0
            #getting difference between player and enemy
            try:
                difference_x = self.lbl_player.x() - self.enemylabels_list[i].x()
                difference_y = self.lbl_player.y() - self.enemylabels_list[i].y()
                #abs value ensures it only pops if needed
                if abs(difference_x) > 100 and self.lbl_player.x() > self.enemylabels_list[i].x():        
                    self.enemyrangedX = 10
                elif abs(difference_x) > 100 and self.lbl_player.x() < self.enemylabels_list[i].x():
                    self.enemyrangedX = -10
                if abs(difference_y) > 100 and self.lbl_player.y() > self.enemylabels_list[i].y():
                    self.enemyrangedY = 10
                elif abs(difference_y) > 100 and self.lbl_player.y() < self.enemylabels_list[i].y():    
                    self.enemyrangedY = -10
            except:
                pass
            try:
                    #moving fireball
                fireball.move(fireball.x() + self.enemyrangedX, fireball.y() + self.enemyrangedY)
            except:
                pass
            try:
                if self.playerinvicible == False:
                    if ULTIMATE_DEFS.collision(self.lbl_player, fireball):
                        self.fireball_timers[i].stop()
                        fireball.setVisible(False)
                        self.dmg = self.enemyclass_list[i].rangedattack-self.playerdefense
                        if self.dmg < 0:
                            self.dmg = 0
                        self.playerhealth -= self.dmg
                        try:
                            if self.maxhealth == 100:
                                self.lbl_healthbar.setFixedSize(self.playerhealth * 4, 41)#the times four is because self.playerhealth is 4 times as big as the players hp
                            elif self.maxhealth == 200:
                                self.lbl_healthbar.setFixedSize(self.playerhealth * 2, 41) 
                        except:
                            pass
                        self.lbl_playerhealth.setText(str(self.playerhealth))
                        if self.lbl_playerhealth.text() <= "0":
                            if self.imstillstandingequipped == True and self.imstillstandingused == False and self.TOIcompleted == True and self.BIBcompleted:
                                mixer.music.stop()
                                self.play_music("audio/imstillstanding.mp3")
                                self.imstillstanding()
                            else:
                                self.gameover()
            except:
                pass
            #fireball going offscreen
            try:
                if fireball.x() < -50 or fireball.x() > 1420 or fireball.y() < -50 or fireball.y() > 950:
                    self.fireball_timers[i].stop()
                    fireball.setVisible(False)
            except:
                pass

                
#KEYBIND CODEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE
    def keyPressEvent(self, event):
        if event.key() not in self.keypress:
            self.keypress.append(event.key())
        #esc button for esc menu
        if event.key() == Qt.Key.Key_Escape:
            self.pausestate = True
            for i, button in enumerate(self.pause_buttons):
                button.setVisible(True)
                button.raise_()
        #enter button for pressing dialogue
        if self.enter == True:
            if event.key() == Qt.Key.Key_Return:
                self.itemchoicevalidness = True
                self.dialogue()
        #ability buttons (im still standing is auto activated so it doesnt need a keybind)
        if event.key() == Qt.Key.Key_Z:
            if self.disc1 == "backinblack" and self.backinblackequipped == True and self.backinblackused == False and self.TOIcompleted == True and self.ISScompleted == True and self.SHScompleted == True:
                mixer.music.stop()
                self.play_music("audio/backinblack.mp3")
                self.backinblack()
            if self.disc1 == "thickofit" and self.thickofitequipped == True and self.thickofitused == False and self.BIBcompleted == True and self.ISScompleted == True and self.SHScompleted == True:
                mixer.music.stop()
                self.play_music("audio/thickofit.mp3")
                self.thickofit()
            if self.enemylabels_list != [] or self.boss_labels != []:
                print(self.sixhundredstrikeused)
                print(self.disc1)
                print(self.sixhundredstrikeequipped)
                if self.disc1 == "sixhundredstrike" and self.sixhundredstrikeequipped == True and self.sixhundredstrikeused == False and self.BIBcompleted == True and self.ISScompleted == True and self.TOIcompleted == True:
                    mixer.music.stop()
                    self.play_music("audio/sixhundredstrike.mp3")
                    self.sixhundredstrike()                        
        if event.key() == Qt.Key.Key_X:
            if self.disc2 == "backinblack" and self.backinblackequipped == True and self.backinblackused == False and self.TOIcompleted == True and self.ISScompleted == True and self.SHScompleted == True:
                mixer.music.stop()
                self.play_music("audio/backinblack.mp3")
                self.backinblack()
            if self.disc2 == "thickofit" and self.thickofitequipped == True and self.thickofitused == False and self.BIBcompleted == True and self.ISScompleted == True and self.SHScompleted == True:
                mixer.music.stop()
                self.play_music("audio/thickofit.mp3")
                self.thickofit()
            if self.enemylabels_list != [] or self.boss_labels != []:
                if self.disc2 == "sixhundredstrike" and self.sixhundredstrikeequipped == True and self.sixhundredstrikeused == False and self.BIBcompleted == True and self.ISScompleted == True and self.TOIcompleted == True:
                    mixer.music.stop()
                    self.play_music("audio/sixhundredstrike.mp3")
                    self.sixhundredstrike()  
        if event.key() == Qt.Key.Key_C:
            if self.disc3 == "backinblack" and self.backinblackequipped == True and self.backinblackused == False and self.TOIcompleted == True and self.ISScompleted == True and self.SHScompleted == True:
                mixer.music.stop()
                self.play_music("audio/backinblack.mp3")
                self.backinblack()
            if self.disc3 == "thickofit" and self.thickofitequipped == True and self.thickofitused == False and self.BIBcompleted == True and self.ISScompleted == True and self.SHScompleted == True:
                mixer.music.stop()
                self.play_music("audio/thickofit.mp3")
                self.thickofit()
            if self.enemylabels_list != [] or self.boss_labels != []:
                if self.disc3 == "sixhundredstrike" and self.sixhundredstrikeequipped == True and self.sixhundredstrikeused == False and self.BIBcompleted == True and self.ISScompleted == True and self.TOIcompleted == True:
                    mixer.music.stop()
                    self.play_music("audio/sixhundredstrike.mp3")
                    self.sixhundredstrike()  
        #choosing which way character is facing
        #topleft
        if Qt.Key.Key_A in self.keypress and Qt.Key.Key_W in self.keypress:
            self.lbl_player.setPixmap(QPixmap(u"images/character_topL_8.png"))
            self.attacknumber = 8
        #topright
        elif Qt.Key.Key_D in self.keypress and Qt.Key.Key_W in self.keypress:
            self.lbl_player.setPixmap(QPixmap(u"images/character_topR_2.png"))
            self.attacknumber = 2
        #bottomleft
        elif Qt.Key.Key_S in self.keypress and Qt.Key.Key_A in self.keypress:
            self.lbl_player.setPixmap(QPixmap(u"images/character_bottomL_6.png"))
            self.attacknumber = 6
        #bottomright
        elif Qt.Key.Key_S in self.keypress and Qt.Key.Key_D in self.keypress:
            self.lbl_player.setPixmap(QPixmap(u"images/character_bottomR_4.png"))
            self.attacknumber = 4
        #top
        elif Qt.Key.Key_W in self.keypress:
            self.lbl_player.setPixmap(QPixmap(u"images/character_top_1.png"))
            self.attacknumber = 1
        #left
        elif Qt.Key.Key_A in self.keypress:
            self.lbl_player.setPixmap(QPixmap(u"images/character_left_7.png"))
            self.attacknumber = 7
        #bottom
        elif Qt.Key.Key_S in self.keypress:
            self.lbl_player.setPixmap(QPixmap(u"images/character_bottom_5.png"))
            self.attacknumber = 5
        #right
        elif Qt.Key.Key_D in self.keypress:
            self.lbl_player.setPixmap(QPixmap(u"images/character_right_3.png")) 
            self.attacknumber = 3
        #attack code
        if event.key() == Qt.Key.Key_Up:
            if self.meleevalid == True: 
                self.attack(self.attack_list[self.attacknumber-1]) 
                self.meleevalid = False
                #0.3 sec cooldown on melee attacks
                QTimer.singleShot(300,lambda:self.attackvalid())
            
        if event.key() == Qt.Key.Key_Right:
            self.rangedattack()
        #inventory
        if event.key() == Qt.Key.Key_Tab:
            if self.tab_part == 1:
                for slot in self.slot_list: 
                    slot.show()
                for i, name in enumerate(self.inventorynames):
                    name.show()
                self.pause()
                self.tab_part = 2
                self.enter = False #ensures you can't have inventory open and click enter
            elif self.tab_part == 2:
                for slot in self.slot_list:
                    slot.hide()
                for i, name in enumerate(self.inventorynames):
                    name.hide()
                self.resume()
                self.tab_part = 1
                self.enter = True
        
    def keyReleaseEvent(self, event):
        if event.key() in self.keypress:
            self.keypress.remove(event.key())

#ATTACK CODEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE
    def attack(self, label: QLabel):
        if self.pausestate == False:
            label.setPixmap(QPixmap(u"images/sword_slash.png"))
            #enemies
            for i, enemy in enumerate(self.enemylabels_list):
                if ULTIMATE_DEFS.collision(label, enemy):        
                    self.dmg = int(self.enemyhplabels_list[i].text())-self.playerattackdmg+self.enemyclass_list[i].defense
                    if self.dmg < 0:
                        self.dmg = 0
                    self.enemyhplabels_list[i].setText(str(self.dmg))
                    if int(self.enemyhplabels_list[i].text()) <= 0:
                        self.enemydeath(i)
                    if self.playerlifesteal == True:
                        self.lifesteal()
                else:
                    pass
            #bosses
            try: 
                for i, name in enumerate(self.boss_labels):
                    if ULTIMATE_DEFS.collision(label, name):
                        self.dmg = int(self.lbl_bosshealth.text())-self.playerattackdmg+self.bossclasslist[0].defense
                        if self.dmg < 0:
                            self.dmg = 0
                        self.lbl_bosshealth.setText(str(self.dmg)) #0 cuz there can only be 1 boss
                        try:
                            if self.lbl_bossname.text() == "The Ghost of the Forest":
                                self.lbl_bosshealthbar.setFixedSize(int(self.lbl_bosshealth.text())*6, 41)
                            elif self.lbl_bossname.text() == "Mycoria: The Blooming Tyrant":
                                self.lbl_bosshealthbar.setFixedSize(int(self.lbl_bosshealth.text())*2, 41)
                        except:
                            pass
                        if int(self.lbl_bosshealth.text()) <= 0:
                            if self.lbl_wave.text() == "5":
                                self.minibossdeath()
                            elif self.lbl_wave.text() == "10":
                                self.bossdeath()
                        if self.playerlifesteal == True:
                            self.lifesteal()
            except:
                pass
            self.play_sound_effect("audio/swordslash.mp3")
            QTimer.singleShot(200,lambda:self.attackpt2(label))
        else:
            pass
    
    def attackpt2(self, label: QLabel):
        label.setPixmap(QPixmap(u""))
        
    def attackvalid(self):
        self.meleevalid = True
    
    def lifesteal(self):
        self.playerhealth += 3
        if self.playerhealth > self.maxhealth:
            self.playerhealth = self.maxhealth
        self.lbl_playerhealth.setText(str(self.playerhealth))
        if self.maxhealth == 100:
            self.lbl_healthbar.setFixedSize(self.playerhealth * 4, 41)#the times four is because self.playerhealth is 4 times as big as the players hp
        elif self.maxhealth == 200:
            self.lbl_healthbar.setFixedSize(self.playerhealth * 2, 41) 
        
#RANGED CODEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE
    def chooserangedpixmap(self):
        #choosing which pixmap to show based on which way the char is facing
        if self.attacknumber == 1:
            self.rangedpixmap = QPixmap(u"images/arrow_top.png")
        elif self.attacknumber == 2:
            self.rangedpixmap = QPixmap(u"images/arrow_topR.png")
        elif self.attacknumber == 3:
            self.rangedpixmap = QPixmap(u"images/arrow_right.png")
        elif self.attacknumber == 4:
            self.rangedpixmap = QPixmap(u"images/arrow_bottomR.png")
        elif self.attacknumber == 5:
            self.rangedpixmap = QPixmap(u"images/arrow_bottom.png")
        elif self.attacknumber == 6:
            self.rangedpixmap = QPixmap(u"images/arrow_bottomL.png")
        elif self.attacknumber == 7:
            self.rangedpixmap = QPixmap(u"images/arrow_left.png")
        elif self.attacknumber == 8:
            self.rangedpixmap = QPixmap(u"images/arrow_topL.png")
            
    def rangedattack(self): 
        if self.pausestate == False:
            if self.rangedvalid == True:
                self.play_sound_effect("audio/arrowrelease.mp3")
                #creation
                self.ranged = QLabel(self.centralwidget)
                #setting size
                self.ranged.setFixedSize(50, 25)
                #pixmap and scaled contents
                self.chooserangedpixmap()
                self.ranged.setPixmap(self.rangedpixmap)
                self.ranged.setScaledContents(True)
                # Add the QLabel to the main_widget
                arrowx = self.attack_list[self.attacknumber-1].x()
                arrowy = self.attack_list[self.attacknumber-1].y()
                #moving and visibility
                self.ranged.move(arrowx,arrowy)
                self.ranged.setVisible(True)
                #arrowmovement
                self.rangedmovementvalid = True
                self.rangedtimer = QTimer()
                self.rangedtimer.start(10)
                self.rangedtimer.timeout.connect(self.ranged_movement)
                #cooldown
                self.rangedvalid = False
                self.lbl_bowcooldown.setText("2")
                QTimer.singleShot(1000,lambda:self.rangedattackcooldown1())
      
    def ranged_movement(self):
        #checking if the way the arrow moves has been decided
        if self.rangedmovementvalid == True:
            #deciding first movement
            if self.attacknumber == 1:
                self.ranged.move(self.ranged.x(),self.ranged.y()-10)
                #sets x and y to be used after decision
                self.rangedx = 0
                self.rangedy = -10
                #ranged movement validness
                self.rangedmovementvalid = False
            elif self.attacknumber == 2:
                self.ranged.move(self.ranged.x()+5,self.ranged.y()-5)
                #sets x and y to be used after decision
                self.rangedx = 5
                self.rangedy = -5
                #ranged movement validness
                self.rangedmovementvalid = False
            elif self.attacknumber == 3:
                self.ranged.move(self.ranged.x()+10,self.ranged.y())
                #sets x and y to be used after decision
                self.rangedx = 10
                self.rangedy = 0
                #ranged movement validness
                self.rangedmovementvalid = False
            elif self.attacknumber == 4:
                self.ranged.move(self.ranged.x()+5,self.ranged.y()+5)
                #sets x and y to be used after decision
                self.rangedx = 5
                self.rangedy = 5
                #ranged movement validness
                self.rangedmovementvalid = False
            elif self.attacknumber == 5:    
                self.ranged.move(self.ranged.x(),self.ranged.y()+10)
                #sets x and y to be used after decision
                self.rangedx = 0
                self.rangedy = 10
                #ranged movement validness
                self.rangedmovementvalid = False
            elif self.attacknumber == 6:
                self.ranged.move(self.ranged.x()-5,self.ranged.y()+5)
                #sets x and y to be used after decision
                self.rangedx = -5
                self.rangedy = 5
                #ranged movement validness
                self.rangedmovementvalid = False
            elif self.attacknumber == 7:
                self.ranged.move(self.ranged.x()-10,self.ranged.y())
                #sets x and y to be used after decision
                self.rangedx = -10
                self.rangedy = 0
                #ranged movement validness
                self.rangedmovementvalid = False
            elif self.attacknumber == 8:    
                self.ranged.move(self.ranged.x()-5,self.ranged.y()-5)
                #sets x and y to be used after decision
                self.rangedx = -5
                self.rangedy = -5
                #ranged movement validness
                self.rangedmovementvalid = False
        #checking if the way the arrow moves has been decided then does that movement
        if self.rangedmovementvalid == False:
            self.ranged.move(self.ranged.x()+self.rangedx, self.ranged.y()+self.rangedy)
        #pausing arrow if game is paused
        if self.pausestate == True:
            self.ranged.move(self.ranged.x()-self.rangedx, self.ranged.y()-self.rangedy)
        #self.dmg
        for i, enemy in enumerate(self.enemylabels_list):
            if ULTIMATE_DEFS.collision(self.ranged, enemy):
                self.rangedtimer.stop()
                self.ranged.deleteLater()
                self.rangedmovementvalid = True
                self.dmg = int(self.enemyhplabels_list[i].text())-self.rangedattackdmg+self.enemyclass_list[i].defense
                if self.dmg < 0:
                    self.dmg = 0
                self.enemyhplabels_list[i].setText(str(self.dmg))
                if self.playerrangedknockback == True and self.enemyintlist[i] != 2:
                    if self.lbl_player.x() < enemy.x():
                        enemy.move(enemy.x()+200,enemy.y())
                        self.enemyhplabels_list[i].move(self.enemyhplabels_list[i].x()+200, self.enemyhplabels_list[i].y())
                    elif self.lbl_player.x() > enemy.x():
                        enemy.move(enemy.x()-200,enemy.y())
                        self.enemyhplabels_list[i].move(self.enemyhplabels_list[i].x()-200, self.enemyhplabels_list[i].y())
                    if self.lbl_player.y() < enemy.y():
                        enemy.move(enemy.x(),enemy.y()+200)
                        self.enemyhplabels_list[i].move(self.enemyhplabels_list[i].x(), self.enemyhplabels_list[i].y()+200)
                    elif self.lbl_player.y() > enemy.y():
                        enemy.move(enemy.x(),enemy.y()-200)
                        self.enemyhplabels_list[i].move(self.enemyhplabels_list[i].x(), self.enemyhplabels_list[i].y()-200)
                if int(self.enemyhplabels_list[i].text()) <= 0:
                    self.enemydeath(i)
        #bosses
        try: 
            for i, name in enumerate(self.boss_labels):
                if ULTIMATE_DEFS.collision(self.ranged, name):
                    self.rangedtimer.stop()
                    self.ranged.deleteLater()
                    self.rangedmovementvalid = True
                    self.dmg = (int(self.lbl_bosshealth.text())-self.rangedattackdmg+self.bossclasslist[0].defense)
                    if self.dmg < 0:
                        self.dmg = 0
                    self.lbl_bosshealth.setText(str(self.dmg)) #0 cuz there can only be 1 boss
                try:
                    if self.lbl_bossname.text() == "The Ghost of the Forest":
                        self.lbl_bosshealthbar.setFixedSize(int(self.lbl_bosshealth.text())*6, 41)
                    elif self.lbl_bossname.text() == "Mycoria: The Blooming Tyrant":
                        self.lbl_bosshealthbar.setFixedSize(int(self.lbl_bosshealth.text())*2, 41)
                except:
                    pass
                if int(self.lbl_bosshealth.text()) <= 0:
                    if self.lbl_wave.text() == "5":
                        self.minibossdeath()
                    elif self.lbl_wave.text() == "10":
                        self.bossdeath()
        except:
            pass
        #checking if the arrow has gone out of bounds
        if self.ranged.y() < 0 or self.ranged.y() > 950 or self.ranged.x() < 0 or self.ranged.x() > 1440:
            self.rangedtimer.stop()
            self.ranged.deleteLater()
            self.rangedmovementvalid = True
    
    def rangedattackcooldown1(self):
        self.lbl_bowcooldown.setText("1")
        QTimer.singleShot(1000,lambda:self.rangedattackcooldown2())
        
    def rangedattackcooldown2(self):
        self.lbl_bowcooldown.setText("")
        self.rangedvalid = True
        
#SMOOVVEMENT CODEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE
    def player_move(self):
        if self.pausestate == False:
            move_x = ((Qt.Key.Key_D in self.keypress) * self.playerspeed) + ((Qt.Key.Key_A in self.keypress)* -self.playerspeed)
            move_y = ((Qt.Key.Key_W in self.keypress) * -self.playerspeed) + ((Qt.Key.Key_S in self.keypress)* self.playerspeed)
            if self.playerconfused == False:
                self.lbl_player.move(self.lbl_player.x()+move_x,self.lbl_player.y()+move_y)
                #moving attack labels
                for i, attack in enumerate(self.attack_list):
                    attack.move(attack.x()+move_x,attack.y()+move_y)
            elif self.playerconfused == True:
                self.lbl_player.move(self.lbl_player.x()-move_x,self.lbl_player.y()-move_y)
                for i, attack in enumerate(self.attack_list):
                    attack.move(attack.x()-move_x,attack.y()-move_y)
                self.confused.move(self.confused.x()-move_x,self.confused.y()-move_y)
            #checking if the player has gone out of bounds and moving them to other side of screen
            if self.lbl_player.x() < 0:
                #moving player
                self.lbl_player.move(self.lbl_player.x()+1420, self.lbl_player.y())
                #moving attack labels
                for i, attack in enumerate(self.attack_list):
                    attack.move(attack.x()+1420,attack.y())
                if self.playerconfused == True:
                    self.confused.move(self.confused.x()+1420, self.confused.y())
            elif self.lbl_player.x() > 1420:
                self.lbl_player.move(self.lbl_player.x()-1420, self.lbl_player.y())
                for i, attack in enumerate(self.attack_list):
                    attack.move(attack.x()-1420,attack.y())
                if self.playerconfused == True:
                    self.confused.move(self.confused.x()-1420, self.confused.y())
            elif self.lbl_player.y() < 0:
                self.lbl_player.move(self.lbl_player.x(), self.lbl_player.y()+950)
                for i, attack in enumerate(self.attack_list):
                    attack.move(attack.x(),attack.y()+950)
                if self.playerconfused == True:
                    self.confused.move(self.confused.x(), self.confused.y()+950)    
            elif self.lbl_player.y() > 950:
                self.lbl_player.move(self.lbl_player.x(), self.lbl_player.y()-950)
                for i, attack in enumerate(self.attack_list):
                    attack.move(attack.x(),attack.y()-950)
                if self.playerconfused == True:
                    self.confused.move(self.confused.x(), self.confused.y()-950)
            #checking if the player has collided with the boss
            if self.bossdead == False:
                if self.playerinvicible == False:
                    if ULTIMATE_DEFS.collision(self.lbl_player, self.boss_label):
                        self.dmg = self.bossclass.attack+self.playerdefense
                        if self.dmg < 0:
                            self.dmg = 0
                        self.playerhealth -= self.dmg
                        self.lbl_healthbar.setFixedSize(self.playerhealth * 4, 41)
                        self.lbl_playerhealth.setText(str(self.playerhealth))
                        if self.lbl_playerhealth.text() <= "0":
                            if self.imstillstandingequipped == True and self.imstillstandingused == False and self.TOIcompleted == True and self.BIBcompleted:
                                mixer.music.stop()
                                self.play_music("audio/imstillstanding.mp3")
                                self.imstillstanding()
                            else:
                                self.gameover()
                        if self.lbl_player.x() < self.boss_label.x():
                            self.lbl_player.move(self.lbl_player.x()-100, self.lbl_player.y()-100)
                        elif self.lbl_player.x() > self.boss_label.x():
                            self.lbl_player.move(self.lbl_player.x()+100, self.lbl_player.y()+100)
            
#INVENTORY CODEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE
    def inventory(self):
        #sets inventorylist to nothing
        self.slot_list = []
        #gets all the list widgets
        for list in self.findChildren(QListWidget):
            if list.objectName().startswith('lst_slot'):
                self.slot_list.append(list)
                self.ui.append(list)
                list.hide()
        for i, name in enumerate(self.inventorynames):
            name.hide()
        #sets all the list widgets to no focus
        for slot in self.slot_list:
            slot.setFocusPolicy(Qt.NoFocus)
            #sets scroll bar to never appear
            slot.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.addinventoryitem("blank.jpeg", slot, "blank")
        #setting list widgets to items
        self.addinventoryitem("trash.jpg", self.lst_slot_trash, "trash")
        
    def addinventoryitem(self, image, inventoryspace, text):
        #reseting inventory space
        inventoryspace.clear()
        #setting icon to be an image
        icon = QIcon(f"images/{image}")
        #setting items and merging to icons
        item = QListWidgetItem()
        item.setText(f"{text}")
        item.setIcon(icon)
        #setting icon size to size of full list widget
        inventoryspace.setIconSize(self.lst_slot_1.size())
        #adding item
        inventoryspace.addItem(item)
        
    def lst_slots_a(self):
        if self.inventory_part == 1:
            self.sword = False
            self.bow = False
            self.armor = False
            self.boots = False
            self.lifeforce = False
            self.cd = False
            #grabbing first list widget
            self.slot_1 = self.sender()
            #grabbing item and icon
            item = self.slot_1.currentItem()
            #checks if item has something
            self.inventory_icon = item.icon()
            self.slot_text = item.text()
            #SWORDS
            if self.slot_text==("timesword") or self.slot_text==("mosquitorapier"):
                self.sword = True
            #BOWS
            elif self.slot_text==("futurebow") or self.slot_text==("slimebow"):
                self.bow = True
            #ARMOR
            elif self.slot_text==("ironarmor") or self.slot_text==("thornmail"):
                self.armor = True
            #BOOTS
            elif self.slot_text==("wingedrunners") or self.slot_text==("ironboots"):
                self.boots = True
            #LIFEFORCE
            elif self.slot_text==("armoredheart") or self.slot_text==("cyborgheart"):
                self.lifeforce = True
            #CD
            elif self.slot_text==("backinblack") or self.slot_text==("thickofit") or self.slot_text==("imstillstanding") or self.slot_text==("sixhundredstrike"):
                self.cd = True
            #logic to switch or not switch inventory
            if self.slot_text==("blank") or self.slot_text==("trash"): #needs to check if it is something that can be moved
                self.inventory_part = 1
                self.clear_inventory_selection()
            else: 
                #setting inventory to part 2 for next clicked
                self.inventory_part = 2
        elif self.inventory_part == 2:
            #grabbing second list widget
            self.slot_2 = self.sender()
            #TRASH
            if self.slot_2.currentItem().text() == "trash":
                #clearing first list widget
                self.addinventoryitem("blank.jpeg", self.slot_1, "blank")
                #reseting inventory to part 1
                self.inventory_part = 1
                self.clear_inventory_selection()
            #NORMAL
            elif self.slot_2.currentItem().text() == "blank" and not self.slot_2.objectName().startswith('lst_slot_melee') and not self.slot_2.objectName().startswith('lst_slot_ranged') and not self.slot_2.objectName().startswith('lst_slot_armor') and not self.slot_2.objectName().startswith('lst_slot_boots') and not self.slot_2.objectName().startswith('lst_slot_lifeforce') and not self.slot_2.objectName().startswith('lst_slot_song'):    
                #clearing first list widget    
                self.addinventoryitem("blank.jpeg", self.slot_1, "blank")
                self.addingitem()
            #SWORDS
            elif self.sword == True:
                if self.slot_2.objectName().startswith('lst_slot_melee') and self.slot_2.currentItem().text() == "blank":
                    #clearing first
                    self.addinventoryitem("blank.jpeg", self.slot_1, "blank")
                    self.addingitem()
                    self.itembuff()
                else:
                    self.resetinginventoryselection()
            #BOWS
            elif self.bow == True:
                if self.slot_2.objectName().startswith('lst_slot_ranged') and self.slot_2.currentItem().text() == "blank":
                    #clearing first
                    self.addinventoryitem("blank.jpeg", self.slot_1, "blank")
                    self.addingitem()
                    self.itembuff()
                else:
                    self.resetinginventoryselection()
            #ARMOR
            elif self.armor == True:
                if self.slot_2.objectName().startswith('lst_slot_armor') and self.slot_2.currentItem().text() == "blank":
                    #clearing first
                    self.addinventoryitem("blank.jpeg", self.slot_1, "blank")
                    self.addingitem()
                    self.itembuff()
                else:
                    self.resetinginventoryselection()
            #BOOTS
            elif self.boots == True:
                if self.slot_2.objectName().startswith('lst_slot_boots') and self.slot_2.currentItem().text() == "blank":
                    #clearing first
                    self.addinventoryitem("blank.jpeg", self.slot_1, "blank")
                    self.addingitem()
                    self.itembuff()
                else:
                    self.resetinginventoryselection()
            #LIFEFORCE
            elif self.lifeforce == True:
                if self.slot_2.objectName().startswith('lst_slot_lifeforce') and self.slot_2.currentItem().text() == "blank":
                    #clearing first
                    self.addinventoryitem("blank.jpeg", self.slot_1, "blank")
                    self.addingitem()
                    self.itembuff()
                else:
                    self.resetinginventoryselection()
            #CD
            elif self.cd == True:
                if self.slot_2.objectName().startswith('lst_slot_song') and self.slot_2.currentItem().text() == "blank":
                    #clearing first
                    self.addinventoryitem("blank.jpeg", self.slot_1, "blank")
                    self.addingitem()
                    self.itembuff()
                else:
                    self.resetinginventoryselection()
            #reseting inventory to part 1
            else:
                self.inventory_part = 1
                self.clear_inventory_selection()
            self.inventoryunequipchecker()
            print(self.playerattackdmg, self.playerdefense, self.playerspeed, self.rangedattackdmg)
            print(f"lifesteal: {self.playerlifesteal}")
            print(f"rangedknockback: {self.playerrangedknockback}")
            print(f"thorns: {self.playerthorns}")
                
    def inventoryunequipchecker(self):
        #basic buffs
        #swords
        if self.lst_slot_melee.item(0).text() == "blank":
            self.playerattackdmg = 5
            if self.lst_slot_lifeforce.item(0).text() == "cyborgheart":
                self.playerattackdmg = 6
        #bows
        if self.lst_slot_ranged.item(0).text() == "blank":
            self.rangedattackdmg = 3
            if self.lst_slot_lifeforce.item(0).text() == "cyborgheart":
                self.rangedattackdmg += 1
        #armor
        if self.lst_slot_armor.item(0).text() == "blank":
            self.playerdefense = 0
            if self.lst_slot_lifeforce.item(0).text() == "cyborgheart":
                self.playerdefense +=1 
            if self.lst_slot_boots.item(0).text() == "ironboots":
                self.playerdefense += 2
        #boots
        if self.lst_slot_boots.item(0).text() == "blank":
            self.playerspeed = 1
            if self.lst_slot_lifeforce.item(0).text() == "cyborgheart":
                self.playerspeed +=1 
            if self.lst_slot_melee.item(0).text() == "timesword":
                self.playerspeed += 1
        #lifeforce
        if self.lst_slot_lifeforce.item(0).text() == "blank":
            self.maxhealth = 100
            self.lbl_healthbar.setFixedSize(self.playerhealth * 4, 41) 
        #special buffs
        if self.lst_slot_melee.item(0).text() != "mosquitorapier":
            self.playerlifesteal = False
        if self.lst_slot_ranged.item(0).text() != "slimebow":
            self.playerrangedknockback = False
        if self.lst_slot_armor.item(0).text() != "thornmail":
            self.playerthorns = False
        #discs
        if self.lst_slot_song1.item(0).text() == "blank":
            self.disc1 = "blank"
        elif self.lst_slot_song2.item(0).text() == "blank":
            self.disc2 = "blank"
        elif self.lst_slot_song3.item(0).text() == "blank":
            self.disc3 = "blank"
        #backinblack
        if self.lst_slot_song1.item(0).text() != "backinblack" and self.lst_slot_song2.item(0).text() != "backinblack" and self.lst_slot_song3.item(0).text() != "backinblack":
            self.backinblackequipped = False
            self.lbl_backinblackability.setVisible(False)
            self.lbl_backinblackcooldown.setVisible(False)
        #thickofit
        if self.lst_slot_song1.item(0).text() != "thickofit" and self.lst_slot_song2.item(0).text() != "thickofit" and self.lst_slot_song3.item(0).text() != "thickofit":
            self.thickofitequipped = False
            self.lbl_thickofitability.setVisible(False)
            self.lbl_thickofitcooldown.setVisible(False)
        #imstillstanding
        if self.lst_slot_song1.item(0).text() != "imstillstanding" and self.lst_slot_song2.item(0).text() != "imstillstanding" and self.lst_slot_song3.item(0).text() != "imstillstanding":
            self.imstillstandingequipped = False
            self.lbl_imstillstandingability.setVisible(False)
            self.lbl_imstillstandingcooldown.setVisible(False)
        #sixhundredstrike
        if self.lst_slot_song1.item(0).text() != "sixhundredstrike" and self.lst_slot_song2.item(0).text() != "sixhundredstrike" and self.lst_slot_song3.item(0).text() != "sixhundredstrike":
            self.sixhundredstrikeequipped = False
            self.lbl_sixhundredstrikeability.setVisible(False)
            self.lbl_sixhundredstrikecooldown.setVisible(False)
            
    def addingitem(self):
        #adding item
        self.slot_2.clear()
        new_item = QListWidgetItem()
        new_item.setIcon(self.inventory_icon)
        new_item.setText(self.slot_text)
        self.slot_2.addItem(new_item)
        #reseting inventory to part 1
        self.inventory_part = 1
        self.clear_inventory_selection()
    
    def resetinginventoryselection(self):
        self.inventory_part = 1
        self.clear_inventory_selection()
            
    def clear_inventory_selection(self):
        for slot in self.slot_list:
            slot.clearSelection()
    
    def itembuff(self):
        #basic buffs
        if self.lst_slot_melee.item(0).text() == "timesword":
            self.playerattackdmg = self.playerattackdmg+3
            self.playerspeed = self.playerspeed+1
        elif self.lst_slot_ranged.item(0).text() == "futurebow":
            self.rangedattackdmg = self.rangedattackdmg+7
        elif self.lst_slot_ranged.item(0).text() == "slimebow":
            self.rangedattackdmg = self.rangedattackdmg+4
        elif self.lst_slot_armor.item(0).text() == "ironarmor":
            self.playerdefense = self.playerdefense+5
        elif self.lst_slot_armor.item(0).text() == "thornmail":
            self.playerdefense = self.playerdefense+2
        elif self.lst_slot_boots.item(0).text() == "wingedrunners":
            self.playerspeed = self.playerspeed+4
        elif self.lst_slot_boots.item(0).text() == "ironboots":
            self.playerdefense = self.playerdefense+2
        elif self.lst_slot_lifeforce.item(0).text() == "cyborgheart":
            self.playerattackdmg = self.playerattackdmg+1
            self.rangedattackdmg = self.rangedattackdmg+1
            self.playerdefense = self.playerdefense+1
            self.playerspeed = self.playerspeed+1
        elif self.lst_slot_lifeforce.item(0).text() == "armoredheart":
            self.maxhealth = self.maxhealth+self.chosen.lifeforcebuff
            self.lbl_healthbar.setFixedSize(self.playerhealth * 2, 41) 
        #special buffs
        if self.lst_slot_melee.item(0).text() == "mosquitorapier":
            self.playerlifesteal = True
        if self.lst_slot_ranged.item(0).text() == "slimebow":
            self.playerrangedknockback = True
        if self.lst_slot_armor.item(0).text() == "thornmail":
            self.playerthorns = True
        #discs
        #backinblack
        if self.lst_slot_song1.item(0).text() == "backinblack":
            self.disc1 = "backinblack"
        elif self.lst_slot_song2.item(0).text() == "backinblack":
            self.disc2 = "backinblack"
        elif self.lst_slot_song3.item(0).text() == "backinblack":
            self.disc3 = "backinblack"
        if self.lst_slot_song1.item(0).text() == "backinblack" or self.lst_slot_song2.item(0).text() == "backinblack" or self.lst_slot_song3.item(0).text() == "backinblack":
            self.backinblackequipped = True
            self.lbl_backinblackability.setVisible(True)
            self.lbl_backinblackcooldown.setVisible(True)
        #thick of it
        if self.lst_slot_song1.item(0).text() == "thickofit":
            self.disc1 = "thickofit"
        elif self.lst_slot_song2.item(0).text() == "thickofit":
            self.disc2 = "thickofit"
        elif self.lst_slot_song3.item(0).text() == "thickofit":
            self.disc3 = "thickofit"
        if self.lst_slot_song1.item(0).text() == "thickofit" or self.lst_slot_song2.item(0).text() == "thickofit" or self.lst_slot_song3.item(0).text() == "thickofit":
            self.thickofitequipped = True
            self.lbl_thickofitability.setVisible(True)
            self.lbl_thickofitcooldown.setVisible(True)
        #im still standing
        if self.lst_slot_song1.item(0).text() == "imstillstanding":
            self.disc1 = "imstillstanding"
        elif self.lst_slot_song2.item(0).text() == "imstillstanding":
            self.disc2 = "imstillstanding"
        elif self.lst_slot_song3.item(0).text() == "imstillstanding":
            self.disc3 = "imstillstanding"
        if self.lst_slot_song1.item(0).text() == "imstillstanding" or self.lst_slot_song2.item(0).text() == "imstillstanding" or self.lst_slot_song3.item(0).text() == "imstillstanding":
            self.imstillstandingequipped = True
            self.lbl_imstillstandingability.setVisible(True)
            self.lbl_imstillstandingcooldown.setVisible(True)
        #six hundred strike
        if self.lst_slot_song1.item(0).text() == "sixhundredstrike":
            self.disc1 = "sixhundredstrike"
        elif self.lst_slot_song2.item(0).text() == "sixhundredstrike":
            self.disc2 = "sixhundredstrike"
        elif self.lst_slot_song3.item(0).text() == "sixhundredstrike":
            self.disc3 = "sixhundredstrike"
        if self.lst_slot_song1.item(0).text() == "sixhundredstrike" or self.lst_slot_song2.item(0).text() == "sixhundredstrike" or self.lst_slot_song3.item(0).text() == "sixhundredstrike":
            self.sixhundredstrikeequipped = True
            self.lbl_sixhundredstrikeability.setVisible(True)
            self.lbl_sixhundredstrikecooldown.setVisible(True)
            
#PAUSE CODEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE + GAMEOVERRRRRRRRRRRRRRRRRRRRRRRR
    def pause(self):
        self.pausestate = True
        self.timer_player.stop()
        self.timer_enemy.stop()
        
    def resume(self):
        self.pausestate = False
        self.timer_player.start(5)
        self.timer_enemy.start(15)         
        
    def gameover(self):
        for i, name in enumerate(self.fireball_list):
            try:
                name.setVisible(False)
                name.deleteLater()
            except:
                pass
        for i, name in enumerate(self.fireball_timers):
            try:
                name.stop()
            except:
                pass
        self.pausestate = True
        self.timer_player.stop()
        self.timer_enemy.stop()
        self.sonicIN = False
        while self.enemylabels_list:
            self.enemylabels_list[0].deleteLater()
            self.enemyhplabels_list[0].deleteLater()
            self.enemyclass_list.pop(0)
            self.enemylabels_list.pop(0)
            self.enemyhplabels_list.pop(0) 
        if self.minibossdead == False:
            self.minibossdeath()
        elif self.bossdead == False:
            self.bossdeath()
        score = self.lbl_score.text()
        manager.screen_youdied.lbl_score.setText(str(score))
        self.BIBcooldown = 0
        self.TOIcooldown = 0
        self.ISScooldown = 0
        self.SHScooldown = 0
        mixer.music.stop()
        self.play_music("audio/bgmusic.mp3")
        manager.widget.setCurrentWidget(manager.screen_youdied)

#MIXER CODEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE
    def play_music(self, file_path, volume=0.5):
        mixer.music.load(file_path)
        mixer.music.set_volume(volume)
        mixer.music.play()
    
    def play_sound_effect(self,file_path, volume=0.5):
        sound_effect = mixer.Sound(file_path)
        sound_effect.set_volume(volume)
        sound_effect.play()
            
    def loop_music(self):
        if not mixer.music.get_busy():
            self.play_music("audio/bgmusic.mp3")
        

#DISC CODEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE
#backinblack
    def backinblack(self):
        self.backinblackused = True
        self.BIBcompleted = False
        self.warning_label1 = QLabel(self.centralwidget)
        self.warning_labels.append(self.warning_label1)
        self.warning_label2 = QLabel(self.centralwidget)
        self.warning_labels.append(self.warning_label2)
        self.warning_label3 = QLabel(self.centralwidget)
        self.warning_labels.append(self.warning_label3)
        self.warning_label4 = QLabel(self.centralwidget)
        self.warning_labels.append(self.warning_label4)
        self.warning_label5 = QLabel(self.centralwidget)
        self.warning_labels.append(self.warning_label5)
        self.warning_label6 = QLabel(self.centralwidget)
        self.warning_labels.append(self.warning_label6)
        self.warning_label1.move(100, 70)
        self.warning_label2.move(100, 570)
        self.warning_label3.move(590, 70)
        self.warning_label4.move(590, 570)
        self.warning_label5.move(1100, 70)
        self.warning_label6.move(1100, 570)
        for i, name in enumerate(self.warning_labels):
            name.setFixedSize(300, 300)
            name.setVisible(True)
            name.setPixmap(QPixmap(u"images/fireball.jpeg"))
            name.setScaledContents(True)
            #enemies
            for i, enemy in enumerate(self.enemylabels_list):
                if ULTIMATE_DEFS.collision(name, enemy):   
                    self.dmg = int(self.enemyhplabels_list[i].text())-15
                    if self.dmg < 0:
                        self.dmg = 0
                    self.enemyhplabels_list[i].setText(str(self.dmg))
                    if int(self.enemyhplabels_list[i].text()) <= 0:
                        self.enemydeath(i)
                else:
                    pass
            #bosses
            try: 
                for i, boss in enumerate(self.boss_labels):
                    if ULTIMATE_DEFS.collision(name, boss):
                        self.dmg = int(self.lbl_bosshealth.text())-15
                        if self.dmg < 0:
                            self.dmg = 0
                        self.lbl_bosshealth.setText(str(self.dmg)) #0 cuz there can only be 1 boss
                        try:
                            if self.lbl_bossname.text() == "The Ghost of the Forest":
                                self.lbl_bosshealthbar.setFixedSize(int(self.lbl_bosshealth.text())*6, 41)
                            elif self.lbl_bossname.text() == "Mycoria: The Blooming Tyrant":
                                self.lbl_bosshealthbar.setFixedSize(int(self.lbl_bosshealth.text())*2, 41)
                        except:
                            pass
                        if int(self.lbl_bosshealth.text()) <= 0:
                            self.bossdeath()
            except:
                pass
        if self.BIBvalid == True:
            QTimer.singleShot(10000, lambda: self.backinblackcooldownfunction())
            self.BIBvalid = False
        QTimer.singleShot(300, lambda: self.backinblack2())
    
    def backinblack2(self):
        for i, name in enumerate(self.warning_labels):
            name.setPixmap(QPixmap(u""))
            name.deleteLater()
        self.warning_labels.clear()
        if self.backinblack_cooldown == False:
            QTimer.singleShot(3000, lambda: self.backinblack())
    
    def backinblackcooldownfunction(self):
        self.backinblack_cooldown = True
        self.BIBcooldown = 45
        self.BIBcompleted = True
        self.play_music("audio/bgmusic.mp3")
        self.backinblacktimer = QTimer()
        self.backinblacktimer.timeout.connect(self.update_backinblack_cooldown)
        self.backinblacktimer.start(1000)
    
    def update_backinblack_cooldown(self):
        self.BIBcooldown -= 1
        self.lbl_backinblackcooldown.setText(str(self.BIBcooldown))
        if self.BIBcooldown == 0:
            self.lbl_backinblackcooldown.setText("")
            self.backinblack_cooldown = False
            self.backinblacktimer.stop()
            self.backinblackused = False
#thickofit
    def thickofit(self):
        self.thickofitused = True
        self.TOIcompleted = False
        self.thickofitmovement = True
        QTimer.singleShot(30000, lambda: self.thickofitcooldownfunction())
    
    def thickofitcooldownfunction(self):
        self.TOIcooldown = 60
        self.TOIcompleted = True
        self.thickofitmovement = False
        self.play_music("audio/bgmusic.mp3")
        self.thickofittimer = QTimer()
        self.thickofittimer.timeout.connect(self.update_thickofit_cooldown)
        self.thickofittimer.start(1000)
    
    def update_thickofit_cooldown(self):
        self.TOIcooldown -= 1
        self.lbl_thickofitcooldown.setText(str(self.TOIcooldown))
        if self.TOIcooldown == 0:
            self.lbl_thickofitcooldown.setText("")
            self.thickofittimer.stop()
            self.thickofitused = False

#imstillstanding
    def imstillstanding(self):
        self.imstillstandingused = True
        self.ISScompleted = False
        self.playerhealth = 25
        self.lbl_playerhealth.setText(str(self.playerhealth))
        if self.maxhealth == 100:
            self.lbl_healthbar.setFixedSize(self.playerhealth * 4, 41)#the times four is because self.playerhealth is 4 times as big as the players hp
        elif self.maxhealth == 200:
            self.lbl_healthbar.setFixedSize(self.playerhealth * 2, 41) 
        self.playerinvicible = True
        QTimer.singleShot(10000, lambda: self.imstillstandingcooldownfunction())

    def imstillstandingcooldownfunction(self):
        self.ISScooldown = 120
        self.ISScompleted = True
        self.playerinvicible = False
        self.play_music("audio/bgmusic.mp3")
        self.imstillstandingtimer = QTimer()
        self.imstillstandingtimer.timeout.connect(self.update_imstillstanding_cooldown)
        self.imstillstandingtimer.start(1000)
    
    def update_imstillstanding_cooldown(self):
        self.ISScooldown -= 1
        self.lbl_imstillstandingcooldown.setText(str(self.ISScooldown))
        if self.ISScooldown == 0:
            self.lbl_imstillstandingcooldown.setText("")
            self.imstillstandingtimer.stop()
            self.imstillstandingused = False
            
#Six Hundred Strike
    def sixhundredstrike(self):
        if self.enemylabels_list != [] or self.boss_labels != []:
            if self.sixhundredstrikecooldown == False:
                self.allenemieshp = []
                self.enemyhplabels = []
                self.allenemieslabels = []
                self.sixhundredstrikeused = True
                self.SHScompleted = False
                for i, name in enumerate(self.enemyhplabels_list):
                    self.allenemieshp.append(int(name.text()))
                    self.enemyhplabels.append(name)
                    self.allenemieslabels.append(self.enemylabels_list[i])
                if self.minibossdead == False:
                    self.allenemieshp.append(int(self.lbl_bosshealth.text()))
                    self.enemyhplabels.append(self.lbl_bosshealth)
                    self.allenemieslabels.append(self.miniboss_label)
                elif self.bossdead == False:
                    self.allenemieshp.append(int(self.lbl_bosshealth.text()))
                    self.enemyhplabels.append(self.lbl_bosshealth)
                    self.allenemieslabels.append(self.boss_label)
                largest = max(self.allenemieshp)
                index = self.allenemieshp.index(largest)
                enemy = self.allenemieslabels[index]
                trident = QLabel(self.centralwidget)
                trident.setFixedSize(100, 100)
                trident.setPixmap(QPixmap(u"images/trident.jpg"))
                trident.setScaledContents(True)
                trident.setVisible(True)
                trident.move(enemy.x(), enemy.y())
                self.enemyhplabels[index].setText(str(int(largest)-10))
                if int(self.enemyhplabels[index].text()) <= 0:
                    self.enemydeath(index)
                if self.sixhundredstrikevalid == True:
                    print("run")
                    QTimer.singleShot(20000, lambda: self.sixhundredstrikecooldownfunction())
                    self.sixhundredstrikevalid = False
                QTimer.singleShot(500, lambda: self.sixhundredstrikerepeat(trident))
            
    def sixhundredstrikerepeat(self, trident): 
        trident.deleteLater()
        if self.sixhundredstrikecooldown == False:
            QTimer.singleShot(3000, lambda: self.sixhundredstrike())
    
    def sixhundredstrikecooldownfunction(self):
        self.SHScooldown = 80
        self.SHScompleted = True
        self.sixhundredstrikecooldown = True
        self.play_music("audio/bgmusic.mp3")
        self.sixhundredstriketimer = QTimer()
        self.sixhundredstriketimer.timeout.connect(self.update_sixhundredstrike_cooldown)
        self.sixhundredstriketimer.start(1000)
    
    def update_sixhundredstrike_cooldown(self):
        self.SHScooldown -= 1
        self.lbl_sixhundredstrikecooldown.setText(str(self.SHScooldown))
        if self.SHScooldown == 0:
            self.lbl_sixhundredstrikecooldown.setText("")
            self.sixhundredstriketimer.stop()
            self.sixhundredstrikecooldown = False
            self.sixhundredstrikeused = False 
            self.sixhundredstrikevalid = True

#ESCAPE MENU CODEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE

    def btn_resume_a(self):
        self.pausestate = False
        for i, button in enumerate(self.pause_buttons):
            button.setVisible(False)
    
    def btn_title_a(self):
        self.gameover()
        manager.widget.setCurrentWidget(manager.screen_startscreen)
    
    def btn_exit_a(self):
        exit()