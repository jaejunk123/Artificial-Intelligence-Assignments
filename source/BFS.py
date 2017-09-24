# -*- coding:utf8 -*-
# 8 puzzle을 BFS로 품

from node import Node
from eightpuzzle import EightPuzzle, UP, DOWN, LEFT, RIGHT

import copy
import random

# 가능한 움직임들
DIRECTIONS = [UP, DOWN, LEFT, RIGHT]

# 해당 node의 state와 depth를 출력
def log(node):
    print('current state : {0}, depth : {1}'.format(node.get_data().get_state(), node.get_depth()))

# 부모 node와 중복인지 아닌지 체크
def check_duplication_of_parent(node):
    parent = node.get_parent()

    while True:
        if node.get_data().get_state() == parent.get_data().get_state():
            return True

        if parent.get_depth() == 0:
            return False

        parent = parent.get_parent()

# node 확장
def make_nodes(node):
    # 일단 먼저, depth와 puzzle을 받음
    puzzle = node.get_data()
    depth = node.get_depth()

    # actions 리스트 생성 (directions로부터 복사)
    actions = DIRECTIONS[:]

    # 혹시나 해서 임의의 action을 취하도록 했습니다.
    random.shuffle(actions)

    # 확장할 node들
    nodes = []

    for action in actions:
        # 가능하지 않은 action이면 통과
        if not puzzle.check_possible_direction(action):
            continue

        # 일단 현재 게임 상황 복사
        copied = copy.deepcopy(puzzle)
        # 그리고 action 취해보기
        copied.act(action)

        # 그 게임 상황을 가지고 새로운 node 만들기
        new_node = Node(depth + 1, copied)
        new_node.set_parent(node)

        # 근데 부모랑 중복이면 패스
        if check_duplication_of_parent(new_node):
            continue
        
        # 추가
        nodes.append(new_node)

    return nodes

def search(initial_node):
    # fringe 초기 값
    fringe = [initial_node]

    while fringe:
        # FILO 형식
        node = fringe.pop(0)
        current_puzzle = node.get_data()

        # log 찍기
        log(node)

        # 게임 끝났으면
        if current_puzzle.is_end():
            return node

        # 아니면 확장
        fringe.extend(make_nodes(node))

    return False

def run(times):
    # 초기값 만들기
    puzzle = EightPuzzle() 
    puzzle.shuffle(times) # puzzle 섞기

    # 결과
    result = search(Node(0, puzzle))

    # 출력
    print("Final Depth : {0}".format(result.get_depth()))

if __name__ == "__main__":
    # 15번 섞은거 찾는걸 100번 돌림
    # 평균내자
    for _ in range(100):
        run(15)