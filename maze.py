import maze_env
import get_voice_command
import cozmo_controller
import cozmo

def set_ads(angle, distance, speed):
    cozmo_controller.angle = angle
    cozmo_controller.distance = distance
    cozmo_controller.speed = speed


env = maze_env.MazeEnv()
#cozmo = cozmo_bot.Cozmo() # initilization
state = env.reset()
done = False

while not done:
    angle, distance, speed, action = get_voice_command.get_command_from_keyboard()
    print(action, type(action))
    state, reward, hit_wall, front, done, _ =env.step(action) 
    if hit_wall:
        # if hit wall, show attemptation
        set_ads(0, 10, 10)
        cozmo.run_program(cozmo_controller.act)
        set_ads(0, -10, 10)
        cozmo.run_program(cozmo_controller.act)
        cozmo_controller.front = "hit"
        cozmo.run_program(cozmo_controller.cozmo_show_img)
    else:    
        set_ads(angle, distance, speed)
        cozmo.run_program(cozmo_controller.act)
    cozmo_controller.front = front
    cozmo.run_program(cozmo_controller.cozmo_show_animation)
    
    #cozmo.run_program(cozmo_expression)
    print(state, reward, hit_wall, front, done)
    print(env.maze)