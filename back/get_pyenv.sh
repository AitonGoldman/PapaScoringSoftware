curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash
export PATH="/root/.pyenv/bin:$PATH"
eval "$(/root/.pyenv/bin/pyenv init -)"
eval "$(/root/.pyenv/bin/pyenv virtualenv-init -)"
pyenv install 2.7.11
pyenv virtualenv 2.7.11 tdvenv
pyenv activate tdvenv
pip install gunicorn
cd /td
python setup.pyenv.py
