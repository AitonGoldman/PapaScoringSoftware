FROM node
ADD . /td
RUN npm install ionic cordova gulp -g
WORKDIR /td
RUN npm install
ENTRYPOINT ionic serve -a 
