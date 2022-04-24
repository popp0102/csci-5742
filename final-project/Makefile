cwe1:
	PYTHONPATH=${PYTHONPATH}:./cve_plugins pylint --load-plugins=cwe1 --disable=all --enable=pass-only-used tests/cwe1_test.py
input-sanitization:
	PYTHONPATH=${PYTHONPATH}:./cve_plugins pylint --load-plugins=input_sanitization_check --disable=all --enable=input-sanitize-check tests/input_sanitization_test.py
file-read-sanitization:
	PYTHONPATH=${PYTHONPATH}:./cve_plugins pylint --load-plugins=file_reading_sanitization_check --disable=all --enable=file-reading-sanitize-check tests/file_reading_sanitization_test.py
cwe78:
	PYTHONPATH=${PYTHONPATH}:./cve_plugins pylint --load-plugins=ban_create_os_subprocess,ban_arbitrary_execution_subprocess \
                                              tests/from_os_system_test.py test/os_system_test.py tests/subprocess_test.py
