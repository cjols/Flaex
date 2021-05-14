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


        # calculations
        my_goal_to_ball, ball_to_my_goal = (agent.ball.location - agent.friend_goal.location).normalize(True)
        op_goal_to_ball, ball_to_op_goal = (agent.ball.location - agent.foe_goal.location).normalize(True)

        my_goal_to_me = agent.me.location - agent.friend_goal.location
        op_goal_to_op = agent.foes[0].location - agent.foe_goal.location

        me_to_my_goal = my_goal_to_ball.dot(my_goal_to_me)
        op_to_op_goal =  op_goal_to_ball.dot(op_goal_to_op)

        my_point = agent.friend_goal.location + (my_goal_to_ball * me_to_my_goal)
        op_point = agent.foe_goal.location + (op_goal_to_ball * op_to_op_goal)


        # lines
        agent.line(agent.friend_goal.location, agent.ball.location, [255,255,255])
        agent.line(my_point - Vector3(0,0,100), my_point + Vector3(0,0,100), [0,255,0])


        # definitions
        me_close = (agent.me.location - agent.ball.location).magnitude() < BALL_AGRO
        op_close = (agent.foes[0].location - agent.ball.location).magnitude() < BALL_AGRO

        me_have_boost = agent.me.boost > BOOST_AGRO
        op_have_boost = agent.foes[0].boost > BOOST_AGRO

        me_onside = me_to_my_goal - OFFSIDE_AGRO > ball_to_my_goal
        op_onside = op_to_op_goal - OFFSIDE_AGRO > ball_to_op_goal


        # if agent.team == 0:
        #     agent.debug_stack()
        #     print(me_close)

        # kickoff
        if len(agent.stack) < 1:
            if agent.kickoff_flag:
                agent.push(kickoff())

            elif (me_close and me_onside) or (not op_onside and me_onside):
                left_field = Vector3(4200 * -side(agent.team),agent.ball.location.y + (1000 * -side(agent.team)), 0)
                right_field = Vector3(4200 * side(agent.team),agent.ball.location.y + (1000 * -side(agent.team)), 0)
                targets = {"goal":(agent.foe_goal.left_post, agent.foe_goal.right_post), "upfield": (left_field,right_field)}
                shots = find_hits(agent, targets)

                if len(shots["goal"]) > 0:
                    agent.push(shots["goal"][0])
                elif len(shots["upfield"]) > 0 and abs(agent.friend_goal.location.y - agent.ball.location.y) < 8490:
                    agent.push(shots["upfield"][0])

            # elif not me_onside

            else:
                relative_target = agent.friend_goal.location - agent.me.location
                angles = defaultPD(agent, agent.me.local(relative_target))
                defaultThrottle(agent, 2300)

                agent.controller.boost = False if abs(angles[1]) > 0.5 or agent.me.airborne else agent.controller.boost
                agent.controller.handbrake = True if abs(angles[1]) > 2.8 else False

