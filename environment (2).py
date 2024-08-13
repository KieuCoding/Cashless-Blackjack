import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def main():
    # TUTORIAL
    
    # First: Create Environment Object
    env = trash_env() # returns environment
    random.seed(8)
    """
    # Second: Generate Environment
    env.gen_env()
    
    # Third: Can Obtain Information
    claw_pos = env.get_claw_pos() # returns claw position wxh
    boxes = env.get_objs() # returns list of boxes [xc, yc, w, h, label]
    
    # Fourth: Can Attempt to Grab Object
    xc = 320
    yc = 240
    w = 64
    h = 48
    success = env.grab([xc, yc, w, h]) # returns the success of grab
    
    # Fifth: Can Dump All Items
    env.dump()
    
    # Sixth: Can Manually Show Vis
    env.vis()
    """
    
    # Seventh: Can Automatically Show Visualization
    #env.toggle_verbose()
    
    # Eighth: Can Use to Benchmark
    # NOTE: Create Environment Outside of Loop
    for itera in range(100000):
        env.gen_env()
        
        ##############Your Code Starts Here###############
        def ymax(bboxes):
            ylist = [box[1] + int(box[3]/2) for box in bboxes]
            if env.get_objs():
                max_element = max(ylist)
                max_index = ylist.index(max_element)
            else:
                max_index = None
            return bboxes[max_index]
            
        
        def gather_hid_objs(target, bboxes):
            target_xmin = target[0] - int(target[2]/2)
            target_xmax = target[0] + int(target[2]/2)
            unreachable = []  
            for box in bboxes:
                box_xmin = box[0] - int(box[2]/2)
                box_xmax = box[0] + int(box[2]/2)
                if box == target:
                    pass
                elif target_xmin < box_xmin and target_xmax > box_xmin or \
                    target_xmin < box_xmax and target_xmax > box_xmax or \
                    box_xmin < target_xmin and box_xmax > target_xmin:
                        unreachable.append(box)
                        prev_xmin = box_xmin
                        prev_xmax = box_xmax
                        prev = box
                        for box in bboxes:
                            box_xmin = box[0] - int(box[2]/2)
                            box_xmax = box[0] + int(box[2]/2)
                            if box == target or box == prev:
                                pass
                            elif prev_xmin < box_xmin and prev_xmax > box_xmin or \
                                prev_xmin < box_xmax and prev_xmax > box_xmax or \
                                box_xmin < prev_xmin and box_xmax > prev_xmin:
                                    unreachable.append(box)
            return unreachable
        
            
                            
            
        """
        if itera == 88:
            env.toggle_verbose()
        elif itera == 89:
            assert False
        """
        blacklist = []
        while env.get_objs():   #if there is object True, if no objects false
            bboxes = env.get_objs()
            for box in reversed(bboxes):
                if box in blacklist:
                    bboxes.remove(box)
            if not bboxes:
                break
            target = ymax(bboxes)
            #bboxes.remove(target)
            
            for _ in range(5):
                success = env.grab(target[:-1])
                if success:
                    break   
            """
            if itera == 88:
                env.vis()
                print(f"bboxes {bboxes}")
                print(f"black {blacklist}")
                print(f"target {target}")
            """
            if not success:
                unreachable = gather_hid_objs(target, bboxes)
                blacklist.extend(unreachable + [target])
                bboxes.remove(target)
            
        
        
        ##################################################
        
        env.dump() # NOTE: Always Dump Before Generating New Environment
    env.analysis() # Analyzes Seach Effectiveness
    
