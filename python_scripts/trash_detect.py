from ultralytics import YOLO
import csv
import os

#create a model directory in models based on which pretrained yolo model you choose.
model_directory = "yolo11n"
# once training is finished, ultralytics will provide model on best performing epoch and last epoch, best.pt and last.pt
model_name = "best.pt"

model_path = os.path.join("models", model_directory, model_name)

model = YOLO(model_path)

# input image to run model on
image_path = os.path.join("input_images", "juicebox-kid.jpg")

# model runs on input image and saves to runs/detect/predict#
results = model.predict(image_path, save=True)
#results = model(image_path)
csv_path = "recycling_info.csv"

# loads disposal instructions (Ann Arbor regulations) for each trash label into dictionary
# TODO: CSV file is incomplete for some labels
def read_trash_csv(file_path):
    data_dict = {}

    with open(file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)  # Skip the header row if there is one
        
        for row in csv_reader:
            data_dict[row[0]] = row[1]
    
    return data_dict

# provides instructions based on model classification
def get_info(results, info_dict):
    predicted_classes = []
    for result in results:  
        if hasattr(result, 'boxes'):
            for box in result.boxes:
                class_id = int(box.cls)  
                class_name = result.names[class_id]  
                if class_name not in predicted_classes:
                    predicted_classes.append(class_name)

    #print("Predicted Classes:", predicted_classes)
    if not predicted_classes:
        print("\nNo item detected")

    for prediction in predicted_classes:
        if prediction in info_dict:
            print(f"\nType: {prediction} \nInstruction: {info_dict[prediction]}")
    

trash_dict = read_trash_csv(csv_path)
#print(trash_dict)
    
get_info(results, trash_dict)
