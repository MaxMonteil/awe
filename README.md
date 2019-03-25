# AWE

![AWE Logo](/home/max/Pictures/awe_logo.png "The AWE Logo")

The Accessibility Web Engine aims to make the web more accessible by following WACG 2.0 standard.

## Table of Contents

* [About This Project](#about-this-project)
* [The Team](#the-team)
* [Getting Started](#getting-started)
	* [Prerequisites](#prerequisites)
	* [Installing](#installing)
* [API Functions](#api-functions)
* [Deployment](#deployment)
* [Built With](#built-with)

## About This Project

Although the internet is now over 30 years old, it is still incredibly difficult for some people to navigate. Today with the huge amount of media content available, and with an ever increasing number connected people, it is more important than ever that a strong effort is made to create a more accessible internet.

This project aims to make the internet more accessible through our Accessibility Web Engine API which works by taking the URL of a page, scanning it, and returning a version that reaches or surpassed the WCAG 2.0 AA guideline level.

![API Structure](/home/max/Pictures/api_structure.png "The AWE API's structure")

## The Team

* [Hussein Murtada](https://github.com/husseinmur)
* [Maria Daou](https://github.com/mariadaou)
* [Marina Kayrouz](https://github.com/MarinaKeyrouz)
* [Maxime Hermez](https://github.com/MaxHermez)
* [Maximilien Monteil](https://github.com/MaxMonteil)
* [Waseem Elghali](https://github.com/Sauronsring)

## Getting Started

### Prerequisites

You will need to have a [Google Cloud Platform](https://cloud.google.com/) instance.

Make sure you also have [pipenv](https://pipenv.readthedocs.io) installed on your machine in order to easily set up the environment.

### Installing

```
git clone git@github.com:MaxMonteil/awe.git
cd awe
pipenv install
```

## API Functions

\* Indicates function is feasible but is not 100% guaranteed. It will require an AI model to improve.

** Indicates function is not feasible within the scope of this course. Requires an AI model.

**DEMO** Indicates that this function needs to be implemented in time for the demo.

### accesskeys

Adds accesskey attribute to interactive HTML elements.

#### Input

Submitted HTML file/string

#### Output

Optimized HTML file

#### Terms

* Accesskey is an HTML attribute that binds the chosen keyboard key to the HTML element in order to switch focus to that element.

#### Example

##### Input

```HTML
<a href="index.html">table of Content</a>
```

##### Output

```HTML
<a href="index.html" accesskey="C">table of Content</a>
```

### aria-allowed-attr\**

This function fixes assigned allowed attribute with the semantically-appropriate role.

*In order to do this without human input, we need to utilize an AI model that recognizes the semantically-appropriate roles for each element.*


### aria-required-attr\*

Adds an “aria-required” attribute as part of the field's name for visually-represented elements.

#### Input

Submitted HTML file/string

#### Output

Optimized HTML file

#### Terms

* The parts of the HTML code that have a direct visual representation in the client's browser.

#### Example

##### Input

```HTML
<input type="text" name="username" id="username"/>
```

##### Output

```HTML
<input type="text" name="username" id="username" aria-required="true"/>
```

### aria-required-children\**

Ensure all ARIA roles have their required children elements if any. Adds missing required children elements.

### aria-required-parent\**

Ensure all ARIA roles have their required parent elements if any. Adds missing required parents elements.


### aria-roles\**

Defines the role of an element using the “role” attribute with one of the non-abstract values defined in the WAI-ARIA Definition of Roles.

#### Example

```HTML
<div role="toolbar"></div>
```

### aria-valid-attr-value\**

Replaces invalid values with valid values for ARIA attributes.

### aria-valid-attr\*

Replaces invalid attributes with valid ARIA attributes.

#### Input

Submitted HTML file/string

#### Output

Optimized HTML file

#### Terms

* An invalid attribute is one that is misspelled or non-existent.

#### Example

##### Input

```HTML
<ul role="menubar">
    <li role="menuitem" aria-haspopup="F" aria-labelledby="filelabl" aria-required="tru">File</li>
</ul>
```

##### Output

```HTML
<ul role="menubar">
    <li role="menuitem" aria-haspopup="false" aria-labelledby="filelabel" aria-required="true">File</li>
</ul>
```

### audio-caption **DEMO**

Audio and video content in their corresponding HTML tags get subtitles or captions added in a `<track>` tag.

#### Input

Submitted HTML file/string

#### Output

Optimized HTML file

*Utilizes speech-to-text API to create subtitles for the audio.*

#### Example

```HTML
<video controls width="250" src="/media/examples/friday.mp4">
	<track default kind="captions" srclang="en" src="/media/examples/friday.vtt"/>
	Sorry, your browser doesn't support embedded videos.
</video>
```

### button-name

Make the inner text of button elements, aria “role” = “button” elements, and button type input fields discernable to screen readers. Done with proper aria-label and value attributes.

#### Input

Submitted HTML file/string

#### Output

Optimized HTML file

*Makes sure that every button element is visible, e.g. clicking a certain picture sometimes functions as a button. Instead, a visible button will be placed next to the picture.*

#### Example

##### Input

```HTML
<input type="button" aria-hidden="true" value="">
```

##### Output

```HTML
<input type="button" aria-hidden="false" value="Click here" aria-label="button">
```

### bypass

Adds a ‘Skip to Content’ link to the header. This link moves the user from the top of the page down to the start of the page’s content when they are navigating the page with the keyboard.

#### Input

Submitted HTML file/string

#### Output

Optimized HTML file

#### Example

```HTML
<header>
	<a id="skip" alt="skip to content" href="#content"> Skip to content<a/>
<header/>
```

### color-contrast **DEMO**

Modifies the background and foreground color of text content to increase the contrast. Defaults to black on white (or vice versa for dark themes).

#### Input

Submitted HTML file/string

#### Output

Optimized HTML file

*Modify color contrast of at least 4.5:1 for small text or 3:1 for large text, even if the text is part of an image*

#### Example

![Example of text on backgrounds with varying contrast levels.](https://opentextbc.ca/accessibilitytoolkit/wp-content/uploads/sites/94/2015/02/colour-contrast-egs.jpg)

### definition-list

Ensures `<dl>` children elements are only of type`<dt>` and `<dd>`. Additionally, `<dt>` elements must always be followed by one or more `<dd>` elements.

#### Input

Submitted HTML file/string

#### Output

Optimized HTML file

#### Example

```HTML
<dl>
    <dt>Coffee</dt>
    <dd>Black hot drink</dd>
    <dt>Milk</dt>
    <dd>White cold drink</dd>
</dl>
```

### dlitem

Definition list items (`<dt>`, `<dd>`) must be direct children of a `<dl>` element.

#### Input

Submitted HTML file/string

#### Output

Optimized HTML file

#### Example

##### Input

```HTML
<dt>Coffee</dt>
<dd>Black hot drink</dd>
<dt>Milk</dt>
<dd>White cold drink</dd>
```

##### Output

```HTML
<dl>
    <dt>Coffee</dt>
    <dd>Black hot drink</dd>
    <dt>Milk</dt>
    <dd>White cold drink</dd>
</dl>
```

### document-title

Adds title to the `<head>` if missing.

#### Input

Submitted HTML file/string

#### Output

Optimized HTML file

#### Example

```HTML
<html>
	<title> A brief, clear, informative, and unique title</title>
	<!-- the rest of the page content -->
</html>
```

### duplicate-id

Removes ID duplicates if more than one element has the same ID.

#### Input

Submitted HTML file/string

#### Output

Optimized HTML file

#### Example

##### Input

```HTML
<html>
    <input type="text" id="TextBox"/>
    <input type="text" id="TextBox"/>
</html>
```

##### Output

```HTML
<html>
    <input type="text" id="TextBox1"/>
    <input type="text" id="TextBox2"/>
</html>
```

### frame-title

Adds a title for `<iframe>` tag depending on its content.

#### Input

Submitted HTML file/string

#### Output

Optimized HTML file

*Ensure all* `<frame>` *and* `<iframe>` *elements have valid title attribute values.
Adds a title attribute to a frame element.*

#### Example

```HTML
<iframe title="myFrame" ...> frame body </iframe>
```

### html-lang

Adds the missing lang on `<html>` tag.

#### Input

Submitted HTML file/string

#### Output

Optimized HTML file

*Add a lang attribute to the HTML element which represents the primary language of the document.*

#### Example

```HTML
<html lang="en">
    <!-- document text -->
</html>
```

### html-lang-valid

Changes the HTML lang property to the correct one.

#### Input

Submitted HTML file/string

#### Output

Optimized HTML file

#### Example

##### Input

```HTML
<html lang="en">
    <p>Ceci est un paragraphe.</p>
</html>
```

##### Output

```HTML
<html lang="fr">
    <p>Ceci est un paragraphe.</p>
</p>
```

### image-alt

Adds the missing alt text, this text will be returned from an image classification API.

#### Input

Submitted HTML file/string

#### Output

Optimized HTML file

---

There are three main ways to add alternate text to an image:

* Using an alt attribute i.e.

```HTML
<img alt="drawing of a cat" src="...">
```

* Using an aria-label i.e.

```HTML
<img aria-label="drawing of a cat" src="...">
```

* Using an aria-labelledby attribute i.e.

```HTML
<img arialabelledby="someID" src="...">
```

### input-image-alt **DEMO**

Adds the missing alt text to image inputs like buttons, checkboxes, etc…

#### Input

Submitted HTML file/string

#### Output

Optimized HTML file

#### Example

```HTML
<input type="image" src="submit.png" name="submit" height="36" width="113" alt="Submit">
```

### label

Adds missing labels to forms elements.

#### Input

Submitted HTML file/string

#### Output

Optimized HTML file

#### Example

```HTML
<label>First Name: <input type="text" name="fname"></label>
<label>Last Name: <input type="text" name="lname"></label>
```

### layout-table

Optimizes the layout of tables to be screen reader friendly.
Header cells must be marked up with `<th>`, and data cells with `<td>` to make tables accessible

#### Input

Submitted HTML file/string

#### Output

Optimized html file

*Ensures that presentational* `<table>` *elements do not use* `<th>`*,* `<caption>` *elements or the summary attribute.
The table-layout property defines the algorithm to be used to lay out the table cells, rows, and columns in CSS.*


### link-name

Ensure that all links are accessible.

#### Input

Submitted HTML file/string

#### Output

Optimized HTML file

*Replace onmouseover(), mouseover(), hover(), onmouseout(), mouseout() with these with device-independent events such as onfocus(), focus(), onblur(), or blur().*


### list

Orders the paragraph using different types of lists (unordered list, ordered list, description list) to group information according to its nature to provide orientation for users.

#### Input

Submitted HTML file/string

#### Output

Optimized HTML file

#### Example

##### Input

```HTML
<p>
    Paragraph 1.
    Paragraph 2.
    Paragraph 3.
</p>
```

##### Output

```HTML
<p>
    <ul>
        <li>Paragraph 1.</li>
        <li>Paragraph 2.</li>
        <li>Paragraph 3.</li>
    </ul>
</p>
```

### list-item

Identifies and groups an item inside a list of items.

#### Input

Submitted HTML file/string

#### Output

Optimized HTML file

#### Example

##### Input

```HTML
<li>Item</li>
```

##### Output

```HTML
<ul>
    <li>Item</li>
</ul>
```

### meta-refresh

Enables redirects on the client side without confusing the user by using `<meta>` at the beginning of the code.

#### Input

Submitted HTML file/string

#### Output

Optimized HTML file

#### Example

##### Input

```HTML
<meta http-equiv="refresh" content="...;url=..." />
```

##### Output

```HTML
<script language="javascript" type="text/javascript">
	window.location.href = 'URL';
</script>
```

### meta-viewport

Adds `<meta name="viewport">` tag in the `<head>` of the document. It also checks that the node contains a content attribute and that the value of this attribute contains the text width.

#### Input

Submitted HTML file

#### Output

Optimized HTML file

#### Example

```HTML
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
```

### object-alt

Adds a set of tags (namely, img, area and optionally for input and applet) to allow you to provide a text equivalent for the object.

#### Input

Submitted HTML file

#### Output

Optimized HTML file

#### Example of Output

```HTML
<object id="object123" alt="Video Clip" param="abc">
```

### tab-index

Elements should not have tabindex greater than zero.

#### Input

Submitted HTML file

#### Output

Optimized HTML file

#### Example

##### Input

```HTML
<a href="http://www.google.com/" tabindex="1">Google</a>
```

##### Output
```HTML
<a href="http://www.google.com/" tabindex="0">Google</a>
```

### td-headers-attr
All cells in a `<table>` element that use the headers attribute must only refer to other cells of that same table

#### Input

Submitted HTML file

#### Output

Optimized HTML file

*To provide the markup necessary to convey the relationship between header cells and data cells in the data tables, it can be accomplished with the scope attribute.*

#### Example

```HTML
<thead>
	<tr>
		<th scope="col">Name</th>
		<th scope="col">1 km</th>
		<th scope="col">5 km</th>
		<th scope="col">10 km</th>
	</tr>
</thead>

<tbody>
	<tr>
		<th scope="row">Mary</th>
		<td>8:32</td>
		<td>28:04</td>
		<td>1:01:16</td>
	</tr>
</tbody>
```

### th-data-cells

All non-empty `<td>` elements in a table larger than 3 by 3 must have an associated table header, by changing the `<td>` to a `<th>`.

#### Input

Submitted HTML file

#### Output

Optimized HTML file

#### Example

##### Input

```HTML
<table class="data">
	<caption>
		Greensprings Running Club Personal Bests
	</caption>
	<thead>
		<tr>
			<th scope="col">Name</th>
			<th scope="col">1 km</th>
			<th scope="col">5 km</th>
			<th scope="col">10 km</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<th scope="row">Mary</th>
			<td>8:32</td>
			<td>28:04</td>
			<td>1:01:16</td>
		</tr>
		<tr>
			<th scope="row">Betsy</th>
			<td>7:43</td>
			<td>26:47</td>
			<td>55:38</td>
		</tr>
		<tr>
			<th scope="row">Matt</th>
			<td>7:55</td>
			<td>27:29</td>
			<td>57:04</td>
		</tr>
		<tr>
			<th scope="row">Todd</th>
			<td>7:01</td>
			<td>24:21</td>
			<td>50:35</td>
		</tr>
	</tbody>
</table>
```

##### Output

```HTML
<table class="data complex" border="1">
    <caption>
        Example 2 (column group headers):
    </caption>
    <tr>
        <td rowspan="2"><span class="offscreen">empty</span></td>
        <th colspan="2" id="females2">Females</th>
        <th colspan="2" id="males2">Males</th>
    </tr>
    <tr>
        <th width="40" id="mary2">Mary</th>
        <th width="35" id="betsy2">Betsy</th>
        <th width="42" id="matt2">Matt</th>
        <th width="42" id="todd2">Todd</th>
    </tr>
    <tr>
        <th width="39" id="mile1_2">1 mile</th>
        <td headers="females2 mary2 mile1_2">8:32</td>
        <td headers="females2 betsy2 mile1_2">7:43</td>
        <td headers="males2 matt2 mile1_2">7:55</td>
        <td headers="males2 todd2 mile1_2">7:01</td>
    </tr>
    <tr>
        <th id="km5_2">5 km</th>
        <td headers="females2 mary2 km5_2">28:04</td>
        <td headers="females2 betsy2 km5_2">26:47</td>
        <td headers="males2 matt2 km5_2">27:29</td>
        <td headers="males2 todd2 km5_2">24:21</td>
    </tr>
    <tr>
        <th id="km10_2">10 km</th>
        <td headers="females2 mary2 km10_2">1:01:16</td>
        <td headers="females2 betsy2 km10_2">55:38</td>
        <td headers="males2 matt2 km10_2">57:04</td>
        <td headers="males2 todd2 km10_2">50:35</td>
    </tr>
</table>
```

### valid-lang

Translates images alt text to the language in the HTML lang attribute.

#### Input

Submitted HTML file

#### Output

Optimized HTML file

#### Example

##### Input

```HTML
<img src="bonjour.jpg" alt="bonjour">
```

##### Output

```HTML
<img src="bonjour.jpg" alt="Good morning">
```

### video-caption **DEMO**

Adds captions to videos which don’t have captions.

#### Input

Submitted HTML file

#### Output

Optimized HTML file

#### Example

```HTML
<video width="300" height="200">
    <source src="myVideo.mp4" type="video/mp4">
    <track src="captions_en.vtt" kind="captions" srclang="en" label="english_captions">
    <track src="captions_es.vtt" kind="captions" srclang="es" label="spanish_captions">
</video>
```

### video-description

Labels videos by objects it contains using cloud video API.

#### Input

Submitted HTML file

#### Output

Optimized HTML file

#### Example

```HTML
<video width="300" height="200">
    <source src="myVideo.mp4" type="video/mp4">
    <track src="audio_desc_en.vtt" kind="descriptions" srclang="en" label="english_description">
    <track src="audio_desc_es.vtt" kind="descriptions" srclang="es" label="spanish_description">
</video>
```

## Built With
