This deployment folder contains files that describe how a release of TTR should be run on the gameservers.

uberdogs.yml contains the 'uberdogs' section of an astrond.yml. Please keep it updated, or else you'll break prod!

deploy.json describes a specific release of TTR. It contains the version of astron to use as well as the version of Panda3D to use.
deploy.json also contains a version prefix. For releases, a commit should be made that updates deploy.json to state the new version prefix.
The key 'server-resources' maps to a list of file extensions of files in the resources directory that are necessary to be used server-side. We do not package and deploy art assets onto servers.
For example:
deploy.json resides at prefix ttr-v1.0.1-
Git commit 6ebecf60d contains all the code that we want to push in v1.0.2
Whomever is making the release should create a single commit changing deploy.json's version prefix to ttr-v1.0.2-. Don't put anything else in that commit. Say it has commit hash 102bea8c9.
The final rendered version number, after deploy scripts are run, would be ttr-v1.0.2-102bea8.