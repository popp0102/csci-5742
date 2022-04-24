cwe1:
	PYTHONPATH=${PYTHONPATH}:./cve_plugins pylint --load-plugins=cwe1 --disable=all --enable=pass-only-used tests/cwe1_test.py
cwe78:
	PYTHONPATH=${PYTHONPATH}:./cve_plugins pylint --load-plugins=ban_create_os_subprocess,ban_arbitrary_execution_subprocess \
                                              tests/from_os_system_test.py test/os_system_test.py tests/subprocess_test.py
