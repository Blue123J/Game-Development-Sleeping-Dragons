import math
import random

# Game constants
WIDTH = 800  # Width of the game window in pixels.
HEIGHT = 600  # Height of the game window in pixels.
CENTER_X = WIDTH / 2  # X-coordinate of the center of the screen.
CENTER_Y = HEIGHT / 2  # Y-coordinate of the center of the screen.
CENTER = (CENTER_X, CENTER_Y)  # Tuple representing the center of the screen.
FONT_COLOR = (0, 0, 0)  # Font color for text, black in this case.
EGG_TARGET = 20  # Number of eggs the player must collect to win.
HERO_START_1 = (200, 300)  # Initial position of hero 1.
HERO_START_2 = (200, 400)  # Initial position of hero 2.
ATTACK_DISTANCE = 200  # Distance within which a dragon can attack a hero.
DRAGON_WAKE_TIME = 2  # Duration (in seconds) for which a dragon stays awake.
EGG_HIDE_TIME = 2  # Duration (in seconds) for which eggs remain hidden after being collected.
MOVE_DISTANCE = 5  # Number of pixels the hero moves with each key press.

# Game state variables
lives = 3  # Number of lives the player has.
eggs_collected = 0  # Number of eggs collected by the player.
game_over = False  # Boolean flag for game over state.
game_complete = False  # Boolean flag for game completion state.
reset_required = False  # Boolean flag to handle resetting hero position after dragon collision.

# Defining lairs with associated dragons, eggs, and related parameters.
easy_lair = {
    "dragon": Actor("dragon-asleep", pos=(600, 100)),  # Actor for the dragon in this lair.
    "eggs": Actor("one-egg", pos=(400, 100)),  # Actor for the egg in this lair.
    "egg_count": 1,  # Number of eggs in this lair.
    "egg_hidden": False,  # Status of eggs (visible or hidden).
    "egg_hide_counter": 0,  # Counter to track how long eggs are hidden.
    "sleep_length": 10,  # Duration for which the dragon remains asleep.
    "sleep_counter": 0,  # Counter for the dragon's sleep cycle.
    "wake_counter": 0  # Counter for the dragon's awake cycle.
}

medium_lair = {  # Similar structure as easy_lair, with different positions and parameters.
    "dragon": Actor("dragon-asleep", pos=(600, 300)),
    "eggs": Actor("two-eggs", pos=(400, 300)),
    "egg_count": 2,
    "egg_hidden": False,
    "egg_hide_counter": 0,
    "sleep_length": 7,
    "sleep_counter": 0,
    "wake_counter": 0
}

hard_lair = {  # Harder lair with a shorter dragon sleep duration.
    "dragon": Actor("dragon-asleep", pos=(600, 500)),
    "eggs": Actor("three-eggs", pos=(400, 500)),
    "egg_count": 3,
    "egg_hidden": False,
    "egg_hide_counter": 0,
    "sleep_length": 4,
    "sleep_counter": 0,
    "wake_counter": 0
}

lairs = [easy_lair, medium_lair, hard_lair]  # List of all lairs.
hero1 = Actor("hero", pos=HERO_START_1)  # Actor for the first hero.
hero2 = Actor("hero2", pos=HERO_START_2)  # Actor for the second hero.

def draw():  # Draws the game screen including background, heroes, lairs, and game state text.
    global lairs, eggs_collected, lives, game_complete
    screen.clear()  # Clears the screen.
    screen.blit("dungeon", (0, 0))  # Draws the dungeon background.
    if game_over:  # Displays "GAME OVER" if the game is over.
        screen.draw.text("GAME OVER!", fontsize=60, center=CENTER, color=FONT_COLOR)
    elif game_complete:  # Displays "YOU WON!" if the player wins.
        screen.draw.text("YOU WON!", fontsize=60, center=CENTER, color=FONT_COLOR)
    else:  # Draws heroes, lairs, and counters if the game is ongoing.
        hero1.draw()
        hero2.draw()
        draw_lairs(lairs)
        draw_counters(eggs_collected, lives)

def draw_lairs(lairs_to_draw):  # Draws all lairs including dragons and eggs (if visible).
    for lair in lairs_to_draw:
        lair["dragon"].draw()  # Draws the dragon in the lair.
        if lair["egg_hidden"] is False:
            lair["eggs"].draw()  # Only draw eggs if they are not hidden.

def draw_counters(eggs_collected, lives):  # Draws the counters for eggs collected and lives remaining.
    screen.blit("egg-count", (0, HEIGHT - 30))  # # Draws the egg count icon.
    screen.draw.text(str(eggs_collected),
                     fontsize=40,
                     pos=(30, HEIGHT - 30),
                     color=FONT_COLOR)
    screen.blit("life-count", (60, HEIGHT - 30))  # Draws the life count icon.
    screen.draw.text(str(lives),
                     fontsize=40,
                     pos=(90, HEIGHT - 30),
                     color=FONT_COLOR)

