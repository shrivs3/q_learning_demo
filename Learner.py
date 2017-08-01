__author__ = 'philippe'
import World
import threading
import time


##-------------------------------------------------
# Initializing the game world and the Q matrix

discount = 0.3
#importing just possible actions in World
actions = World.actions
states = []
Q = {}

#x and y are 2 variables set in World
for i in range(World.x):
    for j in range(World.y):
        states.append((i, j))
# states just has all the possible positions as tuples of x,y

#for each tuple, here box, the cost or Q value of choosing an action has been given as 0.1
for state in states:
    temp = {}
    for action in actions:
        temp[action] = 0.1
        World.set_cell_score(state, action, temp[action])
    Q[state] = temp
#the state, action and the cost has been stored in the set_cell_store in the World variable

# For the special boxes, different Q values are stored.
for (i, j, c, w) in World.specials:
    for action in actions:
        Q[(i, j)][action] = w
        World.set_cell_score((i, j), action, w)

##-------------------------------------------------
# Running the function

def do_action(action):
    s = World.player
    r = -World.score
    if action == actions[0]:
        World.try_move(0, -1)
    elif action == actions[1]:
        World.try_move(0, 1)
    elif action == actions[2]:
        World.try_move(-1, 0)
    elif action == actions[3]:
        World.try_move(1, 0)
    else:
        return
    s2 = World.player
    r += World.score
    return s, action, r, s2

# for a given postition or state s, it gives us the action which results in the 
# maximum reward and the reward value.
def max_Q(s):
    val = None
    act = None
    for a, q in Q[s].items():
        if val is None or (q > val):
            val = q
            act = a
    return act, val


def inc_Q(s, a, alpha, inc):
    Q[s][a] *= 1 - alpha
    Q[s][a] += alpha * inc
    World.set_cell_score(s, a, Q[s][a])


def run():
    global discount
    time.sleep(1)
    alpha = 1
    t = 1
    while True:
        # Pick the right action
        # World.player is the starting position of the player / Starting state
        s = World.player
        # get the maximum reward with the action from the state s
        max_act, max_val = max_Q(s)
        #returns the variables after executing the action
        (s, a, r, s2) = do_action(max_act)

        # Update Q
        max_act, max_val = max_Q(s2)
        inc_Q(s, a, alpha, r + discount * max_val)

        # Check if the game has restarted
        t += 1.0
        if World.has_restarted():
            World.restart_game()
            time.sleep(0.01)
            t = 1.0

        # Update the learning rate
        alpha = pow(t, -0.1)

        # MODIFY THIS SLEEP IF THE GAME IS GOING TOO FAST.
        time.sleep(0.1)


t = threading.Thread(target=run)
t.daemon = True
t.start()
World.start_game()
