pylint --load-plugins=cve_plugins.ban_create_os_subprocess \
       --disable=all --enable=subprocess-creation-is-banned \
       tests/os_system_test.py