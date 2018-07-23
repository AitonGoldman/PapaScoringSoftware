# Installing pre-reqs for backend

```
./back/utils/ops/install_packages.sh
./back/utils/ops/initialize_pyenv_environment.sh
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

# Configure frontend

There are two files that need to be created in the `front/www/js/app` directory (each has a .template file you can use):

`config.js`
`secret_info.js`
`events.json`

You will need to fill in the `events.json` and the `config.js` file.  See the `events.json.template` and `config.js.template` file for details on this.  You don't need to fill in secret_info.js.  

# Run backend 

```
cd back
source ./utils/ops/env_vars
PYTHONPATH=. ./utils/gunicorn.cmd 1
```

# Create database 

Each pinball event (i.e. "PAPA 20" vs "PPO 6") has it's own database.  A endpoint is provided that will create a test database. To use the endpoint, run the following : 

```
curl -X POST http://0.0.0.0:8000/meta_admin/db
```

# "Start" the frontend

You need to serve the frontend code with a http server.  Ionic provides a lightweight http server (that forces a reload of content on changes to any of the frontend files).  You can run it with these commands :

`cd front`
`ionic serve -a`

This will serve frontend pages/code over port 8100.  Goto the following url : 

`http://0.0.0.0:8100`


