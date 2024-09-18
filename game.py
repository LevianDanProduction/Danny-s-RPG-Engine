import json
import random
import P_8 as engi

def load_json_file(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
        raise
    except FileNotFoundError:
        print(f"File not found: {filename}")
        raise
    except Exception as e:
        print(f"An error occurred: {e}")
        raise

def load_enemy_data():
    return load_json_file('all_enemies.json')

def get_enemies_for_scene(scene_id):
    all_enemies = load_enemy_data()
    for scene in all_enemies['scenes']:
        if scene['scene_id'] == scene_id:
            return scene['enemies']
    return []

replaceskill = {
    "skill_1":engi.Skill.skills[0]
}

def enemysync(sceneID):
    engi.Enemy.enemies = [i["base"] for i in get_enemies_for_scene(sceneID)]
    for i in engi.Enemy.enemies:
        i["skills"] = [replaceskill[j] for j in i["skills"]]

def load_player_data(data):
    return load_json_file('player_data.json')

def create_players(player_data):
    players = []
    exp = []
    for player in player_data['players']:
        players.append(engi.Player(player['name'], player['gender'], player['class'], player['suffix']))
    return players

def random_encounterprep(sceneID,enemyparty,playerparty):
    #print(enemyparty)
    eteam = []
    #print(engi.Enemy.enemies)
    for i in enemyparty:
        eteam.append(engi.Enemy(i,20,"cool "))
    for i in eteam:
        i.enemyStatSet() 
    for i in playerparty:
        i.fullRecover()
    engi.Battle(playerparty,eteam,'battle')
    

def display_dialogue(dialogue_list):
    for line in dialogue_list:
        print(f"{line['character']} ({line.get('expression', 'neutral')}): {line['text']}")
        input("Press Enter to continue...")

def get_random_enemy(scene_id):
    enemies = get_enemies_for_scene(scene_id)
    if not enemies:
        print("No enemies found for this scene.")
        return None
    return random.choice(enemies)

def handle_exploration(exploration, scene_id,players):
    repeat = True
    while repeat:
        print(exploration['prompt'])
        for i, choice in enumerate(exploration['choices'], 1):
            print(f"{i}. {choice['option']}")
        
        if 'exit_option' in exploration:
            print(f"{len(exploration['choices']) + 1}. {exploration['exit_option']}")

        while True:
            try:
                user_choice = input("Enter your choice: ").strip()
                if user_choice == "":
                    raise ValueError("No input provided.")
                user_choice = int(user_choice) - 1
                if user_choice < 0 or user_choice > len(exploration['choices']):
                    raise ValueError("Invalid choice.")
                break
            except ValueError as e:
                print(f"Error: {e}. Please enter a valid number.")

        if user_choice == len(exploration['choices']):
            if 'exit_option' in exploration:
                print(f"Exiting: {exploration['exit_option']}")
                if "dialogue" in exploration.get('exit_option', {}):
                    display_dialogue(exploration['exit_option'].get('dialogue', []))
                repeat = False
            else:
                print("Invalid choice. Please select a valid option.")
        else:
            selected_choice = exploration['choices'][user_choice]
            if "dialogue" in selected_choice:
                display_dialogue(selected_choice['dialogue'])

            if "outcome" in selected_choice:
                outcome = selected_choice["outcome"]
                if "dialogue" in outcome:
                    display_dialogue(outcome['dialogue'])
                
                if outcome["trigger_event"] == "random_encounter":
                    enemy = get_random_enemy(scene_id)
                    enemyGroup = [enemy]
                    if enemy:
                        print(f"An enemy appears: {enemy['base']['name']}")
                        print("Starting battle...")
                        random_encounterprep(scene_id,[enemy['base']['name']],players)
                        # Call the battle function here with the enemy data
                        # battle(enemy)
                        input("Battle complete. Press Enter to continue...")
                
                if outcome["trigger_event"] == "leave_area":
                    print("You leave the area.")
                    repeat = False
                
                if outcome.get("repeatable", "False"):
                    # If repeatable, continue the loop
                    exploration = outcome.get('next_prompt', exploration)
                else:
                    repeat = False

def handle_scene(scene,players):
    print(f"Location: {scene['location']}")
    print(f"{scene['description']}\n")

    for interaction_id in scene['interaction_order']:
        interaction = scene['interactions'][interaction_id]
        if interaction['type'] == 'dialogue':
            display_dialogue(interaction['content'])
        elif interaction['type'] == 'exploration':
            handle_exploration(interaction, scene['scene_id'],players)

def handle_chapter(chapter_data,players):
    print(f"Chapter {chapter_data['chapter']}: {chapter_data['title']}\n")
    for scene_id in chapter_data['scene_order']:
        scene = next(s for s in chapter_data['scenes'] if s['scene_id'] == scene_id)
        enemysync(scene_id)
        handle_scene(scene,players)
        print("\n" + "=" * 40 + "\n")

def start_game():
    player_data = load_player_data('player_data.json')
    players = create_players(player_data)
    for i in players:
        i.gain_exp(400)
        i.fullRecover()
    chapter_data = load_json_file('game_data.json')
    handle_chapter(chapter_data, players)

# Start the game
start_game()
