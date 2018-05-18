test: lint

develop:
	@echo "--> Installing dependencies"
	pip install -r requirements.txt
	@echo ""

clean:
	@echo "--> Cleaning pyc files"
	find . -name "*.pyc" -delete
	@echo ""

lint:
	@echo "--> Linting Python files"
	PYFLAKES_NODOCTEST=1 flake8 codecommit_slack
	@echo ""

publish:
	rm -rf ./publish/codecommit_slack/
	mkdir -p ./publish/codecommit_slack
	cp -r ./codecommit_slack ./publish/codecommit_slack/
	mv ./publish/codecommit_slack/codecommit_slack/aws_lambda/* ./publish/codecommit_slack/
	cp -r ./aws_lambda_libs/. ./publish/codecommit_slack/
	cd ./publish/codecommit_slack && zip -r ../codecommit_slack.zip .

compile:
	yum install -y gcc libffi-devel openssl-devel python27-virtualenv
	virtualenv /tmp/venv
	/tmp/venv/bin/pip install --upgrade pip setuptools
	/tmp/venv/bin/pip install -e .
	cp -r /tmp/venv/lib/python2.7/site-packages/. ./aws_lambda_libs
	cp -r /tmp/venv/lib64/python2.7/site-packages/. ./aws_lambda_libs

lambda-deps:
	@echo "--> Compiling lambda dependencies"
	docker run --rm -it -v ${CURDIR}:/src -w /src amazonlinux make compile

.PHONY: develop clean lint publish
