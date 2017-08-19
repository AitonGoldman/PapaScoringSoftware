#rm /tmp/test_db*
export db_type='sqlite'
export db_username='fakeusername'
export db_password='fakepassword'
export db_name='test_db'
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PYTHONPATH=$DIR python -m unittest discover -s $DIR/test/unit -f
PYTHONPATH=$DIR python -m unittest discover -s $DIR/test/integration -f
