set -e
source ./back/utils/ops/list_of_packages_to_install.sh
apt-get update
for i in ${LIST_OF_PACKAGES[@]}
do
    apt-get --allow-downgrades --force-yes install $i    
done

