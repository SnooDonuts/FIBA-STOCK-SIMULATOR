from ursina import *
import random

app = Ursina()

stock_names = [line.strip() for line in open('stock_names.txt', 'r').readlines()]

max_value = 500
graph_scale = 2
graph_entities = []
score = 100.0

score_text = Text(text=f'Score: {score}', position=(-0.8, 0.3), origin=(0, 0))
result_background = Entity(parent=camera.ui, model='quad', scale=(1.5, 0.3), color=color.black66, visible=False, z=-0.1)
result_text = Text(text='', parent=result_background, origin=(0, 0), color=color.yellow, scale=(2, 10), z=-0.1)
stock_title = Text(text='', position=(0, 0.4), origin=(0, 0), scale=2, color=color.white)


def create_axis_and_labels(center_offset, graph_width):
    x_axis = Entity(model=Mesh(vertices=[Vec3(center_offset, -2, 0), Vec3(center_offset + graph_width, -2, 0)], mode='line'), color=color.white)
    y_axis = Entity(model=Mesh(vertices=[Vec3(center_offset, -2, 0), Vec3(center_offset, 3, 0)], mode='line'), color=color.white)
    time_label = Text(text='Time', position=(center_offset + graph_width / 2, -0.3), origin=(0, 0), scale=1, color=color.white)
    money_label = Text(text='Money (USD)', position=(-0.7, 0), origin=(0, 0), scale=1, rotation=(0, 0, 270), color=color.white)
    graph_entities.extend([x_axis, y_axis, time_label, money_label])

def create_points_and_lines(points, graph_width):
    for i, (x, y) in enumerate(points):
        line_color = color.green if i == 0 or y > points[i - 1][1] else color.red

        # Vertical line to X-axis
        vertical_line = Entity(model=Mesh(vertices=[Vec3(x, -1.9, 0), Vec3(x, -2.1, 0)], mode='line'), color=color.white)
        graph_entities.append(vertical_line)
        # Label on X-axis
        x_label = Text(text=f'{i}', position=(x, -2.2), origin=(0, 0), scale=1, color=color.white)
        graph_entities.append(x_label)

        # Horizontal line to Y-axis
        horizontal_line = Entity(model=Mesh(vertices=[Vec3(-graph_width / 2-0.2, y, 0), Vec3(-graph_width / 2+0.2, y, 0)], mode='line'), color=color.white)
        graph_entities.append(horizontal_line)
        # Label on Y-axis
        y_label = Text(text=f'{int(y / graph_scale * max_value)}', position=(-graph_width / 2 - 0.1, y), origin=(0, 0), scale=1, color=color.white)
        graph_entities.append(y_label)

        # Line and point on the graph
        if i > 0:
            point_a = points[i - 1]
            line_entity = Entity(model=Mesh(vertices=[Vec3(point_a[0], point_a[1], 0), Vec3(x, y, 0)], mode='line'), color=line_color)
            graph_entities.append(line_entity)
        point_entity = Entity(model='sphere', scale=0.1, color=line_color, position=(x, y, 0))
        graph_entities.append(point_entity)

    # Last point doesn't connect to a new line, so only a point entity is added.


def draw_graph(data_points, stock_name):
    global graph_entities
    stock_title.text = stock_name
    num_points = len(data_points)
    graph_width = num_points - 1
    center_offset = -graph_width / 2
    points = [(i + center_offset, y / max_value * graph_scale) for i, y in enumerate(data_points)]
    create_axis_and_labels(center_offset, graph_width)
    create_points_and_lines(points, graph_width)


def generate_datapoints():
    return [random.randint(10, 500) for _ in range(11)]


def generate_score():
    return round(float(random.randint(1000, 100000)) / 100.0, 2)


def remove_old_graph():
    global graph_entities
    for entity in graph_entities:
        destroy(entity)
    graph_entities = []


def update_result(n, success):
    global score, result_text
    if success:
        score = round(score + n, 2)
        result_text.text = f'You Won {n}USD!'
        result_text.color = color.green
    else:
        score = round(score - n, 2)
        result_text.text = f'You Lost {n}USD!'
        result_text.color = color.red
    score_text.text = f'Score: {score}'
    result_background.visible = True
    result_text.visible = True
    invoke(hide_result, delay=1)


def buy():
    global score
    buy_button.disable()
    sell_button.disable()
    remove_old_graph()
    stock_name = random.choice(stock_names)
    draw_graph(generate_datapoints(), stock_name)
    n = generate_score()
    update_result(n, random.random() > 0.6)


def hide_result():
    result_background.visible = False
    result_text.visible = False
    buy_button.enable()
    sell_button.enable()


draw_graph(generate_datapoints(), random.choice(stock_names))

buy_button = Button(text="Buy", color=color.green, position=(-0.5, -0.4), scale=(0.2, 0.1))
buy_button.on_click = buy

sell_button = Button(text="Sell", color=color.red, position=(0.5, -0.4), scale=(0.2, 0.1))
sell_button.on_click = buy

app.run()
