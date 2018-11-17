Bug queue and PRs will be open by December.  TODO list (shorter term ideas/priorities):

docs generator
* module docs generator / docs

facts:
* flesh out OS facts
* site facts (/etc/opsmop/facts.d). In opsmop facts are functions so this is easy.

core platform:
* rename 'method' to 'provider' in the language
* much better errors from template code - not full tracebacks
* better asserts if things like set_resources does not return a Resources(), ditto for set_roles
* add 'with' - takes a real variable or an Eval()
* rename 'register' to 'save'
* allow 'save' to take a 'save_value=Eval()'
* validators.py should use common file test class
* fix (small bugs with) nested scopes in the variable system
* changed_when, failed_when
* make conditionals human readable in callbacks - show test & evaluated value
* when traversing parents with child objects, evaluate the condition on the parent before returning the children (Visitor.py) - eliminate the condition_stack code 
  this may cause some minor problems when the condition on the child object depends on a set variable, so we should always return the children in *CHECK* mode
  traversal and filter them in *APPLY* mode traversal.  This means the visitor needs to understand check vs apply.

modules:
* Still allow some way for Set('') to also do global scope.  Maybe Global()
* add a 'sudo' parameter to shell which just does sudo -u
* when the Debug() module is called with no arguments it should show all variables in scope.
* finish out testing File module, Service:brew and Package:brew
* finish out package/service modules for main OSes
* make FileUtils a seperate class in common, simply file type/provider code lots
* Shell module should allow File's easy copy behavior to transfer scripts
* File should be able to fetch URLs
* Basic REST module

testing:
* Baseline for unit test infrastructure, ideally with mocked providers.

generalized refactoring
* consistently use underscore _vars for member data throughout
* more of __slots__ throughout
* cleanup field.py
* eliminate filetest.py / overhaul file module
* cleanup executor.py some
* cleanup the visitor and scope code, which is a little self-referential in resource.py

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


