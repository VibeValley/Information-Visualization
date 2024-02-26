import * as d3 from "https://cdn.jsdelivr.net/npm/d3@7/+esm";
import fullInteractionData from "./starwars-interaction/starwars-full-interactions-allCharacters.json" assert { type: "json" };
import data1 from "./starwars-interaction/starwars-episode-1-interactions-allCharacters.json" assert { type: "json" };
import data2 from "./starwars-interaction/starwars-episode-2-interactions-allCharacters.json" assert { type: "json" };
import data3 from "./starwars-interaction/starwars-episode-3-interactions-allCharacters.json" assert { type: "json" };
import data4 from "./starwars-interaction/starwars-episode-4-interactions-allCharacters.json" assert { type: "json" };
import data5 from "./starwars-interaction/starwars-episode-5-interactions-allCharacters.json" assert { type: "json" };
import data6 from "./starwars-interaction/starwars-episode-6-interactions-allCharacters.json" assert { type: "json" };
import data7 from "./starwars-interaction/starwars-episode-7-interactions-allCharacters.json" assert { type: "json" };

function changeDataset(episode) {
  var dataArray = [
    fullInteractionData,
    data1,
    data2,
    data3,
    data4,
    data5,
    data6,
    data7,
  ];

  return dataArray[parseInt(episode)];
}
var leftData = changeDataset(0);
var rightData = changeDataset(0);
var leftSelect = document.getElementById("EpisodeChooserLeft");
var rightSelect = document.getElementById("EpisodeChooserRight");
var leftTooltipName = d3.select(".leftName").text("");
var leftTooltipInteraction = d3.select(".leftInteractions").text("");
var rightTooltipName = d3.select(".rightName").text("");
var rightTooltipInteraction = d3.select(".rightInteractions").text("");
const rangeSlider = document.getElementById("mySlider");
let slidingValue = 30;

leftSelect.addEventListener("change", function () {
  var selectedText = leftSelect.options[leftSelect.selectedIndex].value;
  leftData = changeDataset(selectedText);
  runLeftSimulation();
});
rightSelect.addEventListener("change", function () {
  var selectedText = rightSelect.options[rightSelect.selectedIndex].value;
  rightData = changeDataset(selectedText);
  runRightSimulation(slidingValue);
});
rangeSlider.addEventListener("input", () => {
  //console.log(rangeSlider.value);
  slidingValue = rangeSlider.value;
  //runRightSimulation(rangeSlider.value);
});

function linkHighlightHover(node) {
  var leftSVG = d3
    .select(".nodes")
    .selectAll("circle")
    .filter((d) => {
      //console.log(d, node);
      return d.name === node.name;
    })
    .transition()
    .duration(150)
    .attr("r", (d) => {
      leftTooltipInteraction.text(d.value);
      leftTooltipName.text(d.name);
      return d.value / 6 + 10;
    })
    .style("stroke", "#000000")
    .style("stroke-width", "4px");
  //console.log(d3.selectAll("g.nodes2"));

  var rightSVG = d3
    .select(".nodes2")
    .selectAll("circle")
    .filter((d) => {
      //console.log(d, node);
      return d.name === node.name;
    })
    .transition()
    .duration(150)
    .attr("r", function (d) {
      //leftTooltipName.text(d.source.name + " with " + d.target.name);
      rightTooltipInteraction.text(d.value);
      rightTooltipName.text(d.name);
      return d.value / 6 + 10;
    })
    .style("stroke", "#000000")
    .style("stroke-width", "4px");
}

function linkHighlightOut(node) {
  var leftSVG = d3
    .select(".nodes")
    .selectAll("circle")
    .filter((d) => {
      //console.log(d, node);
      return d.name === node.name;
    })
    .transition()
    .duration(150)
    .attr("r", function (d) {
      leftTooltipInteraction.text("");
      leftTooltipName.text("");
      return d.value / 6 + 5;
    })
    .style("stroke", "");

  var rightSVG = d3
    .select(".nodes2")
    .selectAll("circle")
    .filter((d) => {
      //console.log(d, node);
      return d.name === node.name;
    })
    .transition()
    .duration(150)
    .attr("r", function (d) {
      rightTooltipInteraction.text("");
      rightTooltipName.text("");
      return d.value / 6 + 5;
    })
    .style("stroke", "");
}

var width = 600;
var height = 600;

