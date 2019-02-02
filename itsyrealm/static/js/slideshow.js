var Slideshow = [];
var SlideshowIndex = 0;
var SlideshowInterval = null;
var FullScreenElement = null;
var SLIDESHOW_SPEED = 2000;

function closeSlide() {
	if (FullScreenElement) {
		FullScreenElement.parentNode.removeChild(FullScreenElement);
		FullScreenElement = null;
	}
}

function clickSlide() {
	closeSlide();

	var rootElement = document.createElement('div');

	var backgroundElement = document.createElement('div');
	backgroundElement.classList.add("slideshow-image-full");
	rootElement.appendChild(backgroundElement);

	var contentElement = document.createElement('div');
	contentElement.classList.add("slideshow-image-full-content");
	rootElement.appendChild(contentElement);

	var slideshowElement = document.createElement('div');
	slideshowElement.classList.add("slideshow-image-full-image");
	contentElement.appendChild(slideshowElement);

	var titleElement = document.createElement('span');
	titleElement.classList.add("slideshow-image-full-title");
	titleElement.innerText = Slideshow[SlideshowIndex].title;
	slideshowElement.appendChild(titleElement);

	var imageElement = Slideshow[SlideshowIndex].full.cloneNode();
	imageElement.onclick = () => {
		closeSlide();
		SlideshowInterval = setInterval(tickSlide, SLIDESHOW_SPEED);
	}

	slideshowElement.appendChild(imageElement);

	var descriptionElement = document.createElement('span');
	descriptionElement.classList.add("slideshow-image-full-description");
	descriptionElement.innerText = Slideshow[SlideshowIndex].description;
	slideshowElement.appendChild(descriptionElement);

	document.querySelector("body").appendChild(rootElement);
	FullScreenElement = rootElement;

	if (SlideshowInterval) {
		clearInterval(SlideshowInterval)
	}
}

function updateSlide() {
	var slideshowElement = document.createElement('a');
	slideshowElement.href = "#/";
	slideshowElement.onclick = clickSlide;
	slideshowElement.appendChild(Slideshow[SlideshowIndex].thumb.cloneNode());

	let slideshowRoot = document.getElementById("ir-slideshow-image");
	if (slideshowRoot.childNodes.length === 0) {
		slideshowRoot.appendChild(slideshowElement);
	} else {
		let childNode = slideshowRoot.childNodes[0];
		slideshowRoot.replaceChild(slideshowElement, childNode);
	}
}

function tickSlide() {
	SlideshowIndex = (SlideshowIndex + 1) % Slideshow.length;
	updateSlide();
}

function incrementSlide() {
	SlideshowIndex = SlideshowIndex + 1;
	if (SlideshowIndex >= Slideshow.length) {
		SlideshowIndex = 0;
	}

	updateSlide();

	clearInterval(SlideshowInterval);
	SlideshowInterval = setInterval(tickSlide, SLIDESHOW_SPEED);
}

function decrementSlide() {
	SlideshowIndex = SlideshowIndex - 1;
	if (SlideshowIndex < 0) {
		SlideshowIndex = Slideshow.length - 1;
	}

	updateSlide();

	clearInterval(SlideshowInterval);
	SlideshowInterval = setInterval(tickSlide, SLIDESHOW_SPEED);
}

function generateSlideshow(json) {
	for (var i = 0; i < json.length; ++i) {
		var element = json[i];
		var full = new Image();
		full.src = "/api/photo/view/full/" + element.id;
		var thumb = new Image();
		thumb.src = "/api/photo/view/thumb/" + element.id;
		Slideshow.push({
			full: full,
			thumb: thumb,
			title: element.title,
			description: element.description
		});
	}
	updateSlide();

	SlideshowInterval = setInterval(tickSlide, SLIDESHOW_SPEED);

	document.getElementById("ir-slideshow-prev-button").onclick = decrementSlide;
	document.getElementById("ir-slideshow-next-button").onclick = incrementSlide;
}

fetch("/api/photo/list")
	.then(response => response.json())
	.then(json => generateSlideshow(json));
