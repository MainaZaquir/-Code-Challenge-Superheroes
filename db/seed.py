from models import db, Power, Hero, HeroPower
from random import randint, choice

def seed():
    print("🦸‍♀️ Seeding powers...")
    powers = Power.create([
        {"name": "super strength", "description": "gives the wielder super-human strengths"},
        {"name": "flight", "description": "gives the wielder the ability to fly through the skies at supersonic speed"},
        {"name": "super human senses", "description": "allows the wielder to use her senses at a super-human level"},
        {"name": "elasticity", "description": "can stretch the human body to extreme lengths"}
    ])

    print("🦸‍♀️ Seeding heroes...")
    heroes = Hero.create([
        {"name": "Kamala Khan", "super_name": "Ms. Marvel"},
        {"name": "Doreen Green", "super_name": "Squirrel Girl"},
        {"name": "Gwen Stacy", "super_name": "Spider-Gwen"},
        {"name": "Janet Van Dyne", "super_name": "The Wasp"},
        {"name": "Wanda Maximoff", "super_name": "Scarlet Witch"},
        {"name": "Carol Danvers", "super_name": "Captain Marvel"},
        {"name": "Jean Grey", "super_name": "Dark Phoenix"},
        {"name": "Ororo Munroe", "super_name": "Storm"},
        {"name": "Kitty Pryde", "super_name": "Shadowcat"},
        {"name": "Elektra Natchios", "super_name": "Elektra"}
    ])

    print("🦸‍♀️ Adding powers to heroes...")
    strengths = ["Strong", "Weak", "Average"]

    for hero in heroes:
        for _ in range(randint(1, 3)):
            power = choice(powers)
            HeroPower.create(hero=hero, power=power, strength=choice(strengths))

    print("🦸‍♀️ Done seeding!")

if __name__ == "__main__":
    db.create_all() 
    seed()
