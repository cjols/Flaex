from tools import  *
from objects import *
from routines import *


#This file is for strategy

class Flaex(GoslingAgent):

    def run(agent):

        # variables
        BALL_AGRO = 2000
        BOOST_AGRO = 12
        OFFSIDE_AGRO = 200

        # my_distance_my_goal = abs(agent.friend_goal.location.y - agent.me.location.y)
        # op_distance_op_goal = abs(agent.foe_goal.location.y - agent.foes.location.y)
        # ball_distance_my_goal = abs(agent.friend_goal.location.y - agent.ball.location.y)
        # ball_distance_op_goal = abs(agent.foe_goal.location.y - agent.ball.location.y)


        # lines
        agent.line(agent.friend_goal.location, agent.ball.location, [255,255,255])


        my_goal_to_ball, ball_to_my_goal = (agent.ball.location - agent.friend_goal.location).normalize(True)
        my_goal_to_me = agent.me.location - agent.friend_goal.location
        me_to_my_goal = my_goal_to_ball.dot(my_goal_to_me)

        op_goal_to_ball, ball_to_op_goal = (agent.ball.location - agent.foe_goal.location).normalize(True)
        op_goal_to_op = agent.foes.location - agent.foe_goal.location
        op_to_op_goal =  op_goal_to_ball.dot(op_goal_to_op)


        # definitions
        close = (agent.me.location - agent.ball.location).magnitude() < BALL_AGRO
        have_boost = agent.me.boost > BOOST_AGRO

        me_onside = me_to_my_goal - OFFSIDE_AGRO > ball_to_my_goal
        op_onside = op_to_op_goal - OFFSIDE_AGRO > ball_to_op_goal


        if agent.team == 0:
            agent.debug_stack()
            print(close)

        # kickoff
        if len(agent.stack) < 1:
            if agent.kickoff_flag:
                agent.push(kickoff())

