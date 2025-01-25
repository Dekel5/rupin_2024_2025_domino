import pandas as pd

def split_images_by_balanced_feature(excel_path: str):
    """
    מחלקת תמונות לסטים (אימון, אימות, מבחן) כך שסך הנקודות (sum_up_feature) בכל קבוצה יהיה שווה ככל הניתן.

    :param excel_path: str - הנתיב לקובץ האקסל שמכיל את הפיצ'רים לחלוקה.
    :return: dict - מילון שמכיל רשימות של שמות תמונות לכל סט.
    """
    # קריאת קובץ האקסל
    df = pd.read_excel(excel_path, sheet_name='data')

    # מיון התמונות לפי ערך sum_up_feature
    df = df.sort_values(by='sum_up_feature', ascending=False)

    # רשימות לאחסון שמות התמונות בכל קבוצה
    train_images = []
    val_images = []
    test_images = []

    # סך הנקודות בכל קבוצה
    train_sum = 0
    val_sum = 0
    test_sum = 0

    # חלוקה לתוך הקבוצות כך שסכום הנקודות יתאזן
    for _, row in df.iterrows():
        if train_sum <= val_sum and train_sum <= test_sum:
            train_images.append(row['image_name'])
            train_sum += row['sum_up_feature']
        elif val_sum <= train_sum and val_sum <= test_sum:
            val_images.append(row['image_name'])
            val_sum += row['sum_up_feature']
        else:
            test_images.append(row['image_name'])
            test_sum += row['sum_up_feature']

    # החזרת המידע כמילון
    return {
        "train": train_images,
        "validation": val_images,
        "test": test_images
    }
