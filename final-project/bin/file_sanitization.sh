export PATH=$PATH:~/.local/bin
pylint --load-plugins=cve_plugins.file_reading_sanitization_check \
       --disable=all --enable=file-reading-sanitize-check \
       tests/file_reading_sanitization_test.py
