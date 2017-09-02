# Installing pre-reqs for backend

```
./back/utils/ops/install_packages.sh
./back/utils/ops/verify_install_packages.sh
./back/utils/ops/initialize_pyenv_environment.sh
./back/utils/ops/verify_initialize_pyenv_environment.sh
python ./setup.pyenv.py
```

# Create postgres user

```
sudo -u postgres createuser -s -P <database_username>
```

# Install pre-reqs for frontend

```
cd front
npm install
sudo npm install -g gulp-util
sudo npm install -g gulp-cli
sudo npm install -g cordova
sudo npm install -g ionic
node_modules/bower/bin/bower install
```

# Configure backend

The file `back/utils/ops/env_vars.template` contains all the environment variables that are required to be set by the backend.  Each variable is described in the file.  If you want to use the file to store the environment variables values on disk, copy the file `back/utils/ops/env_vars.template` to `back/utils/ops/env_vars`.  Please use the filename `env_vars`, as that file name is gitignored.

# Bootstrap database

Assuming you have set the variables in `back/utils/ops/env_vars`...
```
cd back
source ./utils/ops/env_vars
PYTHONPATH=. python ./utils/populate/create_db.py $pss_db_name
```

# Run backend 

```
cd back
source ./utils/ops/env_vars
PYTHONPATH=. ./utils/gunicorn.cmd 1
```

Note that the PSS will default to running on port 8000.


In a seperate window, run the following command 

```
curl -X POST http://0.0.0.0:8000/pss_admin/healthcheck
```

you should get back a json response.


# "Start" the frontend

You need to serve the frontend code with a http server.  Ionic provides a lightweight http server (that forces a reload of content on changes to any of the frontend files).  You can run it with these commands :

`cd front`
`ionic serve -a`

This will serve frontend pages/code over port 8100.  Goto the following url : 

`http://0.0.0.0:8100`