def tony_search(iterations=100, seed=8, animation=False):
    print(f"Tony's Search Algorithm (seed: {seed})")
    random.seed(seed)
    
    env = trash_env()
    if animation:
        env.toggle_verbose()
    
    for _ in range(iterations):
        env.gen_env()
        
        def gather_hlines(boxes):
            lines = []
            for box in boxes:
                xc, yc, w, h, _ = box
                xmin = int(xc - w/2)
                xmax = int(xc + w/2) + 1
                ymax = int(yc + h/2) + 1
                lines.append([xmin, xmax, ymax, xc, yc, w, h])
            return lines
        
        def gather_posgrabs(lines):
            boxes = lines.copy()
            for line1 in lines:
                for line2 in lines:
                    if line1 == line2:
                        continue
                    if (line1[0] > line2[0] and line1[0] < line2[1] or 
                        line1[1] > line2[0] and line1[1] < line2[1] or 
                        line2[0] > line1[0] and line2[0] < line1[1]):
                        if line1[2] > line2[2]:
                            if line2 in boxes:
                                boxes.remove(line2)
                        else:
                            if line1 in boxes:
                                boxes.remove(line1)
            return [box[3:] for box in boxes]
        
        def l1_norm(obj_pos, claw_pos):
            return abs(claw_pos[0]-obj_pos[0]) + abs(claw_pos[1]-obj_pos[1])
        
        def close_obj(objs, claw_pos):
            dists = []
            for obj in objs:
                xc, yc, w, h = obj
                dists.append(l1_norm(claw_pos, (xc, yc)))
            return objs[dists.index(min(dists))]
        
        blacklist, hist = [], {}
        while(env.get_objs()):            
            targets = gather_posgrabs(gather_hlines(env.get_objs()))
 
            for target in reversed(targets): # fix bug in python loop
                if target in blacklist:
                    targets.remove(target)
            
            if not targets:
                break
            
            target = close_obj(targets, env.get_claw_pos())
            if tuple(target) in hist.keys():
                if hist[tuple(target)] > 1:
                    blacklist.append(target)
                hist[tuple(target)] += 1
                env.grab(target)
            else:
                hist[tuple(target)] = 1
                env.grab(target)
        
        env.dump()
    env.analysis()

