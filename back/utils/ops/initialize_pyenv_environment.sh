curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash
export PATH="~/.pyenv/bin:$PATH"
eval "$(~/.pyenv/bin/pyenv init -)"
eval "$(~/.pyenv/bin/pyenv virtualenv-init -)"
pyenv install 2.7.11
pyenv virtualenv 2.7.11 pss_venv
pyenv activate pss_venv
#pip install gunicorn
