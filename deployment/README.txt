This deployment folder contains files that describe how a release of TTR should be run on the gameservers.

uberdogs.yml contains the 'uberdogs' section of an astrond.yml. Please keep it updated, or else you'll break prod!

deploy.json describes a the environment for a release of TTR. It contains the version of astron to use as well as the version of Panda3D to use.
deploy.json also contains a version prefix. This is used to generate dev version strings on the development server (which are probably something like ttr-beta-dev-gabcdef0).
When we deploy a release to prod, we push a git tag named after the version to the repository (i.e. ttr-beta-v1.3.7). It is required that the tag's name contain the version prefix specified in deploy.json.
The key 'server-resources' maps to a list of file extensions of files in the resources directory that are necessary to be used server-side. We do not package and deploy art assets onto servers.

Last, server.prc is the configuration file we use for specifying config vars related to gameplay (a variable like want-sbhq should be put in server.prc, while a variable like air-stateserver does not belong here). server.prc is the last portion added to generated configuration files.
We also have a tag system to allow certain blocks of configuration to be used only in a certain environment. This allows us to generate releases that behaive differently depending on the environment that they are deployed in. For example:

-----
want-toontowncentral #t
#<prod>
want-bbhq #f
#</prod>

#<dev>
want-bbhq #t
#</dev>
-----

In prod, the parsed config file would look like this:

-----
want-toontowncentral #t
#<prod>
want-bbhq #f
#</prod>

#<dev>
##UNUSED SECTION
##want-bbhq #t
#</dev>
-----