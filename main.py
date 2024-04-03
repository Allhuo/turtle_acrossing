import random
import time
from turtle import Screen

from car_manager import CarManager
from player import Player, FINISH_LINE_Y

# 初始化屏幕
screen = Screen()
screen.setup(width=600, height=600)
screen.tracer(0)

# 初始化玩家
player = Player()

# 初始化车流
cars = []
y_positions = []
last_car_time = time.time()
car_spawn_interval = 1.0  # 车辆生成间隔为1秒


# 生成不重叠的车辆Y坐标
def generate_non_overlapping_car(cars_list, y_positions, safe_distance=20):
    new_ycor = random.randint(-250, 250)

    # 检查y轴位置是否重叠
    for existing_ycor in y_positions:
        if abs(new_ycor - existing_ycor) < safe_distance:
            # 如果在y轴上发现重叠，检查所有重叠的车辆是否都在新车辆的x轴位置的右边
            for car in cars_list:
                if car.ycor() == existing_ycor and car.xcor() >= 250:
                    # 发现了重叠并且至少有一辆车不在右边，返回None表示失败
                    return None
            # 如果代码执行到这里，意味着所有重叠的车辆都在右边
            break  # 不需要检查其他的y坐标了

    # 没有发现重叠，或者所有重叠的车辆都在右边
    return new_ycor


# 键盘监听
screen.listen()
screen.onkeypress(player.move_up, "Up")

game_is_on = True
while game_is_on:
    time.sleep(0.1)
    screen.update()
    # 创建车流
    if time.time() - last_car_time > car_spawn_interval:
        new_y = None
        while new_y is None:
            new_y = generate_non_overlapping_car(cars, y_positions)
        new_car = CarManager(new_y)
        y_positions.append(new_y)
        cars.append(new_car)
        last_car_time = time.time()

    # 车流移动
    for car in cars:
        car.move_left()

    # 检查车辆是否离开屏幕,如果是,将其从列表中删除
    for car in cars[:]:  # 创建一个cars列表的副本,避免在遍历过程中修改原列表
        if car.xcor() < -300:
            car.hideturtle()
            y_cor_to_remove = int(car.ycor())
            if y_cor_to_remove in y_positions:
                y_positions.remove(y_cor_to_remove)
            else:
                print(f"Trying to remove {y_cor_to_remove}, but it's not in the list.")
            cars.remove(car)  # 将车辆从列表中删除

    # 检查是否失败
    for car in cars:
        if player.distance(car) < 10:
            game_is_on = False

    # 检查是否过关
    if player.ycor() > FINISH_LINE_Y:
        player.reset_position()
        car_spawn_interval *= 0.8
        for car in cars:
            car.hideturtle()
        cars = []
        y_positions = []

screen.exitonclick()
