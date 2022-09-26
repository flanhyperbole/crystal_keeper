Crystal Keeper - an extensible interface to different secret management apps to avoid the need for secrets being kept in env or config. 
Intended for developers to keep sesitive information syncronised across different machines without relying on cloud based or
 third party products by creating a network of machines autorised through ssh.
Base structure:
	- Keeper: logic behind auth access to other nodes in the network and keep them in sync
		- Provide general structures that other parts of the app need to adhere to
	- Crystals: auth with each secret source and provide api for set and get
		- Local and Remote Crystals give control over what should be synced to the entire network (Remote) and what is only to be changed locally
		- A single Crystal can have both a local and a remote variant
	- Shards: in-app for the secret object, probably an object on the crystal. Might have some convenience functions of parsing.

UI will be mostly just the dev experince in code, although a CLI for Keeper management would be good.

Techs needed:
	- SSH auth library
	- Sockets for listening to updates
	- Oauth, probably, for any third party app integration
	- python-secretstorage for linking to the ubuntu secret store which'll be the 'database'
	for secrets synced
Most of the services that will be integrated with will handle the decryption of the secret
For the extensibility, we'll want to rely on protocol

Testing:
	- all methods and functions should have a corresponding test
	- like to open up at some stage to pen testing
	- a generative library for fake information will be good also, Hypothesis
	- Keeper to 'connect' to yaml/json file which will mimic the structure of a crystal source

I do admit I don't really have an idea on how to have a 'test' instance up and running, possibly, POSSIBLY I could do some tests between machines with docker instances although I do not like docker
Test for what happens when nodes on the network get turned on or off.

Plan / Def of done: each stage should result in a running package / executable - it'll need to be a running server or the like that other apps connect to?
	- first stage should be local scope - connecting to ubuntu secrets, set and get, defining the structure of the data
	- option extra for this should be 'environemt injection' where a reference to the env at the boot of a project would inject matching secrets from Crystals
	- second stage connection to third party secrets providers - updating local and sync
	- third stage is connecting network together and syncing
	- stretch goals could be docker / cross os compatibility
	- stretchy stretch stretchems would be interfaces for other programming languages

Definate limitations are at the stretch and stretchy goal stages, where moving into C might be necessary (same for the environment injection idea). Although my kowledge in the setup of a service will make some problems at first stage. 


