import pandas as pd

def split_images_by_balanced_feature_no_test(excel_path: str):
    """
    מחלקת תמונות לסטים (אימון ואימות) כך שסך הנקודות (sum_up_feature) בכל קבוצה יהיה שווה ככל הניתן,
    מבלי לחלק תמונות לסט מבחן (0 תמונות בסט המבחן).

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

    # סך הנקודות בכל קבוצה
    train_sum = 0
    val_sum = 0

    # חלוקה לתוך הקבוצות כך שסכום הנקודות יתאזן
    for _, row in df.iterrows():
        if train_sum <= val_sum:
            train_images.append(row['image_name'])
            train_sum += row['sum_up_feature']
        else:
            val_images.append(row['image_name'])
            val_sum += row['sum_up_feature']

    # החזרת המידע כמילון (אין סט מבחן)
    return {
        "train": train_images,
        "validation": val_images,
        "test": []  # אין תמונות בסט המבחן
    }
