import random

import torch
from torchvision import transforms

class Augmentation(): # based on SSD
    def __init__(self, 
                 flip=False, 
                 expand=False, 
                 crop=False, 
                 resize=False, 
                 brightness=False, 
                 contrast=False, 
                 saturation=False, 
                 hue=False, 
                 normalize=False):

        '''
        if User Value
        elif Default
        else Disabled
        '''
        self.mean = [0.5, 0.5, 0.5] # [-1, 1]
        self.std = [0.5, 0.5, 0.5]

        # flip probability
        if flip and isinstance(flip, float):
            self.flip = flip
        elif flip:
            self.flip = 0.5
        else:
            self.flip = False

        # expand ratio
        if expand and isinstance(expand, (int, float)) and not isinstance(expand, bool): # bool is a subclass of int
            self.expand = expand
        elif expand:
            self.expand = 4
        else:
            self.expand = False
        
        # crop overlaps
        if crop and isinstance(crop, list):
            self.crop = crop
        elif crop:
            self.crop = [0, 0.1, 0.3, 0.5, 0.7, 0.9, None]
        else:
            self.crop = False

        # resize resolution
        if resize and isinstance(resize, (list, tuple)):
            self.resize = resize
        elif resize:
            self.resize = (224, 224)
        else:
            self.resize = False

        # brightness value
        if brightness and isinstance(brightness, float):
            self.brightness = brightness
        elif brightness:
            self.brightness = 0.1
        else:
            self.brightness = 0

        # contrast value
        if contrast and isinstance(contrast, float):
            self.contrast = contrast
        elif contrast:
            self.contrast = 0.1
        else:
            self.contrast = 0

        # saturation value
        if saturation and isinstance(saturation, float):
            self.saturation = saturation
        elif saturation:
            self.saturation = 0.2
        else:
            self.saturation = 0

        # hue value
        if hue and isinstance(hue, float):
            self.hue = hue
        elif hue:
            self.hue = 0.2
        else:
            self.hue = 0
        
        # mean and std
        if normalize and isinstance(normalize, (list, tuple)):
            self.normalize = normalize
        elif normalize:
            self.normalize = (self.mean, self.std)
        else:
            self.normalize = False

    def __call__(self, image, boxes=None):
        image = torch.from_numpy(image).permute(2, 0, 1).type(torch.FloatTensor) # np uint8: hwc -> float tensor: chw
        image /= 255 # pre-normalize

        # geometric transforms
        if self.flip and self.flip > random.random():
            image, boxes = __class__.flip_fn(image, boxes)
        if self.expand and 0.5 > random.random():
            image, boxes = __class__.expand_fn(image, boxes, self.expand)
        if self.crop:
            image, boxes = __class__.crop_fn(image, boxes, self.crop)
        if self.resize:
            image, boxes = __class__.resize_fn(image, boxes, self.resize)

        # photometric transforms
        if self.brightness or self.contrast or self.saturation or self.hue:
            color_jitterer = transforms.ColorJitter(self.brightness, self.contrast, self.saturation, self.hue)
            image = color_jitterer(image)
        if self.normalize:
            image = transforms.functional.normalize(image, *self.normalize)
        
        # no boxes
        if boxes is None:
            return image
        
        return image, boxes
    
    @staticmethod
    def resize_fn(image, boxes, resolution=(224, 224)):
        # 1. Extract Info
        old_height, old_width = image.shape[1:]
        new_height, new_width = resolution

        # 2. No Boxes
        if boxes is None:
            return transforms.functional.resize(image, resolution), None

        # 3. Find Scaling Factor
        height_scale = new_height/old_height
        width_scale = new_width/old_width
        scaler = torch.tensor([width_scale, height_scale, width_scale, height_scale, 1]).unsqueeze(0)

        # 4. Resize Image and Scale Boxes
        return transforms.functional.resize(image, resolution), boxes * scaler
    
    @staticmethod
    def flip_fn(image, boxes):
        # 1. Extract Info
        width = image.shape[2]
        new_boxes = boxes.clone()

        # 2. No Boxes
        if boxes is None:
            return transforms.functional.hflip(image), None
        
        # 3. Flip Boxes
        new_boxes[:, 0] = width - boxes[:, 2]
        new_boxes[:, 2] = width - boxes[:, 0]

        # 3. Flip Image
        return transforms.functional.hflip(image), new_boxes
    
    @staticmethod
    def expand_fn(image, boxes, scale=4):
        # 1. Extract Info
        filler = torch.tensor([0.5, 0.5, 0.5])
        old_height, old_width = image.shape[1:]

        # 2. Create Filler Image
        scale = random.uniform(1, scale)
        new_height, new_width = int(scale*old_height), int(scale*old_width)
        new_image = torch.ones((3, new_height, new_width)) * filler.unsqueeze(1).unsqueeze(1)

        # 3. No Boxes
        if boxes is None:
            return new_image, None

        # 4. Insert Image
        left = random.randint(0, new_width - old_width)
        right = left + old_width
        top = random.randint(0, new_height - old_height)
        bottom = top + old_height
        new_image[:, top:bottom, left:right] = image

        # 5. Offset Boxes
        return new_image, boxes + torch.tensor([left, top, left, top, 0]).unsqueeze(0)

    @staticmethod
    def crop_fn(image, boxes, overlaps=[0, 0.1, 0.3, 0.5, 0.7, 0.9, None]):
        # 1. Extract Info
        old_height, old_width = image.shape[1:]

        while True: # try overlap samples
            # 1. Extract Info
            overlap = random.choice(overlaps)

            if overlap is None: # no crop
                return image, boxes

            for _ in range(50): # try 50 crops

                # 2. Candidate Scale
                scale = 0.3
                new_height = int(random.uniform(scale, 1)*old_height)
                new_width = int(random.uniform(scale, 1)*old_width)

                min_ar, max_ar = 0.5, 2
                if not min_ar < new_height/new_width < max_ar: # check aspect ratio
                    continue
                
                # 3. Candidate Crop
                left = random.randint(0, old_width - new_width) 
                right = left + new_width
                top = random.randint(0, old_height - new_height)
                bottom = top + new_height
                crop = torch.tensor([left, top, right, bottom])

                # 4. No Boxes
                if boxes is None:
                    return image[:, top:bottom, left:right], None

                jaccard_overlap = __class__.compute_jaccard_overlap(crop, boxes)
                if jaccard_overlap.max().item() < overlap: # check jaccard overlap
                    continue

                # 5. Compute Masks
                centers = (boxes[:, :2] + boxes[:, 2:4]) / 2
                mask = (left < centers[:, 0]) * (centers[:, 0] < right) * (top < centers[:, 1]) * (centers[:, 1] < bottom)
                
                if not mask.any(): # check mask
                    continue

                # 6. Filter Boxes
                boxes = boxes[mask, :]

                # 7. Offset Remaining Boxes
                boxes[:, :2] = torch.max(boxes[:, :2], crop[:2]) - crop[:2]
                boxes[:, 2:4] = torch.min(boxes[:, 2:4], crop[2:]) - crop[:2]

                # 8. Crop Image
                return image[:, top:bottom, left:right], boxes

    @staticmethod
    def compute_jaccard_overlap(crop, boxes):
        '''
        crop: dim(4); 4 = [left, top, right, bottom]
        boxes: dim(N, 5); 5 = [xmin, ymin, xmax, ymax, class]
        where N is the number of boxes
        ''' 
        # intersection
        tl = torch.max(crop[:2].unsqueeze(0), boxes[:, :2]) # N x 2
        br = torch.min(crop[2:].unsqueeze(0), boxes[:, 2:4])
        wh = torch.clamp(br - tl, 0)
        intersection = wh[:, 0] * wh[:, 1] # N

        # union
        area_crop = (crop[2] - crop[0])*(crop[3] - crop[1]) # scaler
        area_boxes = (boxes[:, 2] - boxes[:, 0])*(boxes[:, 3] - boxes[:, 1]) # N
        union = area_crop + area_boxes - intersection

        # iou
        return intersection / union