function runLeftSimulation() {
  let zoom = d3.zoom().on("zoom", handleZoom);

  function handleZoom(e) {
    d3.select(".svg")
      .selectAll("g.links, g.nodes")
      .attr("transform", e.transform);
  }

  function initZoom() {
    d3.select(".svg").call(zoom);
  }

  var nodes = leftData.nodes;
  var links = leftData.links;
  var simulation = d3
    .forceSimulation(nodes)
    .force("charge", d3.forceManyBody().strength(-200))
    .force(
      "center",
      d3
        .forceCenter()
        .x(width / 2)
        .y(height / 2)
    )
    .force("link", d3.forceLink().links(links))
    .force(
      "collision",
      d3.forceCollide().radius(function (d) {
        return d.value / 6 + 5;
      })
    )
    .on("tick", ticked);

  function updateLinks() {
    var u = d3
      .select(".links")
      .selectAll("line")
      .data(links)
      .join("line")
      .attr("x1", function (d) {
        return d.source.x;
      })
      .attr("y1", function (d) {
        return d.source.y;
      })
      .attr("x2", function (d) {
        return d.target.x;
      })
      .attr("y2", function (d) {
        return d.target.y;
      })
      .on("mouseover", function (event, d) {
        d3.select(this)
          .transition()
          .duration(150)
          .style("stroke", "#000000")
          .style("stroke-width", "5");
        return (
          leftTooltipName.text(d.source.name + " with " + d.target.name) &&
          leftTooltipInteraction.text(d.value)
        );
      })
      .on("mouseout", function (event, d) {
        d3.select(this)
          .transition()
          .duration(150)
          .style("stroke", "#ccc")
          .style("stroke-width", "2");
        return leftTooltipName.text("") && leftTooltipInteraction.text("");
      });
  }

  function updateNodes() {
    var u = d3
      .select(".nodes")
      .selectAll("circle")
      .data(nodes)
      .join("circle")
      .attr("r", function (d) {
        return d.value / 6 + 5;
      })
      .style("fill", function (d) {
        return d.colour;
      })
      .attr("cx", function (d) {
        return d.x;
      })
      .attr("cy", function (d) {
        return d.y;
      })
      .on("mouseover", function (event, d) {
        d3.select(this)
          .transition()
          .duration(150)
          .attr("r", d.value / 6 + 10)
          .style("stroke", "#000000")
          .style("stroke-width", "4px");

        linkHighlightHover(d);
        //d.style("fill", "#000000");
        return (
          leftTooltipName.text(d.name) && leftTooltipInteraction.text(d.value)
        );
      })
      .on("mouseout", function (event, d) {
        d3.select(this)
          .transition()
          .duration(150)
          .attr("r", d.value / 6 + 5);

        linkHighlightOut(d);
        return leftTooltipName.text("") && leftTooltipInteraction.text("");
      });
  }

  function ticked() {
    updateLinks();
    updateNodes();
  }

  initZoom();
}

function runRightSimulation(_sliderValue) {
  var nodes = rightData.nodes;
  var links = rightData.links;
  let sliderValue = _sliderValue;
  let zoomRight = d3.zoom().on("zoom", handleZoomRight);
  console.log(sliderValue);
  function handleZoomRight(e) {
    d3.select(".svg2")
      .selectAll("g.links2, g.nodes2")
      .attr("transform", e.transform);
  }

  function initZoomRight() {
    d3.select(".svg2").call(zoomRight);
  }

  var simulationRight = d3
    .forceSimulation(nodes)
    .force("charge", d3.forceManyBody().strength(-100))
    .force(
      "center",
      d3
        .forceCenter()
        .x(width / 2)
        .y(height / 2)
    )
    .force("link", d3.forceLink().links(links))
    .on("tick", tickedRight);

  function tickedRight() {
    updateNodesRight();
    updateLinksRight();
  }

  function updateLinksRight() {
    var u = d3
      .select(".links2")
      .selectAll("line")
      .data(links)
      .join("line")

      .attr("x1", function (d) {
        return d.source.x;
      })
      .attr("y1", function (d) {
        return d.source.y;
      })
      .attr("x2", function (d) {
        return d.target.x;
      })
      .attr("y2", function (d) {
        return d.target.y;
      })
      .on("mouseover", function (event, d) {
        d3.select(this)
          .transition()
          .duration(150)
          .style("stroke", "#000000")
          .style("stroke-width", "5");
        return (
          rightTooltipName.text(d.source.name + " with " + d.target.name) &&
          rightTooltipInteraction.text(d.value)
        );
      })
      .on("mouseout", function (event, d) {
        d3.select(this)
          .transition()
          .duration(150)
          .style("stroke", "#ccc")
          .style("stroke-width", "2");
        return rightTooltipName.text("") && rightTooltipInteraction.text("");
      });
  }

  function updateNodesRight() {
    var u = d3
      .select(".nodes2")
      .selectAll("circle")
      .data(nodes)
      .join("circle")
      .filter((d) => {
        console.log(sliderValue);
        return d.value > sliderValue;
      })
      .attr("r", function (d) {
        return d.value / 6 + 5;
      })
      .style("fill", function (d) {
        return d.colour;
      })
      .attr("cx", function (d) {
        return d.x;
      })
      .attr("cy", function (d) {
        return d.y;
      })
      .on("mouseover", function (event, d) {
        d3.select(this)
          .transition()
          .duration(150)
          .attr("r", d.value / 6 + 10)
          .style("stroke", "#000000")
          .style("stroke-width", "5px");
        linkHighlightHover(d);
        return (
          rightTooltipName.text(d.name) && rightTooltipInteraction.text(d.value)
        );
      })
      .on("mouseout", function (event, d) {
        d3.select(this)
          .transition()
          .duration(150)
          .attr("r", d.value / 6 + 5)
          .style("stroke", "");
        linkHighlightOut(d);
        return rightTooltipName.text("") && rightTooltipInteraction.text("");
      });
  }
  initZoomRight();
}

runLeftSimulation();
//runRightSimulation(slidingValue);