class trash_env():
    def __init__(self, res=(640, 480), max_num_obj=10, verbose=False):
        # static variables
        self.res = res #wxh
        self.max_num_obj = max_num_obj
        self.verbose = verbose
        self.bins = [(0, res[1]), (res[0], res[1])]
        
        # dynamic variables
        self.claw_pos = (int(random.random()*self.res[0]), self.res[1])
        self.objs = []
        
        # global variables
        self.iter = 0

        self.grabs = 0
        self.grabbed = 0
        self.missed = 0
        self.cmissed = 0
        
        self.items = 0
        self.dumps = 0
        
        self.pixel = 0
    
    def gen_env(self):
        self.iter += 1
        
        # generate objects
        num_obj = random.randrange(1, self.max_num_obj)
        for _ in range(num_obj):
            item = trash()
            box1 = item.get_box()
            box1.pop()
            flag = True
            for obj in self.objs:
                box2 = obj.get_box()
                box2.pop()
                for i, j in zip(box1, box2):
                    if i == j:
                        flag = False
            if flag:
                self.objs.append(item)
        self.items += len(self.objs)
        
        if self.verbose:
            self.vis()
    
    def grab(self, pos):
        self.grabs += 1
        flag = False
        
        # if no object
        if not self.objs:
            self.cmissed += 1
            old_claw = self.claw_pos
            self.claw_pos = (pos[0], self.res[1])
            self.pixel += abs(old_claw[0] - self.claw_pos[0])
            
            if self.verbose:
                self.vis()
            return False
        
        # find index of target
        for i in range(len(self.objs)):
            box = self.objs[i].get_box()
            box.pop()
            if box == pos:
                flag = True
                break
        
        # gather target line
        box = self.objs[i].get_box()
        xmin = int(box[0] - box[2]/2)
        xmax = int(box[0] + box[2]/2) + 1
        ymax = int(box[1] + box[3]/2) + 1
        line = [xmin, xmax, ymax]
        
        # check horizontal lines
        for j in range(len(self.objs)):
            if j == i:
                continue
            
            box = self.objs[j].get_box()
            xmin = int(box[0] - box[2]/2)
            xmax = int(box[0] + box[2]/2) + 1
            ymax = int(box[1] + box[3]/2) + 1
            
            if (line[0] > xmin and line[0] < xmax or 
                line[1] > xmin and line[1] < xmax or 
                xmin > line[0] and xmin < line[1]):
                if ymax > line[2]:
                    flag = False
        
        # unaccessible object
        if flag == False:
            self.cmissed += 1
            old_claw = self.claw_pos
            self.claw_pos = (pos[0], self.res[1])
            self.pixel += abs(old_claw[0] - self.claw_pos[0])
            if self.verbose:
                self.vis()
            return False
            
        # attempt grab
        if self.objs[i].grab_attempt():
            self.grabbed += 1
            old_claw = self.claw_pos
            self.claw_pos = (pos[0], self.res[1])
            self.pixel += abs(old_claw[0] - self.claw_pos[0])
            old_claw = self.claw_pos
            self.claw_pos = self.bins[self.objs[i].get_box()[4]]
            self.pixel += abs(old_claw[0] - self.claw_pos[0])
            self.objs.pop(i)
            if self.verbose:
                self.vis()
            return True
        self.missed += 1
        old_claw = self.claw_pos
        self.claw_pos = (pos[0], self.res[1])
        self.pixel += abs(old_claw[0] - self.claw_pos[0])
        if self.verbose:
            self.vis()
        return False
    
    def dump(self):
        self.dumps += len(self.objs)
        self.objs.clear()
        if self.verbose:
            self.vis()
    
    def get_claw_pos(self):
        return (self.claw_pos[0], self.res[1])
    
    def get_objs(self):
        return [obj.get_box() for obj in self.objs]
    
    def analysis(self, l_miss=1, l_dumped=3, l_cmiss=10, l_move=1/1280):
        print(f'Iterations: {self.iter}')
        print('-'*40)
        print('Hyperparameters:')
        print(f'Item Miss: +{l_miss}')
        print(f'Item Lost: +{l_dumped}')
        print(f'Item Completely Missed: +{l_cmiss}')
        print(f'{int(l_move**-1)} Claw Movement: +1')
        print('-'*40)
        print(f'Items Spawned: {self.items}')
        print(f'Grabs Attempted: {self.grabs}')
        print(f'Items Grabbed: {self.grabbed}')
        print(f'Items Missed: {self.missed}')
        print(f'Items Completely Missed: {self.cmissed}')
        print(f'Items Dumped: {self.dumps}')
        print(f'Pixels Moved: {self.pixel}')
        print('-'*40)
        miss = l_miss * self.missed
        dumped = l_dumped * self.dumps
        cmiss = l_cmiss * self.cmissed
        pixel = l_move * self.pixel
        total = miss + dumped + cmiss + pixel
        avg = total/self.iter
        print(f'Average Cost: {avg}')
        
    def toggle_verbose(self):
        self.verbose = not self.verbose
        if self.verbose:
            self.vis()
        
    def vis(self):
        # claw position
        fig, ax = plt.subplots()
        img = [[[255 for _ in range(3)] for _ in range(640)] for _ in range(480)]
        
        # add boxes
        for box in self.get_objs():
            xmin = int(box[0] - box[2]/2)
            ymin = int(box[1] - box[3]/2)
            edgecolor = 'red' if box[4] == 0 else 'green'
            bb = patches.Rectangle((xmin, ymin), box[2], box[3], linewidth=2, 
                                   edgecolor=edgecolor, facecolor='none')
            ax.add_patch(bb)
        
        xc, yc = self.get_claw_pos()
        xmin = xc - 10
        
        bb = patches.Rectangle((xmin, yc), 20, 10, linewidth=10, 
                               edgecolor='blue', facecolor='none')
        ax.add_patch(bb)
        
        ax.imshow(img)
        plt.show()
        return

class trash():
    def __init__(self, res=(640, 480), ratio=0.5, prob=0.8, decay=0.8):
        self.prob = prob
        self.decay = decay
        
        self.frame_width, self.frame_height = res
        
        obj_max_width = res[0] * ratio
        obj_max_height = res[1] * ratio
        
        self.width = int(random.random()*obj_max_width)
        self.height = int(random.random()*obj_max_height)
        
        bounds_x = [int(self.width/2)+1, int(res[0]-self.width/2)-1]
        bounds_y = [int(self.height/2)+1, int(res[1]-self.height/2)-1]
        
        self.xc = random.randint(*bounds_x)
        self.yc = random.randint(*bounds_y)
        
        self.label = int(random.getrandbits(1))
        
    def get_box(self):
        return [self.xc, self.yc, self.width, self.height, self.label]

    def grab_attempt(self):
        if random.random() < self.prob:
            self.prob = 0
            return True
        else:
            self.prob = self.prob*self.decay
            return False

if __name__ == '__main__':
    main()
    