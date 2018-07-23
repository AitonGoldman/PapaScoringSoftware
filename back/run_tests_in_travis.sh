export db_type='postgres'
export db_username='postgres'
export db_password='fakepassword'
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PYTHONPATH=$DIR python -m unittest discover -s $DIR/test/unit -f
PYTHONPATH=$DIR python -m unittest discover -s $DIR/test/integration -f
