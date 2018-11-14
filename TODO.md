STATUS: Still being refactored/upgraded to establish a strong baseline for future additions.
Bug queue and PRs will be open by December.

TODO list (shorter term ideas):

* Apache2 license headers
* make sure the variable system works like a scoped stack where values are cleared on each indent 
* verify condition/skipped behavior
* Still allow some way for Set('') to also do global scope.  Maybe Global()
* CLI should use ArgumentParser to have --options
* upgrade the default CLI output (what we have now is just a placeholder)
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

TODO list (later):

* Remote pull and push features per list
* Cool ideas everyone comes up with
* Merging stuff
* SPOILERS!


