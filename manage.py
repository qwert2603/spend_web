#!./venv/bin/python3

from app import create_app, db
from app.utils import month_names

app = create_app('prod')


@app.shell_context_processor
def make_shell_context():
    return dict(db=db)


context_dict = dict(month_names=month_names)


@app.context_processor
def context_processor():
    return context_dict


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8362
    )
