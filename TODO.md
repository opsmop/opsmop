STATUS: Still being refactored/upgraded to establish a strong baseline for future additions.
Bug queue and PRs will be open by December.

TODO list (shorter term ideas):

* Apache2 license headers
* make sure the variable system works like a scoped stack where values are cleared on each indent 
* on j2 template errors, have much nicer error info (not a traceback)
* Still allow some way for Set('') to also do global scope.  Maybe Global()
* CLI should use ArgumentParser to have --options
* continued callback code improvement
* make a Debug module (like Set, but different)
* make FileUtils a seperate class in common, simply file type/provider code lots
* implement yum and apt for Package
* implement systemd for Service
* finish out testing File module, Service:brew and Package:brew
* Shell module should allow File's easy copy behavior to transfer scripts
* Baseline for unit test infrastructure, ideally with mocked providers.
* Start Sphinx documentation
* Push documentation website (opsmop.io)
* eliminate the need to use V by injecting all variables into the template namespace
* if the type passed to Roles() or Handlers() is a class and not an instance (a possible user error - instantiate the class)
* make conditional __str__ human readable and ideally mirror entry format

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


