from collections import Counter
import numpy as np
import os
# import pygame
import random
from enum import Enum

parameters = {'width':1000, 'height':1000, 'ants': 20, 'nodes': 7, 'max_line_thickness':10, 'min_line_thickness': 1}

class Direction(Enum):
    FORWARDS = 0
    BACKWARDS = 1

class Ant:
    def __init__(self):
        self.direction = Direction.FORWARDS
        self.pheromone = 100
        self.current_path = None
        self.remaining_distance = 0
        self.current_node = 0
        self.path = []

    def __repr__(self):
        return str(self.current_node) + '\t'

class Node:
    def __init__(self, start, goal, x, y):
        self.start = start
        self.goal = goal
        self.x = x
        self.y = y

def init_graph():
    nodes = []
    random.seed()
    goal_node = random.randrange(2, parameters['nodes'])
    for i in range(parameters['nodes']):
        x = -1
        y = -1
        for node in nodes:
            counter = 0
            while abs(node.x - x) < 70 or x < 0:
                random.seed()
                x = random.randrange(1, parameters['width'])
                counter += 1
                if counter == 100:
                    exit('The number of nodes is too high!')
            counter = 0
            while abs(node.y - y) < 70 or y < 0:
                random.seed()
                y = random.randrange(1, parameters['height'])
                counter += 1
                if counter == 100:
                    exit('The number of nodes is too high!')
        if len(nodes) == 0:
            start = True
        else:
            start = False
        if i + 1 == goal_node:
            goal = True
        else:
            goal = False
        node = Node(start, goal, x, y)
        nodes.append(node)
    paths = np.zeros((len(nodes), len(nodes)))
    for i in range(len(nodes)):
        for j in range(i, len(nodes)):
            if i != j:
                paths[i][j] = paths[j][i] = random.randrange(1, random.randrange(10, 100))
            else:
                paths[i][j] = 0
    # for i in range(len(paths)):
    #     obstacle = random.randrange(0, len(nodes))
    #     while obstacle == i:
    #         obstacle = random.randrange(0, len(nodes))
    #     paths[i][obstacle] = paths[obstacle][i] = 100000
    return nodes, paths

def new_node(probability, nodes):
    return node(probability.index(max(probability)))

def init_ants(nodes, pheromones, desirability):
    ants = []
    for i in range(parameters['ants']):
        ant = Ant()
        # for index, n in enumerate(nodes):
        #     if n.start:
        #             ant.nodes.append(n)
        #     ant.nodes.append(new_node(probability, nodes.copy()))
        # for i in range(1, len(nodes)):
        #     pass
        ants.append(ant)
    return ants

