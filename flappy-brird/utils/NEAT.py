import os

import pygame
import pickle
import neat

from utils.bird import Bird
from utils.ground import Ground
from utils.pipe import Pipes
from utils.radio import Radio
from utils.score import Score

local_dir = os.path.dirname(__file__)
file = open(local_dir + "/config.txt", "r")
a = file.readline().split()[-1]
if a == 'False':
    Testing = False
else:
    Testing = True
file.close()

settings = 0
window = 0

game_flow = {'Gen': 0,
             'Leave_flow': False
             }

pygame.font.init()
STAT_FONT = pygame.font.SysFont("comicsans", 50)


def draw_lasers(birds, pipes, window, n=2):
    """ 
    Function that draws lines to visualize the pipes close to the bird
    Input = (Bird object, List, Window object)
    """

    ends = []
    sorted_pipes = pipes.list_next_pipes()
    if n > len(sorted_pipes):
        n = len(sorted_pipes)
    for i in range(n):
        ends.append(
            (sorted_pipes[i].x + sorted_pipes[i].width, sorted_pipes[i].gap_pos))
        ends.append(
            (sorted_pipes[i].x + sorted_pipes[i].width, sorted_pipes[i].bottom))
    for bird in birds:
        start = (bird.x + bird.img_size[0], bird.y + bird.img_size[1])
        for end in ends:
            pygame.draw.line(window, 'red', start, end)


def draw_AI_info(birds, window):
    """ 
    Function that draws the Generation of the birds and the number of living birds
    Input = (List, Window object)
    """

    txt = STAT_FONT.render(
        'Gen: ' + str(game_flow['Gen']), False, (255, 255, 255))
    window.blit(txt, (10, 10))
    alive = STAT_FONT.render(
        'Alive: ' + str(len(birds)), False, (255, 255, 255))
    window.blit(alive, (10, 60))

    txt = STAT_FONT.render('Gen: ' + str(game_flow['Gen']), False, (0, 0, 0))
    window.blit(txt, (12, 12))
    alive = STAT_FONT.render('Alive: ' + str(len(birds)), False, (0, 0, 0))
    window.blit(alive, (12, 62))


def get_AI_input(bird, next_pipes, input_data):
    """ 
    Function that gathers the inputs for the AI
    Input = (Bird object, List, List)
    """

    if len(next_pipes) == 1:
        input_data[0] = bird.y
        input_data[1] = bird.y - next_pipes[0].gap_pos
        # input_data[2] = bird.y - next_pipes[0].bottom
        input_data[2] = next_pipes[0].x
        # input_data[4] = bird.y - next_pipes[0].bottom
        input_data[3] = bird.y - next_pipes[0].gap_pos
        input_data[4] = next_pipes[0].x * 2
    else:
        input_data[0] = bird.y
        input_data[1] = bird.y - next_pipes[0].gap_pos
        # input_data[2] = bird.y - next_pipes[0].bottom
        input_data[2] = next_pipes[0].x
        # input_data[4] = bird.y - next_pipes[1].bottom
        input_data[3] = bird.y - next_pipes[1].gap_pos
        input_data[4] = next_pipes[1].x


def run_ai(settings_, window_):
    """ 
    Function that runs the AI based on given settings
    Input = (Dict, Window object)
    """

    global settings
    global window

    settings = settings_
    window = window_
    mode = settings['Mode']
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, '../Assets/NEAT_config.txt')
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)

    if settings['Speed'] == 'Normal':
        frame_rate = 60
        frame_skip = 1
    elif settings['Speed'] == '2x':
        frame_rate = 120
        frame_skip = 2
    elif settings['Speed'] == '8x':
        frame_rate = 480
        frame_skip = 8
    elif settings['Speed'] == 'Turbo':
        frame_rate = 100000
        frame_skip = 1000

    game_flow['Leave_flow'] = False
    game_flow['Gen'] = 0

    if mode == 'AI':

        try:
            genome_path = "Assets/AI_models/winner_{}_{}.pkl".format(settings['Theme'],
                                                                     settings['Difficulty'])
            with open(genome_path, "rb") as f:
                genome = pickle.load(f)
        except:
            genome_path = "Assets/AI_models/winner.pkl"
            with open(genome_path, "rb") as f:
                genome = pickle.load(f)

        # Convert loaded genome into required data structure
        genomes = [(1, genome)]

        # Call game with only the loaded genome
        return ai_gameloop(genomes, config)
    else:

        p = neat.Population(config)
        p.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        p.add_reporter(stats)
        try:
            winner = p.run(ai_gameloop, 500)
            with open("Assets/AI_models/winner_{}_{}.pkl".format(settings['Theme'],
                                                                 settings['Difficulty']), "wb") as f:
                pickle.dump(winner, f)
                print("Saved winner AI in AI_models/")
                f.close()
        except:
            return True


