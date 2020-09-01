import json
import pandas as pd

class Item:

    def __init__(self, type: str, count:int):
        self.type = type
        self.count = count
        self.count_needed = count
        self.fullfilled = False

    def check_fullfilled(self):
        if self.count_needed <= 0:
            self.fullfilled = True





class Order:

    def __init__(self, items: list):

        self.order_items = items
        self.fullfilled = False

    def check_fullfilled(self):
        self.fullfilled = all(item.fullfilled == True for item in self.order_items)



class Warehouse:

    def __init__(self, name: str, inventory: dict):
        self.name = name
        self.inventory = inventory
        self.inventorydf : pd.DataFrame
        self.order = Order([])
        self.make_inventory()


    def make_inventory(self):
        df = pd.DataFrame.from_dict(self.inventory, orient='index', columns=['count'])
        self.inventorydf = df

    def check_inventory(self,item,count):
        if item in self.inventorydf.index:

            return True, self.name, self.inventorydf.at[item, "count"]
        else:
            return False

    def fill_item(self,item: Item):
        to_fullfill = min(item.count_needed,self.inventorydf.at[item.type, "count"])

        item.count_needed -=  self.inventorydf.at[item.type, "count"]

        self.order.order_items.append((item, to_fullfill))


        item.check_fullfilled()



class InventoryAllocator:



    def __init__(self, order:dict, warehouses:list):


        '''
        :param order: dictionary of order
        example { "apple": 5, "banana": 5, "orange": 5 }
        :param warehouses: warehouses and inventory
        example: [ { "name": "owd", "inventory": { "apple": 5, "orange": 10 } }, { "name": "dm", "inventory": { "banana": 5, "orange": 10 } } ]
        '''
        items = []
        for order_item in order.items():
            items.append(Item(order_item[0],order_item[1]))
        self.order = Order(items)

        self.warehouses = []

        self.fullfillment_paradigm = {}



        for warehouse in warehouses:

            self.warehouses.append(Warehouse(warehouse['name'],warehouse["inventory"]))





    def make_order(self):
        for item in self.order.order_items:
            for warehouse in self.warehouses:

                if item.fullfilled == False:
                    inventory_check = warehouse.check_inventory(item.type, item.count_needed)
                    if inventory_check is not False:
                            #print(item.count_needed)
                            warehouse.fill_item(item)
                       # print(inventory_check, item.type)



        for warehouse in self.warehouses:
            for fullfilled_item in warehouse.order.order_items:
                print(warehouse.name,fullfilled_item[0].type, fullfilled_item[1])
        self.order.check_fullfilled()

        if self.order.fullfilled == True:
            print("Fullfilled!!")
        else:
            print("Not enough Inventory")
        return


test = InventoryAllocator({ "apple": 5, "banana": 5, "orange": 20 },[ { "name": "owd", "inventory": { "apple": 5, "orange": 10 } }, { "name": "dm", "inventory": { "banana": 5, "orange": 10 } } ])
test.make_order()