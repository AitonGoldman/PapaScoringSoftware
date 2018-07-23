source ./back/utils/ops/list_of_packages_to_install.sh
for i in ${LIST_OF_PACKAGES[@]}
do
    RESULT=`dpkg -s $i 2>1 >/tmp/out`
    if [ "$?" -ne "0" ]
    then
	echo "$i was not installed"
	exit 1
    fi    
done
