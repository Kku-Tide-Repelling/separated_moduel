import os
import pygame
import random
import time
import pickle

file_names = [
    "eagle.wav", "gun.wav", "machine_gun.wav",
    "natural_enemy1.wav", "natural_enemy2.wav", "owl1.wav", "owl2.wav"
]

file_paths = [os.path.join("/home/hyun/wav", name) for name in file_names]

pygame.init()
pygame.mixer.init()
sounds = [pygame.mixer.Sound(path) for path in file_paths]

ranking = {name: 0 for name in file_names}
data_file_path = "/home/hyun/pir_repelling_moduel/data.pkl"

def play_random_sound():
    sound = random.choice(sounds)
    print(sound)
    sound.set_volume(0.5)
    sound.play()
    time.sleep(5)
    sound.stop()
    return sound

def update_ranking(sound, increment):
    global ranking
    if increment:
        ranking[file_names[sounds.index(sound)]] += 1
    else:
        ranking[file_names[sounds.index(sound)]] -= 1
    save_ranking()

def save_ranking():
    with open(data_file_path, 'wb') as f:
        pickle.dump(ranking, f, protocol=pickle.HIGHEST_PROTOCOL)

def get_ranking():
    return ranking
