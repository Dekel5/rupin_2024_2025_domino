import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from PIL import Image
import random
import os
import pandas as pd

# פונקציית החלוקה מתוך train_test_val_function.py
from functions.train_val_test.train_test_val_function import split_images_by_balanced_feature_no_test

# Augmentation מותאם אישית מתוך הפונקציות הקיימות
from functions.pre_processing.black_and_white import convert_to_black_and_white
from functions.pre_processing.blur_image import blur_image_randomly
from functions.pre_processing.brightness_image import change_brightness_randomly
from functions.pre_processing.rotate_image import rotate_image_randomly
from functions.pre_processing.sharpness_image import change_sharpness_randomly


def custom_augmentation(image):
    # רשימה של כל פונקציות האוגמנטציה
    augmentations = [
        lambda img: convert_to_black_and_white(img) if random.random() < 0.5 else img,
        lambda img: blur_image_randomly(img) if random.random() < 0.5 else img,
        lambda img: change_brightness_randomly(img, factor=random.uniform(0.5, 1.5)) if random.random() < 0.5 else img,
        lambda img: rotate_image_randomly(img, angle=random.randint(-15, 15)) if random.random() < 0.5 else img,
        lambda img: change_sharpness_randomly(img, factor=random.uniform(0.5, 2.0)) if random.random() < 0.5 else img,
    ]

    # החלת האוגמנטציות בלולאה
    for augment in augmentations:
        image = augment(image)

    return image


# הגדרת DataLoader מותאם אישית
class DominoDataset(Dataset):
    def __init__(self, image_paths, transform=None):
        self.image_paths = image_paths
        self.transform = transform

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        img_path = self.image_paths[idx]
        image = Image.open(img_path).convert("RGB")
        image = custom_augmentation(image)
        if self.transform:
            image = self.transform(image)
        label = self.get_label_from_path(img_path)
        return image, label

    def get_label_from_path(self, img_path):
        return random.randint(0, 1)  # לשינוי בהתאם לצורך


# קריאת נתונים מתוך קובץ האקסל והכנת הסטים
data_splits = split_images_by_balanced_feature_no_test("path/to/excel_file.xlsx")

# יצירת DataLoaders
train_dataset = DominoDataset(data_splits["train"])
val_dataset = DominoDataset(data_splits["validation"])

train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)


# הגדרת מודל CNN בסיסי
class CNNModel(nn.Module):
    def __init__(self):
        super(CNNModel, self).__init__()
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.fc1 = nn.Linear(64 * 8 * 8, 128)  # להתאים אם גודל התמונות שונה
        self.fc2 = nn.Linear(128, 2)  # להתאים למספר הקלאסים שלך
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.pool(self.relu(self.conv1(x)))
        x = self.pool(self.relu(self.conv2(x)))
        x = x.view(x.size(0), -1)  # Flatten
        x = self.relu(self.fc1(x))
        x = self.fc2(x)
        return x


# הגדרת אובייקטים לאימון
model = CNNModel()
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)


# פונקציית אימון
def train_model(num_epochs=10):
    for epoch in range(num_epochs):
        model.train()
        epoch_loss = 0
        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item()

        print(f"Epoch [{epoch + 1}/{num_epochs}], Loss: {epoch_loss:.4f}")
        save_real_image(images[0], epoch)


# פונקציה לשמירת תמונה לדוגמה (תמונה אחת מכל אפוק)
def save_real_image(image, epoch):
    image = image.cpu().permute(1, 2, 0).numpy()
    img = Image.fromarray((image * 255).astype('uint8'))
    img.save(f"real_image_epoch_{epoch + 1}.png")


# הפעלת האימון
train_model()
