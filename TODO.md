Bug queue and PRs will be open by December.  TODO list (shorter term ideas/priorities):

docs
* document all the new facts structure
* in content/ examples, break them up to show things are more programmable
* document should_process_when, pre, post on the roles class

facts:
* fix FileTests - now it is just a stub
* flesh out OS facts
* better error handling for /etc/opsmop/facts.d

core platform:
* show parameters per executed type
* if a basic list is passed in to any object like Resources() or returned from set_resources, auto-convert it to a collection.
* much better errors from template code - not full tracebacks
* better asserts if things like set_resources does not return a Resources(), ditto for set_roles
* validators.py should use common file test class
* fix (small bugs with) nested scopes in the variable system
* changed_when, failed_when
* make conditionals human readable in callbacks - show test & evaluated value


modules:
* split directory and file apart again
* finish out testing File module, Service:brew and Package:brew
* finish out package/service modules for main OSes
* Still allow some way for Set('') to also do global scope.  Maybe Global()
* add a 'sudo' parameter to shell which just does sudo -u
* when the Debug() module is called with no arguments it should show all variables in scope.
* make FileUtils a seperate class in common, simply file type/provider code lots
* Shell module should allow File's easy copy behavior to transfer scripts
* File should be able to fetch URLs
* Basic REST module
* user 
* group

testing:
* Baseline for unit test infrastructure, ideally with mocked providers.

generalized refactoring
* callbacks need to be cleaned up, which are not needed anymore?  Which can be simplified?
* consistently use underscore _vars for member data throughout
* cleanup field.py

code docs
* Apache2 license headers
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


