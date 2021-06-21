import numpy as np
import os
import pygame
import random
from enum import Enum

parameters = {'width':1000, 'height':1000, 'ants': 20, 'nodes': 5, 'max_line_thickness':10, 'min_line_thickness': 1}

class Direction(Enum):
    FORWARDS = 0
    BACKWARDS = 1

class Ant:
    def __init__(self):
        self.direction = Direction.FORWARDS
        self.pheromone = 100
        self.current_node = 0
        self.path = []
        self.backwards_path = []

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
    goal_node = random.randrange(2, parameters['nodes'])
    for i in range(parameters['nodes']):
        x = -1
        y = -1
        for node in nodes:
            counter = 0
            while abs(node.x - x) < 70 or x < 0:
                x = random.randrange(1, parameters['width'])
                counter += 1
                if counter == 100:
                    exit('The number of nodes is too high!')
            counter = 0
            while abs(node.y - y) < 70 or y < 0:
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
    for i, _ in enumerate(nodes):
        for j, _ in enumerate(nodes):
            paths[i][j] = int(((nodes[i].x - nodes[j].x) ** 2 + (nodes[i].y - nodes[j].y) ** 2) ** (1/2) / 100)
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
    nodes, paths = init_graph()
    t0 = parameters['ants'] / (parameters['nodes'] * paths.mean())
    pheromones = np.zeros((len(nodes), len(nodes)))
    desirability = np.zeros((len(nodes), len(nodes)))
    for i in range(len(nodes)):
        for j in range(len(nodes)):
            pheromones[i][j] = t0
    desirability = 1 / np.array(paths)
    desirability = np.where(desirability == np.inf, 0, desirability)
    evap = 0.1
    ants = init_ants(nodes, pheromones.copy(), desirability.copy())
    ######## PyGame

    FPS = 1
    clock = pygame.time.Clock()
    win = pygame.display.set_mode((parameters['width'], parameters['height']))
    ant_image = pygame.image.load(os.path.join('', 'ant_right.jpg'))
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        win.fill((0, 0, 0))
        thick_arr = desirability * pheromones
        for index, node1 in enumerate(nodes):
            for index2, node2 in enumerate(nodes[index + 1:]):
                thickness = int((thick_arr[index][index2 + index + 1] - thick_arr.min()) / (thick_arr.max() - thick_arr.min()) * parameters['max_line_thickness'])
                pygame.draw.line(win, (0, 0, 255), (node1.x,node1.y), (node2.x,node2.y),thickness)
        for node in nodes:
            if node.goal:
                color = (0, 128, 0)
            elif node.start:
                color = (255, 0, 0)
            else:
                color = (255, 255, 255)
            pygame.draw.circle(win, color, (node.x, node.y), 50)
        probabilities = []
        for index, _ in enumerate(nodes):
            probability = pheromones[index] * desirability[index]
            probability[index] = 0
            probabilities.append(probability)
        probabilities = np.array(probabilities / sum(probabilities))
        print(ants)
        print(pheromones)
        for ant in ants:
            prob = probabilities[ant.current_node].copy()
            print(prob.shape)
            probabilities = probabilities[ant.current_node].copy()
            print(prob.shape[0])
            prob = np.sort(prob)
            for i in range(prob.shape[0]):
                prob[i] = (prob[i] - min(prob)) / (max(prob) - min(prob))
            if len(ant.path) > 0 and ant.direction == Direction.FORWARDS:
                prob[ant.path[-1][1]] = 0
            elif len(ant.backwards_path) > 0 and ant.direction == Direction.BACKWARDS:
                prob[ant.backwards_path[-1][1]] = 0
            num = random.random()
            if num < prob[0]:
                ant.current_node = np.where(probabilities == prob[0])[0][0]
                if ant.direction == Direction.FORWARDS:
                    ant.path.append((ant.current_node, 0))
                else:
                    ant.backwards_path.append((ant.current_node, 0))
                for i in range(1, len(prob)):
                    if num > prob[i - 1] and num < prob[i]:
                        pheromones[ant.current_node][i] += 0.1
                        ant.current_node = np.where(probabilities == prob[i])[0][0]
                        if ant.direction == Direction.FORWARDS:
                            ant.path.append((ant.current_node, i))
                        else:
                            ant.backwards_path.append((ant.current_node, i))
                        if nodes[current_node].goal:
                            ant.direction = Direction.BACKWARDS
                            ant.path = []
                        elif nodes[current_node].start:
                            ant.direction = Direction.FORWARDS
                            ant.backwards_path = []
                        break
            pheromones -= 0.1
        pygame.display.update()

    pygame.quit()

if __name__ == '__main__':
    main()
