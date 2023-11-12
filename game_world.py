objects = [[] for _ in range(4)]


collision_pairs={} # 'boy:ball' : {[[boy],[ball1,ball2...]]} #충돌세계

def add_collision_pairs(group,a=None,b=None): #a,b 사이에 충돌검사 필요
    if group not in collision_pairs:
        print(f'Added new group {group} ')
        collision_pairs[group]=[[],[]]
    if a:
        collision_pairs[group][0].append(a)
    if b:
        collision_pairs[group][1].append(b)

def add_object(o, depth = 0):
    objects[depth].append(o)

def add_objects(ol, depth = 0):
    objects[depth] += ol


def update():
    for layer in objects:
        for o in layer:
            o.update()


def render():
    for layer in objects:
        for o in layer:
            o.draw()


def remove_object(o):
    for layer in objects:
        if o in layer:
            layer.remove(o)
            return
    raise ValueError('Cannot delete non existing object')

def clear():
    for layer in objects:
        layer.clear()


def collide(a,b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if (left_a>right_b):return False
    if (right_a<left_b):return False
    if (top_a<bottom_b):return False
    if (bottom_a>top_b):return False

    return True

def handle_collisions():
    for group, pairs in collision_pairs.items():
        for a in pairs[0]:
            for b in pairs[1]:
                if collide(a,b):
                    a.handle_collision(group,b)
                    b.handle_collision(group,a)
