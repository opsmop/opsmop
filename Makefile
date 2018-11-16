requirements:
	pip install -r requirements.txt --trusted-host pypi.org --trusted-host files.pypi.org --trusted-host files.pythonhosted.org

venv:
	virtualenv env -p /usr/local/bin/python3

html:
	PYTHONPATH=. python3 -m opsmop.meta.docs.cli ../opsmop-demo/module_docs docs/source/modules
#	(rm -rf docs/build/html)
#	(rm -rf docs/build/doctrees)
#	(cd docs; make html)

# docs_publish:
# 	# cp -a docs/build/html/* ../opsmops-docs.github.io/

indent_check:
	pep8 --select E111 opsmop/

pyflakes:
	pyflakes opsmop/

clean:
	find . -name '*.pyc' | xargs rm -r
	find . -name '__pycache__' | xargs rm -rf

todo:
	grep TODO -rn vespene

bug:
	grep BUG -rn vespene

fixme:
	grep FIXME -rn vespene

gource:
	gource -s .06 -1280x720 --auto-skip-seconds .1 --hide mouse,progress,filenames --key --multi-sampling --stop-at-end --file-idle-time 0 --max-files 0  --background-colour 000000 --font-size 22 --title "OpsMop" --output-ppm-stream - --output-framerate 30 | avconv -y -r 30 -f image2pipe -vcodec ppm -i - -b 65536K movie.mp4

