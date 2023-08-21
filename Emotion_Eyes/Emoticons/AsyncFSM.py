# import cozmo
# import asyncio
# from PIL import Image

# class CozmoFSM:
#     def __init__(self):
#         self.current_state = self.explore_state
#         self.current_mood = "neutral.png"
    
#     async def explore_state(self, robot: cozmo.robot.Robot):
#         print("Exploring...")
#         self.current_mood = "happy.png"
#         await self.display_mood(robot)
#         await asyncio.sleep(5)
#         self.current_mood = "neutral.png"
#         await self.display_mood(robot)
    
#     async def interact_state(self, robot: cozmo.robot.Robot):
#         print("Interacting...")
#         self.current_mood = "sad.png"
#         await self.display_mood(robot)
#         await asyncio.sleep(3)
#         self.current_mood = "neutral.png"
#         await self.display_mood(robot)
    
#     async def display_mood(self, robot: cozmo.robot.Robot):
#         image = Image.open(self.current_mood)
#         resized_image = image.resize(cozmo.oled_face.dimensions(), Image.BICUBIC)
#         face_image = cozmo.oled_face.convert_image_to_screen_data(resized_image)
#         robot.display_oled_face_image(face_image, duration_ms=2000)
    
#     async def run_fsm(self, robot: cozmo.robot.Robot):
#         while True:
#             await self.current_state(robot)

# def cozmo_program(robot: cozmo.robot.Robot):
#     fsm = CozmoFSM()
#     asyncio.run(fsm.run_fsm(robot))

# cozmo.run_program(cozmo_program)


import asyncio
async def fn():
    task=asyncio.create_task(fn2())
    print("one")
    #await asyncio.sleep(1)
    #await fn2()
    print('four')
    await asyncio.sleep(1)
    print('five')
    await asyncio.sleep(1)
  
async def fn2():
    #await asyncio.sleep(1)
    print("two")
    await asyncio.sleep(1)
    print("three")
      
asyncio.run(fn())