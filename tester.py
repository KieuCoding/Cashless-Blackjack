#from dataset import PascalVoc
import torch, cv2, json, numpy
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from model import YoYo
from augmentations import Augmentation
from utils import decoder, NMS

class Tester:
    def load(self, checkpoints, model):
        # 1. load Chechpoint/YoYo model
        checkpoint = torch.load(checkpoints, map_location='cpu')
        model.load_state_dict(checkpoint)
        return model
    

    def live(self, source, model):
        cap = cv2.VideoCapture(source)
        transform = Augmentation(
            resize=(224, 224), 
            normalize=True
        )
        while cap.isOpened():
            ret, cam = cap.read()
            if not ret:
                exit()
            cam = cv2.cvtColor(cam, cv2.COLOR_BGR2RGB)
            input = transform(cam).unsqueeze(0)
            cam = cv2.resize(cam, (224, 224))
            pred = model(input)
            pred = pred.squeeze()
            bboxes, scores, classes = decoder(pred, 0.2)
            bboxes, scores, classes = NMS(bboxes, scores, classes)
            bboxes, scores, classes = bboxes.numpy(), scores.numpy(), classes.numpy()
            for j, box in enumerate(bboxes):
                box = [int(x) for x in box]
                cv2.rectangle(cam, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)
                cv2.putText(cam, f'{classes[j]}:{scores[j]: .2f}', (box[0], box[1] - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0))
                print(classes[j])
                print(scores[j])
            cv2.imshow("Live Detection", cam)

    
    def picture(self, pic_set, model):
        # 1. take in user's picture set
        pic_files = pic_set
        pic_files = ['pictures/'+pic for pic in pic_files]
        dataset =  PascalVoc('train')

        # 2. augment, resize, and normalize images
        transform = Augmentation(
            resize=True, 
            normalize=True
        )

        # 3. Reformat image , decode and NMS images' bboxes 
        fig, ax = plt.subplots(1, 4)
        mng = plt.get_current_fig_manager()
        mng.resize(800, 800)
        for i, pic in enumerate(pic_files):
            img = cv2.imread(pic)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            input = transform(img).unsqueeze(0)
            img = cv2.resize(img, (224,224))
            pred = model(input)
            pred = pred.squeeze()
            bboxes, scores, classes = decoder(pred, 0.2)
            fig.suptitle('Single Image Detection')
            bboxes, scores, classes = NMS(bboxes, scores, classes)

            # 4. format and show images with bboxes on matplotlib
            for j, box in enumerate(bboxes):
                box = [int(value) for value in box]
                width, height = box[2] - box[0], box[3] - box[1]
                bbox = patches.Rectangle((box[0], box[1]), width, height, linewidth=2, edgecolor='g', facecolor='none')
                ax[i].add_patch(bbox)
                ax[i].text(box[0], box[1]-30, f'{dataset.classes[classes[j]]}:{scores[j]: .2f}', fontsize=10, color='red')
                ax[i].axis('off')
                ax[i].imshow(img)      
        plt.show()
    
    def loss(self, metrics):
        # 1. load metric JSON
        with open(metrics) as file:
            history = json.load(file)

        # 2. plot out validation and training loss 
        plt.figure(figsize=(6, 6))
        plt.plot(history['train loss'], label='Training Loss', color ="blue")
        plt.plot(history['val loss'], label = 'Validation Loss', color="red")
        plt.title('Loss Plot')
        plt.xlabel('Epochs')
        plt.ylabel('Loss')
        plt.legend()
        plt.show()
    
    def accuracy(self, metrics):
        # 1. load metric JSON
        with open(metrics) as file:
            history = json.load(file)

        # 2. plot out validation and training accuracy
        plt.figure(figsize=(6, 6))
        plt.plot(history['train accuracy'], label='Train Accuracy', color ="blue")
        plt.plot(history['val accuracy'], label = 'Validation Accuracy', color="red")
        plt.title('Accuracy Plot')
        plt.xlabel('Epochs')
        plt.ylabel('mAP50')
        plt.legend()
        plt.show()

def main():
    agent = Tester()
    model = agent.load('best.pth', YoYo(num_classes=4))
    agent.live(0, model)
    #agent.picture(['bus.jpg','hero.webp','motorbike.jpg','bike.jpg'], model)
    #agent.loss('checkpoints/history')
    #agent.accuracy('checkpoints/history')


if __name__ == '__main__':
    main()