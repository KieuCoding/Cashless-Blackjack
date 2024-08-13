import torch, torchvision
#from dataset import PascalVoc
from torchmetrics.detection import MeanAveragePrecision

# 1. resolution, grid length
res, S = 224, 7            

# 2. ground truth, prediction
gt = torch.rand(16, 7, 7, 9)                                                        
pred = torch.rand(16, 7, 7, 9)                                                      

def decoder(label, threshold=0.1): 
    # 1. Initialize pixel reolution and bbox properties                                       
    Pixelcell = res/S                                                           
    bboxes, scores, classes = [], [], []                                        
    
    # 2. [xc, xy, w, h, clas] to [xmin, ymin, xmax, ymax, clas]
    for i in range(S):                                                        
        for j in range(S):                                                     
            if label[i][j][4] >= threshold:                   
                w, h = label[i][j][2] * res, label[i][j][3] * res                                                  
                x1 = int((label[i][j][0] + j)*Pixelcell - w/2)                     
                y1 = int((label[i][j][1] + i)*Pixelcell - h/2)                     
                x2 = int((label[i][j][0] + j)*Pixelcell + w/2)                     
                y2 = int((label[i][j][1] + i)*Pixelcell + h/2)

                # 3. Find highest class in classes                
                clas = int(torch.argmax(label[i][j][5:]))

                # 4. Gather decoded XYXY bboxes, classes, and scores                      
                classes.append(clas)                                              
                bboxes.append([x1, y1, x2, y2])                                 
                scores.append(label[i][j][4]*label[i][j][5+clas])

    # 5. return them as a tensor                                                          
    return torch.Tensor(bboxes), torch.Tensor(scores), torch.tensor(classes)   

def NMS(bboxes, scores, classes, threshold=0.5):
    # 1. check for no  bboxes
    if bboxes.nelement() == 0:
        return bboxes, scores, classes
    
    # 2. Else Perform Non Max Suppression
    idx = torchvision.ops.nms(bboxes, scores, threshold)
    return bboxes[idx], scores[idx], classes[idx]                               

def mAP(preds, gts):
    # 1. initiate MAP class
    metric = MeanAveragePrecision()                                                   
    gtList, pred_list = [], []        

    # 2. decode/NMS Ground Truth and Predictions                                                
    for gt, pred in zip(gts, preds):                                                  
        gtBox, _, gtClass = decoder(gt)                                                                   
        pred_box, pred_score, pred_classes = decoder(pred)                            
        pred_box, pred_score, pred_classes = NMS(pred_box, pred_score, pred_classes)

        # 3. Dictionary for Ground Truth and Predictions   
        pred_list.append({                                                            
            'boxes': pred_box,
            'scores': pred_score,
            'labels': pred_classes,
        })
        gtList.append({                                                         
            'boxes': gtBox,
            'labels': gtClass
        })
    
    # 4. update MAP and return map_50
    metric.update(pred_list, gtList)                                            
    return metric.compute()['map_50'].item()
    
def main():
    # testing mAP function
    print(mAP(pred, gt))       

if __name__ == '__main__':
    main()
