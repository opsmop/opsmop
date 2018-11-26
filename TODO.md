Bug queue and PRs will be open by December.  TODO list (shorter term ideas/priorities):

core platform:
* if a resource is just a string, infer that it is an Echo resource
* which using the Echo resource, switch off all output but the Echo
* the TOML bundle idea from the forum
* show parameters per executed type in CLI output
* add a common 'comment' parameter to each resource, show name+comment first when showing details
* if a basic list is passed in to any object like Resources() or returned from set_resources, auto-convert it to a collection.
* much better errors from template code - not full tracebacks
* better asserts if things like set_resources does not return a Resources(), ditto for set_roles
* validators.py should use common file test class
* fix (small bugs with) nested scopes in the variable system
* implement changed_when, failed_when
* when actions taken != actions planned, show both lists
* reinstate the resource counters - how many resources added/changed/etc

modules:
* Still allow some way for Set('') to also do global scope.  Maybe Global()
* add a 'sudo' parameter to shell which just does sudo -u
* Shell module should allow File's easy copy behavior to transfer scripts
* File should be able to fetch URLs
* Basic REST module
* user and group modules
* switch apt implementation to use apt-get because apt is very noisy, or otherwise make it quieter
* say module for OS X speech synthesis just because it is fun

testing:
* Baseline for unit test infrastructure, ideally with mocked providers.

code docs
* review and update all comments

opsmop-pull - simple implementation
* opsmop-pull [daemon|once] pull_cfg.py
* defines TRANSPORT=Transport(), CLI_STATUS_CALLBACKS=[ CliStatusCallback() ], PULL_STATUS_CALLBACKS=[ PullStatusCallback1(), ... ]
* asks transports.is_there_content()
* calls transport.download_content() -> returns (temp_dir, filename)
* uses opsmop.core.api with CLI_STATUS_CALLBACKS
* calls each .report_status in PULL_STATUS_CALLBACKS
* calls transport.sleep(), loops if called with 'daemon' mode.
* initial version comes with GitTransport(repo_url=<>) and recommended use is with ssh-agent to deal with checkout keys

opsmop-push:
* implementation ideas TBD

others:
* Cool ideas everyone comes up with
* Merging stuff
* SPOILERS!


