STATUS: Still being refactored/upgraded to establish a strong baseline for future additions.
Bug queue and PRs will be open by December.

TODO list (shorter term ideas):

* -----
* DOCS!
* ----
* add a generic "changed_when" and an implicit register to a variable called "last" to make it easy to use
* when traversing parents with child objects, evaluate the condition on the parent before returning the children (Visitor.py) - eliminate the condition_stack code 
  this may cause some minor problems when the condition on the child object depends on a set variable, so we should always return the children in *CHECK* mode
  traversal and filter them in *APPLY* mode traversal.  This means the visitor needs to understand check vs apply.
* overhaul comments and audit fixmes
* cleanup field.py
* eliminate filetest.py / overhaul file module
* validators.py should use common file test class
* cleanup executor.py
* fix nested scopes in the variable system
* Apache2 license headers
* cleanup the visitor and scope code, which is a little self-referential in resource.py
* on j2 template errors, have much nicer error info (not a traceback)
* Still allow some way for Set('') to also do global scope.  Maybe Global()
* CLI should use ArgumentParser to have --options
* continued callback code improvement
* make FileUtils a seperate class in common, simply file type/provider code lots
* implement yum and apt for Package
* implement systemd for Service
* finish out testing File module, Service:brew and Package:brew
* Shell module should allow File's easy copy behavior to transfer scripts
* Baseline for unit test infrastructure, ideally with mocked providers.
* make conditionals human readable in callbacks - show test & evaluated value

opsmop-pull - simple implementation
* opsmop-pull [daemon|once] pull_cfg.py
* defines TRANSPORT=Transport(), CLI_STATUS_CALLBACKS=[ CliStatusCallback() ], PULL_STATUS_CALLBACKS=[ PullStatusCallback1(), ... ]
* asks transports.is_there_content()
* calls transport.download_content() -> returns (temp_dir, filename)
* uses opsmop.core.api with CLI_STATUS_CALLBACKS
* calls each .report_status in PULL_STATUS_CALLBACKS
* calls transport.sleep(), loops if called with 'daemon' mode.
* initial version comes with GitTransport(repo_url=<>) and recommended use is with ssh-agent to deal with checkout keys

opsmop-push -
* implementation ideas TBD

TODO list (later):

* Cool ideas everyone comes up with
* Merging stuff
* SPOILERS!


