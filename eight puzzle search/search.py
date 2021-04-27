from abc import ABCMeta, abstractmethod
import util


class SearchProblem(metaclass=ABCMeta):
    @abstractmethod
    def get_start_state(self):
        pass

    @abstractmethod
    def is_goal_state(self, state):
        pass

    @abstractmethod
    def get_successor(self, state):
        # return (next_state, action, cost)
        pass

    @abstractmethod
    def get_costs(self, actions):
        pass

    @abstractmethod
    def get_goal_state(self):
        pass


class Node:
    def __init__(self, state, path=[], priority=0):
        self.state = state
        self.path = path
        self.priority = priority

    def __le__(self, other):
        return self.priority <= other.priority

    def __lt__(self, other):
        return self.priority < other.priority


def search(problem, fringe, calc_heuristic=None, heuristic=None):
    """
    This is an simple abstracted graph search algorithm. You could
    using different combination of fringe storage, calc_heuristic, heuristic
    to implement different search algorithm.

    For example:
    LIFO Queue(Stack), None, None -> Depth First Search
    FIFO Queue, None, None -> Breadth First Search
    PriorityQueue, cost compute function, None -> Uniform Cost Search

    In order to avoid infinite graph/tree problem we setup a list (visited) to
    avoid expanding the same node.

    hint: please check the node first before expanding:

    if node.state not in visited:
        visited.append(node.state)
    else:
        continue

    hint: you could get the successor by problem.get_successor method.

    hint: for fringe you may want to use
        fringe.pop  get a node from the fringe
        fringe.push   put a node into the fringe
        fringe.empty  check whether a fringe is empty or not. If the fringe is empty this function return True
        problem.is_goal_state check whether a state is the goal state
        problem.get_successor get all successor from current state
            return value: [(next_state, action, cost)]
    """
    start_state = problem.get_start_state()
    if isinstance(fringe, util.Stack) or isinstance(fringe, util.Queue):
        fringe.push(Node(start_state))
    else:
        fringe.push(Node(start_state), 0)
    visited = [start_state]
    step = 0

    while not fringe.empty():
        "*** YOUR CODE HERE ***"
        # TODO search
        node0 = fringe.pop()
        # print(node0.state)
        # print(node0.path)
        step = step + 1
        # print(step)

        if problem.is_goal_state(node0.state):
            return node0.path, step

        nodelist = problem.get_successor(node0.state)
        for i in range(len(nodelist)):
            sib_node = Node(state=nodelist[i][0], path=[])  # 这里不加 path=[]就会覆盖list......
            sib_path = nodelist[i][1]

            if sib_node.state not in visited:
                # 一开始我visited里面装的是Node不是state
                # 结果 if sib_node not in visited竟然恒为True！！！
                # 就导致了死循环...
                visited.append(sib_node.state)
                sib_node.path.extend(node0.path)
                sib_node.path.append(sib_path)
                # 判断是不是 PriorityQueue
                if calc_heuristic is not None:
                    sib_node.priority = calc_heuristic(problem=problem, successor=nodelist[i], node=node0,
                                                       heuristic=heuristic)
                    fringe.update(sib_node, sib_node.priority)
                else:
                    fringe.push(sib_node)
                    # DFS因为不可能找到最优解，因此在push的时候就检查是否达到目标值，如果在pop的时候检查，因为DFS的栈会被压得太深，因此step会特别多，导致根本运行不出来
                    if isinstance(fringe, util.Stack) and problem.is_goal_state(sib_node.state):
                        return sib_node.path, step

        "*** END YOUR CODE HERE ***"
    return [], step  # no path is found


def a_start_heuristic(problem, current_state):
    h = 0
    "*** YOUR CODE HERE ***"
    for i in range(3):
        for j in range(3):
            if current_state.cells[i][j] != problem.get_goal_state().cells[i][j]:
                h = h + 1
    # TODO a_start_heuristic
    "*** END YOUR CODE HERE ***"
    return h


def a_start_cost(problem, successor, node, heuristic):
    cost = 0
    "*** YOUR CODE HERE ***"
    # TODO a_start_cost
    cost = cost + node.priority + successor[2] + heuristic(problem, successor[0])
    "*** END YOUR CODE HERE ***"
    return cost


def a_start_search(problem):
    return search(problem, util.PriorityQueue(), a_start_cost, a_start_heuristic)


def ucs_compute_node_cost(problem, successor, node, heuristic):
    """
    Define the method to compute cost within unit cost search
    hint: successor = (next_state, action, cost).
    however the cost for current node should be accumulative
    problem and heuristic should not be used by this function
    """
    cost = 0
    "*** YOUR CODE HERE ***"
    # TODO ucs_compute_node_cost
    cost = cost + node.priority + successor[2]
    "*** END YOUR CODE HERE ***"
    return cost


def uniform_cost_search(problem):
    """
    Search the solution with minimum cost.
    """
    return search(problem, util.PriorityQueue(), ucs_compute_node_cost)


def breadth_first_search(problem):
    return search(problem, util.Queue())


def depth_first_search(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.get_start_state()
    print "Is the start a goal?", problem.is_goal(problem.get_start_state())
    print "Start's successors:", problem.get_successors(problem.get_start_state())

    hint: using util.Stack as the fringe
    """
    return search(problem, util.Stack())


