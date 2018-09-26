d3.json("dag-data/a-a-b-b-a-b-lexicographic.json", function (data) {
    drawGraph(data);
});

function drawGraph(data) {
    // Create the input graph
    var g = new dagreD3.graphlib.Graph()
      .setGraph({})
      .setDefaultEdgeLabel(function() { return {}; });

    for (let node of data) {
        g.setNode(node.id,  { label: node.position + (node.prediction.length > 0 ? ':' + node.prediction.join('') : ''), shape: "rect" });
        for (let parentId of node.parents) {
            if (parentId === null) continue;
            g.setEdge(parentId, node.id);
        }
    }

    // Create the renderer
    var render = new dagreD3.render();

    // Set up an SVG group so that we can translate the final graph.
    var svg = d3.select("svg"),
        svgGroup = svg.append("g");

    // Run the renderer. This is what draws the final graph.
    render(d3.select("svg g"), g);

    // Center the graph
    var xCenterOffset = (svg.attr("width") - g.graph().width) / 2;
    svgGroup.attr("transform", "translate(" + xCenterOffset + ", 20)");
    svg.attr("height", g.graph().height + 40);
}
