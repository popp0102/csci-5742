export PATH=$PATH:~/.local/bin
pylint --load-plugins=cve_plugins.ban_empty_try_catch_blocks \
       --disable=all --enable=pass-only-used \
       tests/ban_empty_try_catch_blocks_test.py
