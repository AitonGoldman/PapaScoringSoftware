VERSION=`pyenv version | grep -Eo pss_venv`
if [ "$VERSION" = "" ]
then
echo "Pyenv did not install correctly!  Please examine the output of the last command"
exit 1
fi

