import lab3_module
import dbUI

b = lab3_module.Book('carlos' , 'ola' , 2000)
b.print()

database = lab3_module.BookDB()
interface = dbUI.dbUI()
interface.run(database)
