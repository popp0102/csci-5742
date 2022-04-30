export PATH=$PATH:~/.local/bin
pylint --load-plugins=cve_plugins.ban_arbitrary_execution_subprocess \
       --disable=all --enable=ban-arbitrary-execution-subprocess \
       tests/subprocess_test.py
