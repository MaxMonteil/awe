<template>
  <div class="home">
    <h1 id="tagline">Making the web more accessible to the world, one page at a time.</h1>

    <h2>About</h2>
    <p>
      Although the internet is now over 30 years old, it is still incredibly difficult
      for some people to navigate. Today with the huge amount of media content
      available, and with an ever increasing number connected people, it is more
      important than ever that a strong effort is made to create a more accessible
      internet. This project aims to make the internet more accessible through our
      Accessibility Web Engine API which works by taking the URL of a page, scanning
      it, and returning a version that reaches or surpassed the WCAG 2.0 AA guideline
      level.
    </p>

    <h2>How It Works</h2>
    <img alt="AWE architecture" src="../assets/architecture.png" width="100%">
    <ol>
      <li>
        <h3>Send us your Webpage URL</h3>
        <p>
          Go to the <router-link class="nav-link" to="visualizer">visualizer</router-link> page and simply paste the URL to the page you want to fix.
        </p>
      </li>
      <li>
        <h3>AWE Accesses WCAG Compliance</h3>
        <p>
          Using Google Lighthouse we run specific diagnostics based on WCAG 2.1 requirements.
        </p>
      </li>
      <li>
        <h3>You Receive A Score</h3>
        <p>
          You will receive an in-depth analysis of your site as well as a score telling you how accessible your page currently is.
        </p>
      </li>
      <li>
        <h3>The Engine Runs Through Your Site</h3>
        <p>
          AWE maps the diagnostic results to its built-in functions and cloud APIs to generate accessibility features where needed.
        </p>
      </li>
      <li>
        <h3>You Get Your Accessible HTML!</h3>
        <p>
          Finally, AWE merges all the new features with your original HTML file giving you a clean accessible version of your site!
        </p>
      </li>
    </ol>
  </div>
</template>

<style>
#tagline {
  font-size: 5em;
  color: #4384F8;
}

.nav-link {
  text-decoration: none;
  color: #4384F8;
}

.nav-link:hover {
  text-decoration: underline;
}

.nav-link:visited {
  color: gray;
}
</style>
