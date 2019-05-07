from models.base_model import BaseModel
import peewee as pw


class ProductCategory(BaseModel):
    category_name = pw.CharField(unique=True)
   


