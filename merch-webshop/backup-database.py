from datetime import datetime
import os

src = "/srv/www/merch-webshop/website/database.db"
dst = "/srv/www/merch-webshop/database-backups/{}.db.bak".format(datetime.now().strftime('%d-%m-%Y-%H%M'))

os.system("cp {} {}".format(src, dst))
