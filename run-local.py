#!/usr/bin/env python
from py_bife import create_app, db

app = create_app()
print(f"Path root \n-->> {app.root_path}")
with app.app_context():
    from py_bife.model.user import User

    db.drop_all()
    db.create_all()
if __name__ == "__main__":
    app.run()
