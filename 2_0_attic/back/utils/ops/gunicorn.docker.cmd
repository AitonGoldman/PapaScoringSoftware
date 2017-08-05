export PATH="/root/.pyenv/bin:$PATH"
eval "$(/root/.pyenv/bin/pyenv init -)"
eval "$(/root/.pyenv/bin/pyenv virtualenv-init -)"
pyenv activate tdvenv
python -m unittest tests.integration.test_route_meta_admin
gunicorn -b 0.0.0.0 app:App --log-file=- -w 1 --reload