def update():  # Updates the game state, including hero movement and checking for collisions.
    # Hero 1 movement (controlled by arrow keys).
    if keyboard.right:
        hero1.x += MOVE_DISTANCE
        if hero1.x > WIDTH:
            hero1.x = WIDTH
    elif keyboard.left:
        hero1.x -= MOVE_DISTANCE
        if hero1.x < 0:
            hero1.x = 0
    elif keyboard.down:
        hero1.y += MOVE_DISTANCE
        if hero1.y > HEIGHT:
            hero1.y = HEIGHT
    elif keyboard.up:
        hero1.y -= MOVE_DISTANCE
        if hero1.y < 0:
            hero1.y = 0
    
    # Hero 2 movement (controlled by WASD keys).
    if keyboard.d:
        hero2.x += MOVE_DISTANCE
        if hero2.x > WIDTH:
            hero2.x = WIDTH
    elif keyboard.a:
        hero2.x -= MOVE_DISTANCE
        if hero2.x < 0:
            hero2.x = 0
    elif keyboard.s:
        hero2.y += MOVE_DISTANCE
        if hero2.y > HEIGHT:
            hero2.y = HEIGHT
    elif keyboard.w:
        hero2.y -= MOVE_DISTANCE
        if hero2.y < 0:
            hero2.y = 0 
    
    check_for_collisions()  # Check for collisions with dragons or eggs.

def update_lairs():  # Periodically updates the state of all lairs (dragons and eggs).
    global lairs, hero, lives
    for lair in lairs:                                
        if lair["dragon"].image == "dragon-asleep":   
            update_sleeping_dragon(lair)  # Handles the sleeping dragon logic.
        elif lair["dragon"].image == "dragon-awake":
            update_waking_dragon(lair)  # Handles the awake dragon logic.
        update_egg(lair)  # Handles the egg visibility logic.

clock.schedule_interval(update_lairs, 1)  # Updates lairs every second.

def update_sleeping_dragon(lair):  # Updates the dragon's state if it is sleeping. Randomly wakes it up after a certain time.
    if lair["sleep_counter"] >= lair["sleep_length"]: 
        # Checks if the sleep_counter is greater than or equal to the sleep_length set for the dragon.
        if random.choice([True, False]):  # 50% chance to wake up
            lair["dragon"].image = "dragon-awake"
            lair["sleep_counter"] = 0  # Reset sleep counter.
    else:
        lair["sleep_counter"] += 1  # Increment sleep counter.

def update_waking_dragon(lair):  # Handles the waking and sleeping states of a dragon based on how long it has been awake.
    if lair["wake_counter"] >= DRAGON_WAKE_TIME:  # Checks if the dragon has been awake long enough.
        lair["dragon"].image = "dragon-asleep"  # Updates the dragon image.
        lair["wake_counter"] = 0  # Resets the dragon’s wake_counter to 0.
    else:
        lair["wake_counter"] += 1  # Adds one to the wake_counter.
    
def update_egg(lair):  # Checks whether eggs need to stay hidden or become visible based on the time they've been hidden.
    if lair["egg_hidden"] is True:
        if lair["egg_hide_counter"] >= EGG_HIDE_TIME:  # Runs if any eggs have been hidden for long enough.
            lair["egg_hidden"] = False
            lair["egg_hide_counter"] = 0  # Resets the egg_hide_counter to 0.
        else:
            lair["egg_hide_counter"] += 1  # Adds one to the egg_hide_counter.

    
def check_for_collisions():  # Checks for collisions between the heroes and the eggs or the dragon in each lair.
    global lairs, eggs_collected, lives, reset_required, game_complete
    for hero in [hero1, hero2]:  # Loop through both heroes
        for lair in lairs:
            if lair["egg_hidden"] is False:
                check_for_egg_collision(lair, hero)  # This function is called if the eggs are not hidden.
                if lair["dragon"].image == "dragon-awake" and reset_required is False:
                    # This makes sure the player doesn’t lose a life when the hero is being moved back to the start position.
                    check_for_dragon_collision(lair, hero)            
                    # This function is called if the dragon is awake and the hero’s position is not being reset.

def check_for_dragon_collision(lair, hero):  # Checks if the hero has collided with the dragon.
    x_distance = hero.x - lair["dragon"].x  # Calculates the horizontal and vertical distances between the dragon and the hero.     
    y_distance = hero.y - lair["dragon"].y
    distance = math.hypot(x_distance, y_distance)  # Finds the distance between the dragon and the hero in a straight line.
    if distance < ATTACK_DISTANCE:
        handle_dragon_collision(hero)
        # This function is called if the distance between the hero and dragon is less than ATTACK_DISTANCE.

def handle_dragon_collision(hero):  # Handles the event when a hero collides with the dragon.
    global reset_required
    reset_required = True
    if hero == hero1:
        animate(hero, pos=HERO_START_1, on_finished=subtract_life)
    else:
        animate(hero, pos=HERO_START_2, on_finished=subtract_life)
    # This function is called when the animation is complete.

def check_for_egg_collision(lair, hero):  # Checks if the hero has collided with the eggs in a lair
    global eggs_collected, game_complete
    if hero.colliderect(lair["eggs"]):
        lair["egg_hidden"] = True
        eggs_collected += lair["egg_count"]  # Adds the number of eggs for the current lair to the player’s egg count.
        if eggs_collected >= EGG_TARGET:
            # Checks if the number of eggs collected is greater than or equal to the EGG_TARGET.
            game_complete = True

def subtract_life():  # Decreases the number of lives left for the player when they lose a life.
    global lives, reset_required, game_over
    lives -= 1
    if lives == 0:
        game_over = True
    reset_required = False # This variable is set to False, as the hero is already at the starting position.