def main():
    all_paths = []
    nodes, paths = init_graph()
    t0 = parameters['ants'] / (parameters['nodes'] * paths.mean())
    pheromones = np.zeros((len(nodes), len(nodes)))
    desirability = np.zeros((len(nodes), len(nodes)))
    for i in range(len(nodes)):
        for j in range(i, len(nodes)):
            if i != j:
                pheromones[i][j] = pheromones[j][i] = t0
            else:
                pheromones[i][j] = 0
    desirability = 1 / np.array(paths)
    desirability = np.where(desirability == np.inf, 0, desirability)
    ants = init_ants(nodes, pheromones.copy(), desirability.copy())
    ######## PyGame

    FPS = 6000
    # clock = pygame.time.Clock()
    # pygame.init()
    # win = pygame.display.set_mode((parameters['width'], parameters['height']))
    # ant_image = pygame.image.load(os.path.join('', 'ant_right.jpg'))
    run = True
    while run:
        # clock.tick(FPS)
        # for event in pygame.event.get():
            # if event.type == pygame.QUIT:
        #         run = False
        # win.fill((0, 0, 0))
        # thick_arr = desirability * pheromones
        # for index, node1 in enumerate(nodes):
        #     for index2, node2 in enumerate(nodes[index + 1:]):
        #         thickness = int((thick_arr[index][index2 + index] - thick_arr.min()) / (thick_arr.max() - thick_arr.min() + 0.01) * parameters['max_line_thickness'])
                # pygame.draw.line(win, (0, 0, 255), (node1.x,node1.y), (node2.x,node2.y),thickness)
                # font = pygame.font.Font('freesansbold.ttf', 16)
                # text = font.render(str(paths[index][index + index2 + 1]), True, (128,0,0), (0,128,0))
                # textRect = text.get_rect()
                # textRect.center = ((node1.x + node2.x) / 2, (node1.y + node2.y) / 2)
                # win.blit(text, textRect)
        # for index, node in enumerate(nodes):
        #     if node.goal:
        #         color = (0, 128, 0)
        #     elif node.start:
        #         color = (255, 0, 0)
        #     else:
        #         color = (255, 255, 255)
            # pygame.draw.circle(win, color, (node.x, node.y), 50)
            # font = pygame.font.Font('freesansbold.ttf', 16)
            # text = font.render(str(index), True, (128,0,0), (0,128,0))
            # textRect = text.get_rect()
            # textRect.center = ((node1.x + node2.x) / 2, (node1.y + node2.y) / 2)
            # win.blit(text, textRect)
        probabilities = pheromones * desirability
        # probabilities = probabilities / probabilities.sum()
        print('Probabilities')
        print(probabilities)
        probability = probabilities.copy()
        for i in range(len(probabilities)):
            for j in range(i, len(probabilities[i])):
                if i != j:
                    probability[i][j] = probability[j][i] = (probabilities[i][j] - probabilities[i].min()) / (probabilities[i].max() - probabilities[i].min() + 0.001)
                else:
                    probability[i][j] = 0
        probabilities = probability
        print(probabilities)
        for ant in ants:
            if (nodes[ant.current_node].goal or nodes[ant.current_node].start) and len(ant.path) > 1:
                print('PATH: ' + str(ant.path))
                all_paths.append(str(ant.path))
                ant.path.reverse()
                all_paths.append(str(ant.path))
                ant.path.reverse()
                print('MOST FREQUENT PATH!!!!!!!!!!!!!!!!!!!!!!!!')
                most_frequent = {}
                for path in all_paths:
                    if path in most_frequent:
                        most_frequent[path] += 1
                    else:
                        most_frequent[path] = 1
                print(max(most_frequent))
                if nodes[ant.current_node].start:
                    total = sum(ant.path)
                    beg = ant.path[0]
                    for i in range(1, len(ant.path)):
                        end = ant.path[i]
                        pheromones[beg][end] = pheromones[end][beg] = pheromones[beg][end] + paths[beg][end] / total
                        beg = ant.path[i]
                ant.path = [ant.current_node]
            else:

                print('Ants')
                print(ants)
                print('Pheromones')
                print(pheromones)
                print('Paths')
                print(paths)
                for index, node in enumerate(nodes):
                    if node.goal:
                        print('GOAL: ' + str(index))
                    if node.start:
                        print('START: ' + str(index))
            # if ant.current_path == None:
                prob = probabilities[ant.current_node].copy()
                for i in range(len(nodes)):
                    if i in ant.path:
                        prob[i] = 0
                prob[ant.current_node] = 0
                node_prob = prob.copy()
                prob = np.sort(prob)
                prob_sum = prob.cumsum()
                # if len(ant.path) > 0 and ant.direction == Direction.FORWARDS:
                #     node_prob[ant.path[-1][1]] = 0
                # elif len(ant.backwards_path) > 0 and ant.direction == Direction.BACKWARDS:
                #     node_prob[ant.backwards_path[-1][1]] = 0
                print('Probabilities')
                print(probabilities)
                print('Cumulative')
                print(prob_sum)
                random.seed()
                num = random.random()
                i = 0
                print('Num: ' + str(num))
                while num > prob_sum[i] and i < len(prob) - 1:
                    i += 1
                i = np.where(prob[i] == node_prob)[0][0]
                print(prob)
                print(node_prob)
                print('Current node: ' + str(ant.current_node))
                print('Probability:' + str(node_prob[i]))
                # ant.current_path = i
                print('Next node: ' + str(i))
                if ant.current_node == i:
                    print('huge bug')
                if len(ant.path) > 0 and ant.path[-1] == i:
                    print('huge bug')
                ant.path.append(ant.current_node)
                ant.current_Node = i
            # ant.remaining_distance = paths[ant.current_node][i]
                # if ant.direction == Direction.FORWARDS:
                #     ant.path.append(ant.current_node)
                # else:
                #     ant.backwards_path.append(ant.current_node)
                #     pheromones[ant.current.node][i] += 1
                #     pheromones[i][ant.current.node] += 1
                #     print(nodes[ant.current_node])
                #     if nodes[ant.current_node].goal:
                #         ant.direction = Direction.BACKWARDS
                #         ant.path = []
                #     elif nodes[ant.current_node].start:
                #         ant.direction = Direction.FORWARDS
                #         ant.path = []
                #         break
            # else:
            #     print('travelling')
            #     ant.remaining_distance -= 1
            #     if ant.remaining_distance == 0:
            #         print('ANT REACHED A NODE')
            #         # for index, node1 in enumerate(nodes):
            #         #     for index2, node2 in enumerate(nodes[index + 1:]):
            #         #         thickness = int((thick_arr[index][index2 + index] - thick_arr.min()) / (thick_arr.max() - thick_arr.min() + 0.01) * parameters['max_line_thickness'])
            #                 # pygame.draw.line(win, (0, 0, 255), (node1.x,node1.y), (node2.x,node2.y),thickness)
            #                 # font = pygame.font.Font('freesansbold.ttf', 16)
            #                 # text = font.render(str(paths[index][index + index2 + 1]), True, (128,0,0), (0,128,0))
            #                 # textRect = text.get_rect()
            #                 # textRect.center = ((node1.x + node2.x) / 2, (node1.y + node2.y) / 2)
            #                 # win.blit(text, textRect)
            #         ant.current_node = ant.current_path
            #         ant.current_path = None
            #         if nodes[ant.current_node].goal or nodes[ant.current_node].start:
            #             print('PATH: ' + str(ant.path))
            #             all_paths.append(str(ant.path))
            #             ant.path.reverse()
            #             all_paths.append(str(ant.path))
            #             ant.path.reverse()
            #             print('MOST FREQUENT PATH!!!!!!!!!!!!!!!!!!!!!!!!')
            #             most_frequent = {}
            #             for path in all_paths:
            #                 if path in most_frequent:
            #                     most_frequent[path] += 1
            #                 else:
            #                     most_frequent[path] = 1
            #             print(max(most_frequent))
            #             if nodes[ant.current_node].start:
            #                 total = sum(ant.path)
            #                 beg = ant.path[0]
            #                 for i in range(1, len(ant.path)):
            #                     end = ant.path[i]
            #                     pheromones[beg][end] = pheromones[end][beg] = pheromones[beg][end] + 10 * paths[beg][end] / total
            #                     beg = ant.path[i]
            #             ant.path = []
            pheromones = (1 - 0.01) * pheromones
            pheromones = np.where(pheromones < 0.01, 0.01, pheromones)
        # pygame.display.update()

    # pygame.quit()

if __name__ == '__main__':
    main()
