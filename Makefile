venvdir := venv

#all: clean create_venv jupyter_spellcheck
all: clean create_venv
	@echo "Done"

create_venv: ${venvdir}

${venvdir}: requirements.txt
	test -d ${venvdir} || python3 -m venv ${venvdir}
	${venvdir}/bin/pip install  --upgrade pip
	${venvdir}/bin/pip install setuptools wheel
	${venvdir}/bin/pip install  -Ur requirements.txt
	echo "source ${venvdir}/bin/activate" > source_me.sh
	echo "module load cadence-flow/mixed-signal/2020-21" >> source_me.sh
	echo "export PYTHONPATH=`readlink -f src/`" >> source_me.sh

# jupyter_spellcheck: venv
# 	${venvdir}/bin/jupyter contrib nbextension install --user
# 	${venvdir}/bin/jupyter nbextension enable spellchecker/main

# Clean Python and Emacs backup and cache files
clean:
	find . -name '*.pyc' -delete
	find . -name '*.yaml' -delete
	find . -name '*~' -delete
	find . -name '__pycache__' -type d | xargs rm -rf
	find . -name '.ipynb_checkpoints' -type d | xargs rm -rf
	find . -name '${venvdir}' -type d | xargs rm -rf
	find . -name 'source_me.sh' -delete
	find . -name 'nosetest_results.txt' -delete

# Perform automatic test on the Python after buiduing it
nosetest_results.txt: ${venvdir} test test/*
	. ${venvdir}/bin/activate && nosetests -s > $@  2>&1 || rm -f $@

#.PHONY: all create_venv clean jupyter_spellcheck
.PHONY: all create_venv clean
