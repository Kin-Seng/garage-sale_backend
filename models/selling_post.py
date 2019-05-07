from models.base_model import BaseModel
import peewee as pw
from models.product_category import ProductCategory
from models.users import Users

class SellingPost(BaseModel):
    # product_category = pw.ForeignKeyField(ProductCategory,backref="categories")
    # product_pic = pw.CharField()
    product_name = pw.CharField(unique=True)
    price = pw.DecimalField()
    seller = pw.ForeignKeyField(Users,backref="seller")
    buyer = pw.ForeignKeyField(Users,backref="buyer", null=True)
    pymt_sts = pw.BooleanField()





