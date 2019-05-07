from models.base_model import BaseModel
import peewee as pw


class Users(BaseModel):
    username = pw.CharField(unique=True,null=False)
    pwd = pw.CharField(null=False)
    profile_pic = pw.CharField(unique=True,null=True)
    age = pw.IntegerField(null=True)
    email = pw.CharField(unique=True,null=False)
    address = pw.CharField(null=True)
    phone_no = pw.CharField(null=True)


