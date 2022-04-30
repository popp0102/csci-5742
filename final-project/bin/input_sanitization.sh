pylint --load-plugins=cve_plugins.input_sanitization_check \
       --disable=all --enable=input-sanitize-check \
       tests/input_sanitization_test.py