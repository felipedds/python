
enemies = 1
def increase_enemies():
    global enemies
    enemies += 1
    print(f"Enemies {enemies}")

increase_enemies()
print(f"Enemies {enemies}")

partners = 3
def increase_partners() -> int:
    partner = 0
    print(f"Partners {partner + 5}")

increase_partners()
print(f"Partners {partners}")

