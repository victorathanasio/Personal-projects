import utils.NEAT
import neat
import os
import pickle


local_dir = os.path.dirname(__file__)
config_path = local_dir[:-5] + r'\Assets\NEAT_config.txt'
config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                            neat.DefaultSpeciesSet, neat.DefaultStagnation,
                            config_path)


genome_path = local_dir[:-5] + r"Assets\AI_models\winner.pkl"
with open(genome_path, "rb") as f:
    genome = pickle.load(f)

net = neat.nn.FeedForwardNetwork.create(genome, config)


def monkey_patch(bird, next_pipes, input_data):
    utils.NEAT.get_AI_input(bird, next_pipes, input_data)

    output = net.activate((input_data[0], input_data[1], input_data[2], input_data[3],
                           input_data[4], input_data[5], input_data[6]))  # , input_data[4]))
    if output[0] > 1:
        return True