def ai_gameloop(genome, config):
    """ 
    Function that runs the game for the AI based on given settings
    Input = (List, Config)
    """

    game_flow['Gen'] += 1
    if not game_flow['Leave_flow']:
        mode = settings['Mode']
        WINDOW_WIDTH = settings['WINDOW_WIDTH']
        difficulty = settings["Difficulty"]
        theme = settings['Theme']

        if settings['Speed'] == 'Normal':
            frame_rate = 60
            frame_skip = 1
        elif settings['Speed'] == '2x':
            frame_rate = 120
            frame_skip = 2
        elif settings['Speed'] == '8x':
            frame_rate = 480
            frame_skip = 8
        elif settings['Speed'] == 'Turbo':
            frame_rate = 100000
            frame_skip = 60

        birds = []
        nets = []
        ge = []
        volume_holder = settings['Sound Volume']
        if mode == 'AI':
            net = neat.nn.FeedForwardNetwork.create(genome[0][1], config)
            nets.append(net)
            bird = Bird(theme=theme)
            birds.append(bird)
            genome[0][1].fitness = 0
            ge.append(genome[0][1])
        else:
            settings['Sound Volume'] = 0
            for _, g in genome:
                net = neat.nn.FeedForwardNetwork.create(g, config)
                nets.append(net)
                bird = Bird(theme=theme)
                birds.append(bird)
                g.fitness = 0
                ge.append(g)

        clock = pygame.time.Clock()
        running = True

        # initialize
        pipes = Pipes(theme=theme, difficulty=difficulty)
        ground = Ground(theme=theme)
        score = Score(WINDOW_WIDTH)
        radio = Radio(settings)
        input_data = [0, 0, 0, 0, 0, ]  # 0, 0]

        path = os.path.join("Assets/", theme)
        background = pygame.image.load(
            os.path.join(path, "bg_big.png")).convert_alpha()
        window.blit(background, (0, 0))
        time = 0
        while running and not game_flow['Leave_flow']:

            time += 1
            if difficulty != 'Meme':
                clock.tick(frame_rate)
            else:
                clock.tick(2 * frame_rate)

            # event handler
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_flow['Leave_flow'] = True
                    settings['Sound Volume'] = volume_holder
                # if event.type == pygame.MOUSEBUTTONDOWN:
                #     game_settings['leave_loop'] = True

            # collisions
            next_pipes = pipes.list_next_pipes()
            for bird in birds:
                if ground.collide(bird):
                    bird.alive = False
                    radio.hit_sound()
                    radio.die_sound()

            for pipe in pipes:
                for x, bird in enumerate(birds):
                    if pipe.collision(bird):
                        bird.alive = False
                        radio.hit_sound()
                        radio.die_sound()
                    if not bird.alive:
                        if next_pipes[0].x > 250:
                            ge[x].fitness -= 50
                        birds.pop(x)
                        nets.pop(x)
                        ge.pop(x)

            # movement
            for bird in birds:
                bird.move()
            if running:
                pipes.move()
                ground.move()

            # pipe management

            pipes.delete_old_pipes()
            pipes.create_pipe(time)

            # Score
            if len(birds) > 0:
                if score.count(birds[0], pipes):
                    radio.score_sound()
                    for g in ge:
                        g.fitness += 1

            # draw
            if time % frame_skip == 0:
                window.blit(background, (0, 0))
                pipes.draw(window)
                score.draw(window)
                for bird in birds:
                    bird.draw(window)
                ground.draw(window)
                draw_lasers(birds, pipes, window, n=2)

                if mode == 'Train AI':
                    draw_AI_info(birds, window)

                pygame.display.flip()

            # get the Data for the AI
            if len(pipes) > 0:
                next_pipes = pipes.list_next_pipes()
                for x, bird in enumerate(birds):
                    get_AI_input(bird, next_pipes, input_data)

                    ge[x].fitness += 0.01
                    if bird.y == 0:
                        bird.alive = False
                    output = nets[x].activate(
                        (input_data[0], input_data[1], input_data[2], input_data[3],
                         input_data[4]))  # , input_data[5], input_data[6]))  # , input_data[4]))
                    if output[0] > 0.5 and time > 135:
                        bird.jump()
                        radio.wing_sound()
            # end game
            if len(birds) == 0:
                settings['Sound Volume'] = volume_holder
                running = False

            # start birds falling
            if time == 135:
                for bird in birds:
                    bird.falling = True

            if Testing and time == 500:
                game_flow['Leave_flow'] = True
                settings['Sound Volume'] = volume_holder
    return True
