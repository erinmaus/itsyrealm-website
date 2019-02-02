`/`
`/home`
* Home page

`/home/download`
* Download select page (allows selecting other versions)

`/home/nominomicon`
* Nominomicon (under construction)

`/admin`
* Bootstrap
* Main admin page
* Links to builds & screenies

`/admin/screenies`
* Upload screenies
* Download screenies
* So on.

`/admin/binaries`
* Can upload new launcher
* Can upload game builds (as zips)
* Can upload launchers (as whatever)

`/api/download/build/version`
`/api/download/build/version/<version>`
```
{
	version: "alpha-YYYYMMDD[x]"
	notes: "markdown"
	platforms: [ "Win32", etc ]
	checksum: SHA512
}
```

`/api/download/launcher/version`
`/api/download/launcher/version/<version>`
```
{
	version: "alpha-YYYYMMDD[x]"
	notes: "markdown"
	platforms: [ "Win32", etc ]
	checksum: SHA512
}
```

`/api/download/build/get/<platform>`
* Downloads latest build ZIP for `<platform>`
* Platform is one of: Win32, Win64, Linux32, Linux64, OSX

`/api/download/launcher/get/<platform>`
* Downloads game launcher
* Platform matches /api/game/build
