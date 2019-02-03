function getPlatform() {
	var info = window.navigator.oscpu;

	if (info.indexOf("Win64") !== -1 || info.indexOf("Win32") !== -1) {
		return "Win64";
	} else if (info.indexOf("Windows") !== -1) {
		return "Win32";
	} else if (info.indexOf("Mac OS X") !== -1) {
		return "macOS";
	} else if (info.indexOf("x86_64") !== -1) {
		return "Linux64";
	} else if (info.indexOf("Linux") !== -1) {
		return "Linux32";
	}
}

function getNicePlatformName(platform) {
	switch (platform) {
		case "Win64":
			return "Windows (64-bit)";
		case "Win32":
			return "Windows (32-bit)";
		case "macOS":
			return "macOS";
		case "Linux64":
			return "Linux (64-bit)";
		case "Linux32":
			return "Linux (32-bit)";
		default:
			return "Unknown";
	}
}

function buildLinks(json) {
	var list = document.querySelector("#ir-platforms-list");
	for (var i = 0; i < json.length; ++i) {
		var listItem = document.createElement("li");
		var listItemLink = document.createElement("a");
		listItemLink.innerText = getNicePlatformName(json[i].platform);
		listItemLink.href = "/api/download/build/get/" + json[i].platform;
		listItem.appendChild(listItemLink);
		list.appendChild(listItem);
	}


	var platform = getPlatform();
	console.log(platform);

	var gotPlatform = false;
	for (var i = 0; i < json.length; ++i) {
		if (json[i].platform === platform) {
			var link = document.querySelector("#ir-download-link");
			link.href = "/api/download/build/get/" + platform;

			var text = document.querySelector("#ir-download-default-platform");
			text.innerText = getNicePlatformName(platform);

			gotPlatform = true;
			break;
		}
	}

	if (!gotPlatform && json.length > 0) {
		var link = document.querySelector("#ir-download-link");
		link.href = "/api/download/build/get/" + json[0].platform;

		var platform = document.querySelector("#ir-download-default-platform");
		platform.innerText = getNicePlatformName(json[0].platform);
	}
}

fetch("/api/download/build/version")
	.then(response => response.json())
	.then(json => buildLinks(json));
