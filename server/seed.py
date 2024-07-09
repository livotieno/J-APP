from models import User, db, Category, TokenBlocklist, Entry
from app import create_app
from datetime import datetime
from models import generate_uuid

app = create_app()


def seed_database():
    with app.app_context():
        User.query.delete()
        Entry.query.delete()
        Category.delete()



users = [{
             "id":"01",
            "username": "frowlett0",
            "password": "aG0)%",
            "created_at": "3/18/2023",
            "updated_at":"6/13/2023"
        }, {
            "id":"02",
            "username": "ibernaciak1",
            "password": "zZ9?y",
            "created_at": "4/15/2023",
            "update_at":"6/15/2023"

        }, {
            "id":"03",
            "username": "djosilowski2",
            "password": "qJ3)}h=",
            "created_at": "8/8/2023",
            "updated_at":"10/8/2022"

        }]

for user_data in users:
            user_data["created_at"] = datetime.strptime(
                user_data["created_at"], "%m/%d/%Y")
            user_data["id"] = generate_uuid()
            user = User(**user_data)
            db.session.add(user)
db.session.commit()
print("Users added!!!")
    

entry = [{
       "id":"00",
       "user_id":"a01",
       "title":"Travel",
       "content":"Travelling",
       "category":"Hillside",
       "craeted_at":"8/12/2023",
       "update_at":"15/12/2023"

       
       

},{
       "id":"01",
       "user_id":"a02",
       "title":"Playing",
       "content":"Football",
       "category":"Nationals",
       "created_at":"10/12/2023",
       "updated_at":"15/12/2023"
       
       
}]

for entry_data in entry:
            entry_data["created_at"] = datetime.strptime(
            entry_data["created_at"], "%m/%d/%Y")
            entry_data["id"] = generate_uuid()
            entry = Entry(**user_data)
            db.session.add(Entry)
db.session.commit()
print("Entry added!!!")



category = [{
        "id":"Personal",
        "name":"Travelling",
        "craeted_at":"8/12/2023",
       "update_at":"15/12/2023"

},{
        "id":"Personal",
        "name":"Cooking",
        "craeted_at":"8/12/2023",
       "update_at":"15/12/2023"

}]

for category_data in category:
            category_data["created_at"] = datetime.strptime(
            category_data["created_at"], "%m/%d/%Y")
            category_data["id"] = generate_uuid()
            category = Category(**user_data)
            db.session.add(Category)
db.session.commit()
print("Category added!!!")

    