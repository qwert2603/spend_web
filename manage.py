#!./venv/bin/python3

from app import create_app, db

app = create_app('dev')


@app.shell_context_processor
def make_shell_context():
    return dict(db=db)


context_dict = dict()


@app.context_processor
def context_processor():
    return context_dict


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8353
    )
