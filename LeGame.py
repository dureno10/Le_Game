import random
import json

class Character:
    def __init__(self, name, health, attack):
        self.name=name
        self.health=health
        self.attack=attack

    def is_alive(self):
        return self.health>0

    def take_damage(self, damage):
        self.health-=damage
        if self.health<0:
            self.health=0
            #if "Dinosaur" == self.enemy.name():
                #defense_charge()

    def attack_target(self,target):
        damage = max(0, self.attack)
        target.take_damage(damage)
        print(f"{self.name} attacks {target.name} for {damage} damage!")

class Dinosaur(Character):
    def __init__(self, name, health, attack, shield_health):
        super().__init__(name, health, attack)
        self.shield_health = shield_health
    def take_damage(self,damage):
        if self.shield_health>0:
            if self.shield_health>=damage:
                self.shield_health-=damage
                print(f"{self.name} shield absorbed {damage} damage.")
                print("Remaing Shield Health", self.shield_health)
            else:
                remaining_damage = damage-self.shield_health
                self.shield_health=0
                super().take_damage(remaining_damage)
                print(f"{self.name} shield breaks")
        else:
            super().take_damage(damage)
    #def defense_charge(self):
     #   defense = random.randint(200, 500)
      #  return defense
       # defense-=damage
        #print(defense)
        #if defense<0:
         #   defense=0

class Robot(Character):
    def __init__(self, name, health, attack):
        super().__init__(name, health, attack)

    def take_damage(self, damage):
        i = random.randint(1,10)
        if i%3==0:
            print(f"{self.name} evaded your attack!")
            self.health-=damage * 0
        else:
            self.health -= damage
            if self.health<0:
                self.health=0
    #def roger_dodger(self):
     #   i=random.randint(1,10)
      #  if i % 3 == 0:
       #     da_defense = player.attack_target(enemy)
        #    dodges = da_defense * 0

class Monster(Character):
    def attack_target(self,target):
        i = random.randint(1,10)
        if i %3==0:
            damage = self.attack*2
            target.take_damage(damage)
            print(f"{self.name} attacks {target.name} for {damage} critical damage!")
        else:
            damage = max(0, self.attack)
            target.take_damage(damage)
            print(f"{self.name} attacks {target.name} for {damage} damage!")

player = Character("Player", 5000, 100)

def generate_enemy():
    enemy_type = random.choice(["Dinosaur", "Robot", "Monster"])
    if enemy_type =="Dinosaur":
        name = random.choice(["Tyranosaurous-Rex", "Stegasaurous", "Pterodactyl"])
        health = random.randint(600,900)
        attack = random.randint(60, 90)
        shield_health = random.randint(200,500)
        return Dinosaur(name, health, attack, shield_health)
    elif enemy_type == "Robot":
        name = random.choice(["Terminator", "Iron Giant", "Bender"])
        health = random.randint(600, 900)
        attack = random.randint(60, 90)
        return Robot(name, health, attack)
    else:
        name = random.choice(["Godzilla", "King Kong", "Mothra"])
        health = random.randint(600, 900)
        attack = random.randint(60, 90)
        return Monster(name, health, attack)

le_level= 1

def level():
    global le_level
    print(f"\n== Level {le_level} ==")
    enemy = generate_enemy()
    print(f"{enemy.name} has appeared")
    while player.is_alive() and enemy.is_alive():
        print(f"Your HP: {player.health} | {enemy.name}'s HP: {enemy.health}")
        action = input("What will you do? (attack/flee): ".lower())
        if action == "attack":
            player.attack_target(enemy)
            if enemy.is_alive():
                enemy.attack_target(player)
        elif action == "flee":
            print("You fled from the battle!")
            homepage()
            break


        else:
            print("Invalid Choice! Choose 'attack' or 'flee'.")
    #else:
     #   if player.is_alive() and isinstance(enemy, Dinosaur):
      #      enemy.defense_charge()
       #     homepage()

    else:
        if player.is_alive():
            print(f"You defeated {enemy.name}")
            le_level += 1
            if le_level == 6:
                print(f"\n====You've Won the Game!====")
                print("Press 1 to quit")
                print("Press 2 to go to homepage")
                fin_inp = input()
                if fin_inp == "1":
                    quit()
                else:
                    homepage()
            homepage()
        else:
            print("You Died")
            homepage()
def homepage():
    print("Welcome to the Jungle! You must fight 5 rounds to survive!")
    print("What would you like to do?")
    user_inp=input(" 1. Fight!\n 2. Store\n 3. Save Game\n")
    if user_inp == "1":
        level()
    elif user_inp == "2":
        store()
    elif user_inp == "3":
        game_save()
        homepage()
    else:
        print("Invalid Choice")
        homepage()

health_itm = []
attack_itm = []
backpack = []
with open("ItemData.json") as f:
    data=json.load(f)
for weapon in data['items']:
    category = weapon.get('category')
    if category and category.lower() in ['magic', 'weapons']:
        attack_itm.append(weapon)
    elif category and category.lower() in ['food', 'healing']:
        health_itm.append(weapon)
    else:
        pass

def game_save(player, backpack, file_path):
    player_data={
        "name": player.name,
        "health": player.health,
        "attack": player.attack
    }
    backpack_data=[{"name": item.name,"description": item.description, "category": item.category} for item in backpack]

    game_data ={
        "player": player_data,
        "backpack": backpack_data
    }
    with open(file_path, "w") as json.file:
        json.dump(game_data,json_file, indent=4)
def item_description():
    for item in backpack:
        print("Name: ", item.get("name"))
        print("Description: ", item.get("description"))
        print("Category: ", item.get("category"))

def item_remove():
    itm_remove = input("Enter Name of Item You Want removed: ")
    for item in backpack:
        if itm_remove == item.get("name"):
            backpack.remove(item)
    store()


def store():
    print("Welcome to the store!")
    print("Here, you can equip and unequip items that can help you in your battles")
    store_input=input(" 1. Equip item\n 2. Check Inventory\n 3. Go Back ")
    if store_input == "1":
        shop_menu()
    elif store_input == "2":
        item_description()
        print("Would you like to remove an item?")
        question = input(" 1. yes\n 2. no")
        if question=="1":
            item_remove()
        else:
            store()
    elif store_input == "3":
        homepage()
    else:
        print("Invalid choice")
        store()

def shop_menu():
    print("This is the shop menu, you can take whatever you like to help you win")
    print("Different types of items will either help with your health or attack")
    print("'Healing' and 'Food' items will help heal your health by a varying amount")
    print("'Magic' and 'Weapons' will help increase your attack")
    shp_inp = input("Please make a selection:\n 1. Health\n 2. Attack\n")
    if shp_inp == "1":
        random.choice(health_itm)
        added_item = backpack.append(random.choice(health_itm))
        print("Your inventory has been updated, and have recieved some health back")
        player.health+=random.randint(10,100)
        store()
    elif shp_inp == "2":
        random.choice(attack_itm)
        added_item = backpack.append(random.choice(attack_itm))
        print("Your inventory has been updated, and have gained some strength")
        player.attack += random.randint(10, 100)
        store()
    else:
        print("Invalid Choice")
        shop_menu()
#import json, ask player what type of item they would like to buy, have it get random item
#item stored to backpack, if magic in bag, character health+5?
#make an exit

#make for loop that makes user play 5 times, have health carry over to next fight

def main():
    homepage()

if __name__ == "__main__":
    main()

