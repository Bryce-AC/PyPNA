import PyPNA

pm = PyPNA.PyPNA()

pm.connect()

pm.load_setup('D:/harrys_setup.csa')

pm.print_id()
